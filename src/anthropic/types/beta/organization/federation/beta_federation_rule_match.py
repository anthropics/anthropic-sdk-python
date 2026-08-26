# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional

from ....._models import BaseModel

__all__ = ["BetaFederationRuleMatch"]


class BetaFederationRuleMatch(BaseModel):
    """Does the incoming JWT qualify?

    All populated fields must pass; omitted fields are skipped. At least one
    of `subject_prefix` (other than a wildcard-only value like `*`), `claims`,
    or `condition` is required; `audience` alone is not sufficient.
    """

    audience: Optional[str] = None
    """Exact match against the `aud` claim (any element if array).

    When omitted, the JWT's `aud` must still equal Anthropic's expected audience for
    the issuer; setting this field overrides that default.
    """

    claims: Optional[Dict[str, str]] = None
    """Exact-match `{claim: value}` pairs against top-level claims.

    Only string-valued claims can be matched; use `condition` for non-string claims.
    """

    condition: Optional[str] = None
    """CEL expression over claims for logic the structural fields can't express.

    Must evaluate to a boolean and may reference only the `claims` variable; a
    constant-true expression (such as `true`) is rejected with 400.
    """

    subject_prefix: Optional[str] = None
    """Match the verified JWT `sub` claim.

    Exact match unless the value ends with `*`, in which case it is a prefix match.
    Example: `repo:my-org/my-repo:ref:refs/heads/main`.
    """
