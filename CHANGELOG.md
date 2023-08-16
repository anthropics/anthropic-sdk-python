# Changelog

## [0.3.10](https://github.com/anthropics/anthropic-sdk-python/compare/v0.3.9...v0.3.10) (2023-08-16)


### Features

* add support for Pydantic v2 ([#121](https://github.com/anthropics/anthropic-sdk-python/issues/121)) ([cafa9be](https://github.com/anthropics/anthropic-sdk-python/commit/cafa9beef10afcec8cc537946c0ee5574f1c96e7))
* allow a default timeout to be set for clients ([#117](https://github.com/anthropics/anthropic-sdk-python/issues/117)) ([a115d2c](https://github.com/anthropics/anthropic-sdk-python/commit/a115d2c978ee6bbe749c55851833e52b8671e343))


### Chores

* assign default reviewers to release PRs ([#119](https://github.com/anthropics/anthropic-sdk-python/issues/119)) ([029a9e1](https://github.com/anthropics/anthropic-sdk-python/commit/029a9e157a4831203f0599d25a223a775fb937a6))
* **internal:** minor formatting change ([#120](https://github.com/anthropics/anthropic-sdk-python/issues/120)) ([7f2f54a](https://github.com/anthropics/anthropic-sdk-python/commit/7f2f54a76dbf182ce13a8d36741421a9c5cf2001))

## [0.3.9](https://github.com/anthropics/anthropic-sdk-python/compare/v0.3.8...v0.3.9) (2023-08-12)


### Features

* **docs:** remove extraneous space in examples ([#109](https://github.com/anthropics/anthropic-sdk-python/issues/109)) ([6d5c1f7](https://github.com/anthropics/anthropic-sdk-python/commit/6d5c1f72aea3156a4773ffb25ac00cdd75191652))


### Bug Fixes

* **docs:** correct async imports ([1ea1bf3](https://github.com/anthropics/anthropic-sdk-python/commit/1ea1bf342c8d54ff9c37ba1d1c591b4fd3362868))


### Documentation

* **readme:** remove beta status + document versioning policy ([#102](https://github.com/anthropics/anthropic-sdk-python/issues/102)) ([2f0a0f9](https://github.com/anthropics/anthropic-sdk-python/commit/2f0a0f9aeac863c18cfc9fff83b3c7675447f408))


### Chores

* **deps:** bump typing-extensions to 4.5 ([#112](https://github.com/anthropics/anthropic-sdk-python/issues/112)) ([f903269](https://github.com/anthropics/anthropic-sdk-python/commit/f9032699e6610363f0490026fb65e05f2283f782))
* **docs:** remove trailing spaces ([#113](https://github.com/anthropics/anthropic-sdk-python/issues/113)) ([e876a6b](https://github.com/anthropics/anthropic-sdk-python/commit/e876a6b957aa2f73f63b4b314942461e4f72de57))
* **internal:** bump pytest-asyncio ([#114](https://github.com/anthropics/anthropic-sdk-python/issues/114)) ([679ecd0](https://github.com/anthropics/anthropic-sdk-python/commit/679ecd0c3c365c70c1c677e5b7e33281cf36fafe))
* **internal:** update mypy to v1.4.1 ([#100](https://github.com/anthropics/anthropic-sdk-python/issues/100)) ([f615753](https://github.com/anthropics/anthropic-sdk-python/commit/f615753a4b6413f1e6af69e3698d19e74bafcdca))
* **internal:** update ruff to v0.0.282 ([#103](https://github.com/anthropics/anthropic-sdk-python/issues/103)) ([9db4b34](https://github.com/anthropics/anthropic-sdk-python/commit/9db4b34844c5bfee65ab4e1ad448ae13d6469e5f))

## [0.3.8](https://github.com/anthropics/anthropic-sdk-python/compare/v0.3.7...v0.3.8) (2023-08-01)


### Features

* **client:** add constants to client instances as well ([#95](https://github.com/anthropics/anthropic-sdk-python/issues/95)) ([d0fbe33](https://github.com/anthropics/anthropic-sdk-python/commit/d0fbe33bd9bab72438c2b80b48b80908bd994797))


### Chores

* **internal:** bump pyright ([#94](https://github.com/anthropics/anthropic-sdk-python/issues/94)) ([d2872dc](https://github.com/anthropics/anthropic-sdk-python/commit/d2872dcc19c409cb7383e70f0472378a0ae86ff0))
* **internal:** make demo example runnable and more portable ([#92](https://github.com/anthropics/anthropic-sdk-python/issues/92)) ([dea1aa2](https://github.com/anthropics/anthropic-sdk-python/commit/dea1aa2f4b699043780b61d92e93c0f2a8fe59bd))


### Documentation

* **readme:** add token counting reference ([#96](https://github.com/anthropics/anthropic-sdk-python/issues/96)) ([79a339e](https://github.com/anthropics/anthropic-sdk-python/commit/79a339e962aa51cf79064af787ce11bd7984e0e4))

## [0.3.7](https://github.com/anthropics/anthropic-sdk-python/compare/v0.3.6...v0.3.7) (2023-07-29)


### Features

* **client:** add client close handlers ([#89](https://github.com/anthropics/anthropic-sdk-python/issues/89)) ([2520a03](https://github.com/anthropics/anthropic-sdk-python/commit/2520a034eed3e218f25f369783ebd09e2763e803))


### Bug Fixes

* **client:** correctly handle environment variable access ([aa53754](https://github.com/anthropics/anthropic-sdk-python/commit/aa53754c71cdfc31f236b41222752f3a58602061))


### Documentation

* **readme:** use `client` everywhere for consistency ([0ff8924](https://github.com/anthropics/anthropic-sdk-python/commit/0ff89245f4aa7ca3f6282827ab7c5cca3be534fb))


### Chores

* **internal:** minor refactoring of client instantiation ([adf9158](https://github.com/anthropics/anthropic-sdk-python/commit/adf91584ade62e3a4c2fbef011a62cf9284db931))
* **internal:** minor reformatting of code ([#90](https://github.com/anthropics/anthropic-sdk-python/issues/90)) ([1175572](https://github.com/anthropics/anthropic-sdk-python/commit/1175572db453b681b5aa8469d09f9400ddcd4946))

## [0.3.6](https://github.com/anthropics/anthropic-sdk-python/compare/v0.3.5...v0.3.6) (2023-07-22)


### Documentation

* **readme:** reference "client" in errors section and add missing import ([#79](https://github.com/anthropics/anthropic-sdk-python/issues/79)) ([ddc81cf](https://github.com/anthropics/anthropic-sdk-python/commit/ddc81cf0c1593ed9d4855e27fbcc0a393cf2c3a2))

## [0.3.5](https://github.com/anthropics/anthropic-sdk-python/compare/v0.3.4...v0.3.5) (2023-07-19)


### Features

* add flexible enum to model param ([#75](https://github.com/anthropics/anthropic-sdk-python/issues/75)) ([d16bb45](https://github.com/anthropics/anthropic-sdk-python/commit/d16bb45c49f4f401bd33ab57d5f9a586bd1e9a01))


### Documentation

* **examples:** bump model to claude-2 in example scripts ([#67](https://github.com/anthropics/anthropic-sdk-python/issues/67)) ([cd68de2](https://github.com/anthropics/anthropic-sdk-python/commit/cd68de2c5351fca85784e44d6eee5d90c835f64b))


### Chores

* **internal:** add `codegen.log` to `.gitignore` ([#72](https://github.com/anthropics/anthropic-sdk-python/issues/72)) ([d9b7e30](https://github.com/anthropics/anthropic-sdk-python/commit/d9b7e30b26235860fe9e7e3053171615173e32ca))

## [0.3.4](https://github.com/anthropics/anthropic-sdk-python/compare/v0.3.3...v0.3.4) (2023-07-11)


### Chores

* **package:** pin major versions of dependencies ([#59](https://github.com/anthropics/anthropic-sdk-python/issues/59)) ([3a75464](https://github.com/anthropics/anthropic-sdk-python/commit/3a754645aa7381d160e985451f385ce231a66904))


### Documentation

* **api:** reference claude-2 ([#61](https://github.com/anthropics/anthropic-sdk-python/issues/61)) ([91ece29](https://github.com/anthropics/anthropic-sdk-python/commit/91ece29cd6ae9ba9a060bee8b55fb62ddc1b69ac))
* **readme:** update examples to use claude-2 ([#65](https://github.com/anthropics/anthropic-sdk-python/issues/65)) ([7e4714c](https://github.com/anthropics/anthropic-sdk-python/commit/7e4714c19a64b2da74531ee7c051a5eef55d693c))
