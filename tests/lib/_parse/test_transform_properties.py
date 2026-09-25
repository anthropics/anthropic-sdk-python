"""
Fuzz-style property tests for transform_schema().

The invariant under test: the transform never silently drops information.
Every key in the input schema must survive into the output either as a
real, equal-valued key, or - when it is unsupported by the strict schema -
demoted into the description (the policy documented in _transform.py: "we
add them to the description so that the model *might* follow them").

Two generators are used:
- an exhaustive, bounded enumeration of small schemas, and
- a seeded random fuzzer that builds deeper, richer schemas (deterministic
  under a fixed seed so CI failures are reproducible).

Known intentional normalization (asserted explicitly rather than treated
as a silent drop): for object schemas the API only accepts
`additionalProperties: false`, so any input value is normalized to False.
"""

import random

from anthropic.lib._parse._transform import transform_schema

TYPES = ["object", "array", "string", "integer", "number", "boolean", "null"]

SUPPORTED_FORMATS = {
    "date-time",
    "time",
    "date",
    "duration",
    "email",
    "hostname",
    "uri",
    "ipv4",
    "ipv6",
    "uuid",
}

SCALAR_EXTRAS = [
    ("description", "A descriptive text"),
    ("title", "A title"),
    ("format", "email"),  # supported
    ("format", "custom-format"),  # unsupported -> demoted
    ("enum", ["a", "b"]),
    ("minimum", 1),
    ("maximum", 10),
    ("exclusiveMinimum", 0),
    ("exclusiveMaximum", 20),
    ("multipleOf", 2),
    ("pattern", "^[a-z]+$"),
    ("minLength", 1),
    ("maxLength", 100),
    ("minItems", 2),
    ("maxItems", 5),
    ("default", "fallback"),
    ("const", 7),
]

OBJECT_EXTRAS = [
    ("required", ["name"]),
    ("additionalProperties", True),
    ("additionalProperties", False),
]


def _simple_schema(rng, depth):
    """A leaf schema: a type plus a random subset of extra keywords."""
    schema = {"type": rng.choice(TYPES)}
    for key, value in SCALAR_EXTRAS:
        if rng.random() < 0.3:
            schema[key] = value
    if schema["type"] == "object":
        for key, value in OBJECT_EXTRAS:
            if rng.random() < 0.5:
                schema[key] = value
        if rng.random() < 0.7:
            schema["properties"] = {f"field{i}": _simple_schema(rng, depth + 1) for i in range(rng.randint(0, 2))}
    elif schema["type"] == "array":
        if rng.random() < 0.8:
            schema["items"] = _simple_schema(rng, depth + 1)
    return schema


def random_schema(rng, depth=0, max_depth=3):
    """Build a schema with a structural root plus extras, bounded by depth."""
    schema = {}
    roll = rng.random()
    if depth >= max_depth:
        schema["type"] = rng.choice(TYPES)
    elif roll < 0.1:
        # $ref schema: refs may carry arbitrary sibling keywords, which the
        # transform must preserve (demoted) rather than drop.
        schema["$ref"] = "#/$defs/Referenced"
        schema["$defs"] = {"Referenced": {"type": "string"}}
        for key, value in SCALAR_EXTRAS + OBJECT_EXTRAS:
            if rng.random() < 0.25:
                schema[key] = value
        return schema
    elif roll < 0.55:
        schema["type"] = rng.choice(TYPES)
    elif roll < 0.7:
        schema["anyOf"] = [_simple_schema(rng, depth + 1) for _ in range(rng.randint(1, 3))]
    elif roll < 0.85:
        schema["oneOf"] = [_simple_schema(rng, depth + 1) for _ in range(rng.randint(1, 3))]
    else:
        schema["allOf"] = [_simple_schema(rng, depth + 1) for _ in range(rng.randint(1, 3))]

    # Combine the structural root with random extra keywords; occasionally
    # combine a composition keyword with a `type` (the demote-to-description
    # path for composition keywords) or two composition keywords.
    for key, value in SCALAR_EXTRAS:
        if rng.random() < 0.2:
            schema[key] = value
    if schema.get("type") == "object":
        for key, value in OBJECT_EXTRAS:
            if rng.random() < 0.4:
                schema[key] = value
        n_props = rng.randint(0, 3)
        if n_props:
            schema["properties"] = {f"field{i}": _simple_schema(rng, depth + 1) for i in range(n_props)}
    elif schema.get("type") == "array":
        if rng.random() < 0.8:
            schema["items"] = _simple_schema(rng, depth + 1)
    if rng.random() < 0.12 and "type" in schema:
        extra = rng.choice(["anyOf", "oneOf", "allOf"])
        schema[extra] = [_simple_schema(rng, depth + 1) for _ in range(rng.randint(1, 2))]
    return schema


def assert_information_preserved(schema, transformed, path=()):
    """Assert every input key survives as a key or is demoted to the description."""
    description = transformed.get("description", "")
    for key, value in schema.items():
        # Structured keys preserved as real keys: recurse into the transformed
        # value so nested demotions are verified too.
        if key == "properties" and "properties" in transformed:
            assert set(value) == set(transformed["properties"]), (
                f"properties set changed at {path!r}: {sorted(value)!r} != {sorted(transformed['properties'])!r}"
            )
            for field_name, field_schema in value.items():
                assert_information_preserved(field_schema, transformed["properties"][field_name], path + (field_name,))
            continue
        if key in ("anyOf", "oneOf") and "anyOf" in transformed and (key == "anyOf" or "anyOf" not in schema):
            variants = transformed["anyOf"]
            assert len(variants) == len(value), f"variant count changed for {key} at {path!r}"
            for i, variant in enumerate(value):
                assert_information_preserved(variant, variants[i], path + (key, str(i)))
            continue
        if key == "allOf" and "allOf" in transformed:
            variants = transformed["allOf"]
            assert len(variants) == len(value), f"variant count changed for allOf at {path!r}"
            for i, variant in enumerate(value):
                assert_information_preserved(variant, variants[i], path + ("allOf", str(i)))
            continue
        if key == "items" and "items" in transformed:
            assert_information_preserved(value, transformed["items"], path + ("items",))
            continue
        if key == "$defs" and "$defs" in transformed:
            assert set(value) == set(transformed["$defs"]), f"$defs names changed at {path!r}"
            for def_name, def_schema in value.items():
                assert_information_preserved(def_schema, transformed["$defs"][def_name], path + ("$defs", def_name))
            continue
        if key == "$ref":
            assert transformed.get("$ref") == value, f"$ref changed at {path!r}"
            continue

        # Intentional normalization: the API only accepts
        # additionalProperties: false for object schemas.
        if key == "additionalProperties" and schema.get("type") == "object":
            assert transformed.get("additionalProperties") is False, (
                f"additionalProperties not normalized for object at {path!r}"
            )
            continue

        if key == "description":
            # The input description is kept as (a prefix of) the output
            # description, or demoted into it for $ref schemas.
            if "description" in transformed:
                assert value in transformed["description"] or (f"description: {value}" in transformed["description"]), (
                    f"description dropped at {path!r}"
                )
                continue

        # Preserved as a real, equal-valued key.
        if key in transformed:
            assert transformed[key] == value, (
                f"value for {key!r} changed at {path!r}: {value!r} -> {transformed[key]!r}"
            )
            continue

        # Otherwise the key must be demoted into the description.
        assert f"{key}: {value}" in description, (
            f"key {key!r} silently dropped at {path!r}: input {value!r}, output {transformed!r}"
        )


def test_transform_schema_fuzz_never_drops_information():
    rng = random.Random(37281)
    for _ in range(300):
        schema = random_schema(rng)
        transformed = transform_schema(schema)
        assert_information_preserved(schema, transformed)


def test_transform_schema_exhaustive_never_drops_information():
    """Exhaustive sweep over a bounded grammar of small schemas."""
    # Every single type with every subset of a small extras pool.
    small_extras = [
        ("description", "desc"),
        ("title", "t"),
        ("format", "custom"),
        ("enum", ["x"]),
        ("minimum", 1),
        ("default", 0),
    ]
    for type_ in TYPES:
        for mask in range(1 << len(small_extras)):
            schema = {"type": type_}
            for i, (key, value) in enumerate(small_extras):
                if mask & (1 << i):
                    schema[key] = value
            assert_information_preserved(schema, transform_schema(schema))

    # Composition keywords, including type + composition and anyOf + oneOf
    # combinations (the demote-to-description paths).
    compositions = [
        {"anyOf": [{"type": "string"}, {"type": "integer"}]},
        {"oneOf": [{"type": "string"}, {"type": "null"}]},
        {"allOf": [{"type": "string"}]},
        {"type": "string", "anyOf": [{"type": "string"}]},
        {"type": "integer", "oneOf": [{"type": "integer"}, {"type": "null"}]},
        {"anyOf": [{"type": "string"}], "oneOf": [{"type": "string"}]},
        {"anyOf": [{"type": "string"}], "allOf": [{"type": "string"}]},
        {"type": "string", "anyOf": [{"type": "string"}], "title": "t"},
        {
            "type": "object",
            "properties": {"a": {"type": "string", "default": "x"}},
            "required": ["a"],
            "anyOf": [{"type": "object"}],
        },
    ]
    for schema in compositions:
        assert_information_preserved(schema, transform_schema(schema))

    # $ref schemas with every subset of sibling keywords (silently dropped
    # before the fix).
    ref_siblings = [
        ("title", "t"),
        ("description", "d"),
        ("enum", ["a"]),
        ("format", "email"),
    ]
    for mask in range(1 << len(ref_siblings)):
        schema = {"$ref": "#/$defs/X", "$defs": {"X": {"type": "string"}}}
        for i, (key, value) in enumerate(ref_siblings):
            if mask & (1 << i):
                schema[key] = value
        assert_information_preserved(schema, transform_schema(schema))
