# Changelog

## 0.7.3 (2023-11-21)

Full Changelog: [v0.7.2...v0.7.3](https://github.com/anthropics/anthropic-sdk-python/compare/v0.7.2...v0.7.3)

### Bug Fixes

* **client:** attempt to parse unknown json content types ([#243](https://github.com/anthropics/anthropic-sdk-python/issues/243)) ([9fc275f](https://github.com/anthropics/anthropic-sdk-python/commit/9fc275f606b52690d5ccda78c72a6fded68ccb1e))


### Chores

* **client:** improve copy method ([#246](https://github.com/anthropics/anthropic-sdk-python/issues/246)) ([c84563f](https://github.com/anthropics/anthropic-sdk-python/commit/c84563fc69554b322d2a4254b6470ba7819689c3))
* **package:** add license classifier metadata ([#247](https://github.com/anthropics/anthropic-sdk-python/issues/247)) ([500d0ca](https://github.com/anthropics/anthropic-sdk-python/commit/500d0ca1e4d08f8c6b5d58071f438de9e1a31217))

## 0.7.2 (2023-11-17)

Full Changelog: [v0.7.1...v0.7.2](https://github.com/anthropics/anthropic-sdk-python/compare/v0.7.1...v0.7.2)

### Chores

* **internal:** update type hint for helper function ([#241](https://github.com/anthropics/anthropic-sdk-python/issues/241)) ([3179104](https://github.com/anthropics/anthropic-sdk-python/commit/31791042c52e825d1763123b14f44b9e68cc3466))

## 0.7.1 (2023-11-16)

Full Changelog: [v0.7.0...v0.7.1](https://github.com/anthropics/anthropic-sdk-python/compare/v0.7.0...v0.7.1)

### Documentation

* **readme:** minor updates ([#238](https://github.com/anthropics/anthropic-sdk-python/issues/238)) ([c40c4e1](https://github.com/anthropics/anthropic-sdk-python/commit/c40c4e1c9979f62a485df52bf51a5d730c3af38f))

## 0.7.0 (2023-11-15)

Full Changelog: [v0.6.0...v0.7.0](https://github.com/anthropics/anthropic-sdk-python/compare/v0.6.0...v0.7.0)

### Features

* **client:** support reading the base url from an env variable ([#237](https://github.com/anthropics/anthropic-sdk-python/issues/237)) ([dd91bfd](https://github.com/anthropics/anthropic-sdk-python/commit/dd91bfd278f4e2e76b2f194098f34070fd5a3ff9))


### Bug Fixes

* **client:** correctly flush the stream response body ([#230](https://github.com/anthropics/anthropic-sdk-python/issues/230)) ([a60d543](https://github.com/anthropics/anthropic-sdk-python/commit/a60d54331f8f6d28bf57dc979d4393759f5e1534))
* **client:** retry if SSLWantReadError occurs in the async client ([#233](https://github.com/anthropics/anthropic-sdk-python/issues/233)) ([33b553a](https://github.com/anthropics/anthropic-sdk-python/commit/33b553a8de5d45273ca9f335c59a263136385f14))
* **client:** serialise pydantic v1 default fields correctly in params ([#232](https://github.com/anthropics/anthropic-sdk-python/issues/232)) ([d5e70e8](https://github.com/anthropics/anthropic-sdk-python/commit/d5e70e8b803c96c8640508b31773b8b9d827d903))
* **models:** mark unknown fields as set in pydantic v1 ([#231](https://github.com/anthropics/anthropic-sdk-python/issues/231)) ([4ce7a1e](https://github.com/anthropics/anthropic-sdk-python/commit/4ce7a1e676023984be80fe0eacb1a0223780886c))


### Chores

* **internal:** fix devcontainer interpeter path ([#235](https://github.com/anthropics/anthropic-sdk-python/issues/235)) ([7f92e25](https://github.com/anthropics/anthropic-sdk-python/commit/7f92e25d6fa15bed799994d173ad62bcf60e5b3b))
* **internal:** fix typo in NotGiven docstring ([#234](https://github.com/anthropics/anthropic-sdk-python/issues/234)) ([ce5cccc](https://github.com/anthropics/anthropic-sdk-python/commit/ce5cccc9bc8482e4e3f6af034892a347eb2b52fc))


### Documentation

* fix code comment typo ([#236](https://github.com/anthropics/anthropic-sdk-python/issues/236)) ([7ef0464](https://github.com/anthropics/anthropic-sdk-python/commit/7ef0464724346d930ff1580526fd70b592759641))
* reword package description ([#228](https://github.com/anthropics/anthropic-sdk-python/issues/228)) ([c18e5ed](https://github.com/anthropics/anthropic-sdk-python/commit/c18e5ed77700bc98ba1c85638a503e9e0a35afb7))

## 0.6.0 (2023-11-08)

Full Changelog: [v0.5.1...v0.6.0](https://github.com/anthropics/anthropic-sdk-python/compare/v0.5.1...v0.6.0)

### Features

* **client:** adjust retry behavior to be exponential backoff ([#205](https://github.com/anthropics/anthropic-sdk-python/issues/205)) ([c8a4119](https://github.com/anthropics/anthropic-sdk-python/commit/c8a4119661c8ff74c7efa308963c2f187728a46f))
* **client:** allow binary returns ([#217](https://github.com/anthropics/anthropic-sdk-python/issues/217)) ([159ddd6](https://github.com/anthropics/anthropic-sdk-python/commit/159ddd69e6c438baf9abb1e518d0c2467c8f952c))
* **client:** improve file upload types ([#204](https://github.com/anthropics/anthropic-sdk-python/issues/204)) ([d85d1e0](https://github.com/anthropics/anthropic-sdk-python/commit/d85d1e04e36a90d43d134992ff4a5b1589aa6e0a))
* **client:** support accessing raw response objects ([#211](https://github.com/anthropics/anthropic-sdk-python/issues/211)) ([ebe8e4a](https://github.com/anthropics/anthropic-sdk-python/commit/ebe8e4a274f21d73cbc2fbb94fe56172f335cbd2))
* **client:** support passing BaseModels to request params at runtime ([#218](https://github.com/anthropics/anthropic-sdk-python/issues/218)) ([9f04ea6](https://github.com/anthropics/anthropic-sdk-python/commit/9f04ea6cf4a68e2ce65e8e00448b4d3de18a8dec))
* **client:** support passing chunk size for binary responses ([#227](https://github.com/anthropics/anthropic-sdk-python/issues/227)) ([c88f01e](https://github.com/anthropics/anthropic-sdk-python/commit/c88f01ed17b505e3e8a30c8a6adc9231e096b3e2))
* **client:** support passing httpx.Timeout to method timeout argument ([#222](https://github.com/anthropics/anthropic-sdk-python/issues/222)) ([ef58166](https://github.com/anthropics/anthropic-sdk-python/commit/ef58166e0fac68256ca8154792d2157698ed6a9d))
* **github:** include a devcontainer setup ([#216](https://github.com/anthropics/anthropic-sdk-python/issues/216)) ([c9fee19](https://github.com/anthropics/anthropic-sdk-python/commit/c9fee192863fa5f894035ce3e1cf52a78b56895d))
* **package:** add classifiers ([#214](https://github.com/anthropics/anthropic-sdk-python/issues/214)) ([380967e](https://github.com/anthropics/anthropic-sdk-python/commit/380967e515279482e7a93570f172f52324f8aa26))


### Bug Fixes

* **binaries:** don't synchronously block in astream_to_file ([#219](https://github.com/anthropics/anthropic-sdk-python/issues/219)) ([2a2a617](https://github.com/anthropics/anthropic-sdk-python/commit/2a2a617d6862eb83b8a671acad08825c3a20d11b))
* prevent TypeError in Python 3.8 (ABC is not subscriptable) ([#221](https://github.com/anthropics/anthropic-sdk-python/issues/221)) ([893e885](https://github.com/anthropics/anthropic-sdk-python/commit/893e885859b5fb94d7673bfa9ad0a04434fec196))


### Chores

* **docs:** fix github links ([#225](https://github.com/anthropics/anthropic-sdk-python/issues/225)) ([dfa9935](https://github.com/anthropics/anthropic-sdk-python/commit/dfa99352291b15b8c885eb558c8b738b26d33373))
* **internal:** fix some typos ([#223](https://github.com/anthropics/anthropic-sdk-python/issues/223)) ([9038193](https://github.com/anthropics/anthropic-sdk-python/commit/9038193db52612f756194fd735aab899bed0931f))
* **internal:** improve github devcontainer setup ([#226](https://github.com/anthropics/anthropic-sdk-python/issues/226)) ([3cd90ab](https://github.com/anthropics/anthropic-sdk-python/commit/3cd90abe2c57375438a4209e31253f758f408b17))
* **internal:** minor restructuring of base client ([#213](https://github.com/anthropics/anthropic-sdk-python/issues/213)) ([60dc609](https://github.com/anthropics/anthropic-sdk-python/commit/60dc609aa9c4b01b88d9c7e8d1eb35bf9561f210))
* **internal:** remove unused int/float conversion ([#220](https://github.com/anthropics/anthropic-sdk-python/issues/220)) ([a6bf20d](https://github.com/anthropics/anthropic-sdk-python/commit/a6bf20d8cb64f13618c3122f8285d240840884f8))
* **internal:** require explicit overrides ([#210](https://github.com/anthropics/anthropic-sdk-python/issues/210)) ([72f4339](https://github.com/anthropics/anthropic-sdk-python/commit/72f4339749f144e75e0e7dc0a7b2bb26f728044e))


### Documentation

* fix github links ([#215](https://github.com/anthropics/anthropic-sdk-python/issues/215)) ([8cbed15](https://github.com/anthropics/anthropic-sdk-python/commit/8cbed150d6e8f6ac8de8962e169ca46cdd0643c5))
* improve to dictionary example ([#207](https://github.com/anthropics/anthropic-sdk-python/issues/207)) ([5e32c20](https://github.com/anthropics/anthropic-sdk-python/commit/5e32c201f7017c2d4aa7416d1a7de3f0c5247fcc))

## 0.5.1 (2023-10-20)

Full Changelog: [v0.5.0...v0.5.1](https://github.com/anthropics/anthropic-sdk-python/compare/v0.5.0...v0.5.1)

### Chores

* **internal:** bump mypy ([#203](https://github.com/anthropics/anthropic-sdk-python/issues/203)) ([aa9a67e](https://github.com/anthropics/anthropic-sdk-python/commit/aa9a67e9286146e088af74ded73e3b4d6dde9c7b))
* **internal:** bump pyright ([#202](https://github.com/anthropics/anthropic-sdk-python/issues/202)) ([f96f5f7](https://github.com/anthropics/anthropic-sdk-python/commit/f96f5f75e4b54481bceb033f432f2911355f02e4))
* **internal:** update gitignore ([#199](https://github.com/anthropics/anthropic-sdk-python/issues/199)) ([b92fa57](https://github.com/anthropics/anthropic-sdk-python/commit/b92fa57ac997d80166dd758e1bc9bb58b217c572))

## 0.5.0 (2023-10-18)

Full Changelog: [v0.4.1...v0.5.0](https://github.com/anthropics/anthropic-sdk-python/compare/v0.4.1...v0.5.0)

### Features

* **client:** support passing httpx.URL instances to base_url ([#197](https://github.com/anthropics/anthropic-sdk-python/issues/197)) ([fe61308](https://github.com/anthropics/anthropic-sdk-python/commit/fe61308baa7d11993e72b3a282633a24fb4e61e4))


### Chores

* **internal:** improve publish script ([#196](https://github.com/anthropics/anthropic-sdk-python/issues/196)) ([7c92b90](https://github.com/anthropics/anthropic-sdk-python/commit/7c92b90864f9510e7cbb68c6b703eec7fd4b7b28))
* **internal:** migrate from Poetry to Rye ([#194](https://github.com/anthropics/anthropic-sdk-python/issues/194)) ([1dd605e](https://github.com/anthropics/anthropic-sdk-python/commit/1dd605e7daf6f8542cb0ff5f5af4f161153f239a))
* **internal:** update gitignore ([#198](https://github.com/anthropics/anthropic-sdk-python/issues/198)) ([4c210b7](https://github.com/anthropics/anthropic-sdk-python/commit/4c210b75ce9fee9a781fbcbab8711409de2d9eea))

## 0.4.1 (2023-10-16)

Full Changelog: [v0.4.0...v0.4.1](https://github.com/anthropics/anthropic-sdk-python/compare/v0.4.0...v0.4.1)

### Bug Fixes

* **client:** accept io.IOBase instances in file params ([#190](https://github.com/anthropics/anthropic-sdk-python/issues/190)) ([5da5f0c](https://github.com/anthropics/anthropic-sdk-python/commit/5da5f0cbfddfc04fc3b1c86dcbd04aa9d5f1b1e4))
* **streaming:** add additional overload for ambiguous stream param ([#185](https://github.com/anthropics/anthropic-sdk-python/issues/185)) ([794dc4d](https://github.com/anthropics/anthropic-sdk-python/commit/794dc4daa1c7ccea4157eed725e47409fe7f23dc))


### Chores

* **internal:** cleanup some redundant code ([#188](https://github.com/anthropics/anthropic-sdk-python/issues/188)) ([cb0bd8c](https://github.com/anthropics/anthropic-sdk-python/commit/cb0bd8c4e7f311c547674ee3c39dec23829e9422))
* **internal:** enable lint rule ([#187](https://github.com/anthropics/anthropic-sdk-python/issues/187)) ([123b5c1](https://github.com/anthropics/anthropic-sdk-python/commit/123b5c196ef87b4293fb5cbee2c6f3e6da739df8))


### Documentation

* organisation -&gt; organization (UK to US English) ([#192](https://github.com/anthropics/anthropic-sdk-python/issues/192)) ([901a330](https://github.com/anthropics/anthropic-sdk-python/commit/901a33004bcf9d2ff10c742924a70a919ae1cfef))

## 0.4.0 (2023-10-13)

Full Changelog: [v0.3.14...v0.4.0](https://github.com/anthropics/anthropic-sdk-python/compare/v0.3.14...v0.4.0)

### Features

* **client:** add logging setup ([#177](https://github.com/anthropics/anthropic-sdk-python/issues/177)) ([a5f87ad](https://github.com/anthropics/anthropic-sdk-python/commit/a5f87ad433ab8332b7c253160bedba0adcc2b3e2))


### Bug Fixes

* **client:** correctly handle arguments with env vars ([#178](https://github.com/anthropics/anthropic-sdk-python/issues/178)) ([91a0e2a](https://github.com/anthropics/anthropic-sdk-python/commit/91a0e2a9e436f47f46e36c7072c917a62a08ce16))


### Chores

* add case insensitive get header function ([#182](https://github.com/anthropics/anthropic-sdk-python/issues/182)) ([708fd02](https://github.com/anthropics/anthropic-sdk-python/commit/708fd027b113911f2e1801c4213f6700a9399aa7))
* update comment ([#183](https://github.com/anthropics/anthropic-sdk-python/issues/183)) ([649d6f4](https://github.com/anthropics/anthropic-sdk-python/commit/649d6f468a09648e91ae69cbc07420f055029edf))
* update README ([#174](https://github.com/anthropics/anthropic-sdk-python/issues/174)) ([bb581b5](https://github.com/anthropics/anthropic-sdk-python/commit/bb581b585e776dee50d05f3fcd2853483c3c2ac1))


### Documentation

* minor readme reordering ([#180](https://github.com/anthropics/anthropic-sdk-python/issues/180)) ([92345e3](https://github.com/anthropics/anthropic-sdk-python/commit/92345e31eca3036ab571c57f8c76424a578b55f4))


### Refactors

* **test:** refactor authentication tests ([#175](https://github.com/anthropics/anthropic-sdk-python/issues/175)) ([c82da53](https://github.com/anthropics/anthropic-sdk-python/commit/c82da53502dbb884fc92f1da094a968c9237927b))

## 0.3.14 (2023-10-11)

Full Changelog: [v0.3.13...v0.3.14](https://github.com/anthropics/anthropic-sdk-python/compare/v0.3.13...v0.3.14)

### Features

* **client:** add forwards-compatible pydantic methods ([#171](https://github.com/anthropics/anthropic-sdk-python/issues/171)) ([4c5289e](https://github.com/anthropics/anthropic-sdk-python/commit/4c5289eb8519ca9a53e9483422237aa25944f8d8))
* **client:** add support for passing in a httpx client ([#173](https://github.com/anthropics/anthropic-sdk-python/issues/173)) ([25046c4](https://github.com/anthropics/anthropic-sdk-python/commit/25046c4fbc6f9d343e3b1f21024cf3982ac48c35))
* **client:** handle retry-after header with a date format ([#168](https://github.com/anthropics/anthropic-sdk-python/issues/168)) ([afeabf1](https://github.com/anthropics/anthropic-sdk-python/commit/afeabf13aa5795a7fadd141e53ec81eadbce099a))
* **client:** retry on 408 Request Timeout ([#155](https://github.com/anthropics/anthropic-sdk-python/issues/155)) ([46386f8](https://github.com/anthropics/anthropic-sdk-python/commit/46386f8f60223f45bc133ddfcfda8d9ca9da26a8))
* **package:** export a root error type ([#163](https://github.com/anthropics/anthropic-sdk-python/issues/163)) ([e7aa3e7](https://github.com/anthropics/anthropic-sdk-python/commit/e7aa3e7785ae511fa35a68ac72079a6230ca84f3))
* **types:** improve params type names ([#160](https://github.com/anthropics/anthropic-sdk-python/issues/160)) ([43544a6](https://github.com/anthropics/anthropic-sdk-python/commit/43544a62c8410061c1a50282f4c45d029db7779b))


### Bug Fixes

* **client:** don't error by default for unexpected content types ([#161](https://github.com/anthropics/anthropic-sdk-python/issues/161)) ([76cfcf9](https://github.com/anthropics/anthropic-sdk-python/commit/76cfcf91172f9804056a7d5c1ec99666ad5991a2))
* **client:** properly configure model set fields ([#154](https://github.com/anthropics/anthropic-sdk-python/issues/154)) ([da6ccb1](https://github.com/anthropics/anthropic-sdk-python/commit/da6ccb10a38e862153871a540cb75af0afdaefb3))


### Chores

* **internal:** add helpers ([#156](https://github.com/anthropics/anthropic-sdk-python/issues/156)) ([00f5a19](https://github.com/anthropics/anthropic-sdk-python/commit/00f5a19c9393f6238759faea40405e60b2054da3))
* **internal:** move error classes from _base_exceptions to _exceptions (⚠️ breaking) ([#162](https://github.com/anthropics/anthropic-sdk-python/issues/162)) ([329b307](https://github.com/anthropics/anthropic-sdk-python/commit/329b307c205435d367c0d4b29b252be807c61c68))
* **tests:** improve raw response test ([#166](https://github.com/anthropics/anthropic-sdk-python/issues/166)) ([8042473](https://github.com/anthropics/anthropic-sdk-python/commit/8042473bd73faa0b819c27a68bfc19b918361461))


### Documentation

* add some missing inline documentation ([#151](https://github.com/anthropics/anthropic-sdk-python/issues/151)) ([1f98257](https://github.com/anthropics/anthropic-sdk-python/commit/1f9825775d58ed8a62b000caaddd622ed4ba3fd2))
* update readme ([#172](https://github.com/anthropics/anthropic-sdk-python/issues/172)) ([351095b](https://github.com/anthropics/anthropic-sdk-python/commit/351095b189b111a74e9e1825ce5b6da6673a1635))

## 0.3.13 (2023-09-11)

Full Changelog: [v0.3.12...v0.3.13](https://github.com/anthropics/anthropic-sdk-python/compare/v0.3.12...v0.3.13)

### Features

* **types:** de-duplicate nested streaming params types ([#141](https://github.com/anthropics/anthropic-sdk-python/issues/141)) ([f76f053](https://github.com/anthropics/anthropic-sdk-python/commit/f76f05320df3059d57ed57153f30be3a8d91fddf))


### Bug Fixes

* **client:** properly handle optional file params ([#142](https://github.com/anthropics/anthropic-sdk-python/issues/142)) ([11196b7](https://github.com/anthropics/anthropic-sdk-python/commit/11196b757c4ef334f8b6db069ecfc6a57c200389))


### Chores

* **internal:** add `pydantic.generics` import for compatibility ([#135](https://github.com/anthropics/anthropic-sdk-python/issues/135)) ([951446d](https://github.com/anthropics/anthropic-sdk-python/commit/951446dbd48e0e5b674fd988865f3aef60c86720))
* **internal:** minor restructuring ([#137](https://github.com/anthropics/anthropic-sdk-python/issues/137)) ([e601206](https://github.com/anthropics/anthropic-sdk-python/commit/e60120670adbc404b06b0fef9e40134929bc7bbd))
* **internal:** minor update ([#145](https://github.com/anthropics/anthropic-sdk-python/issues/145)) ([6a505ef](https://github.com/anthropics/anthropic-sdk-python/commit/6a505ef95523b725a8fdcba71faf9719292e5085))
* **internal:** update base client ([#143](https://github.com/anthropics/anthropic-sdk-python/issues/143)) ([8e0dca4](https://github.com/anthropics/anthropic-sdk-python/commit/8e0dca4fe290833f2aa8b25d6c80b0154ea2a703))
* **internal:** update lock file ([#147](https://github.com/anthropics/anthropic-sdk-python/issues/147)) ([a72b5ca](https://github.com/anthropics/anthropic-sdk-python/commit/a72b5ca4caa8963961d97e5d689393953e00c49b))
* **internal:** update pyright ([#149](https://github.com/anthropics/anthropic-sdk-python/issues/149)) ([9661f94](https://github.com/anthropics/anthropic-sdk-python/commit/9661f941ede82f0023c47b0d9c9beacbd5bbb703))
* **internal:** updates ([#148](https://github.com/anthropics/anthropic-sdk-python/issues/148)) ([9f7fbbc](https://github.com/anthropics/anthropic-sdk-python/commit/9f7fbbcd36ed2accb3a59275255f84200ab17b66))


### Documentation

* **readme:** add link to api.md ([#146](https://github.com/anthropics/anthropic-sdk-python/issues/146)) ([1fcb30a](https://github.com/anthropics/anthropic-sdk-python/commit/1fcb30ae85153d4ab34935a86dcaf0d0fc4470e9))
* **readme:** reference pydantic helpers ([#138](https://github.com/anthropics/anthropic-sdk-python/issues/138)) ([ccaab99](https://github.com/anthropics/anthropic-sdk-python/commit/ccaab990df18404db636f206575ed0548e9420e9))

## 0.3.12 (2023-08-29)

Full Changelog: [v0.3.11...v0.3.12](https://github.com/anthropics/anthropic-sdk-python/compare/v0.3.11...v0.3.12)

### Chores

* **ci:** setup workflows to create releases and release PRs ([#130](https://github.com/anthropics/anthropic-sdk-python/issues/130)) ([8f1048b](https://github.com/anthropics/anthropic-sdk-python/commit/8f1048b0f25116ecf4cdedec651a5f8f38fe0d72))
* **internal:** use shared params references ([#133](https://github.com/anthropics/anthropic-sdk-python/issues/133)) ([feaf6aa](https://github.com/anthropics/anthropic-sdk-python/commit/feaf6aa84e83a12e2bd51d78141c2626bfd228e6))

## [0.3.11](https://github.com/anthropics/anthropic-sdk-python/compare/v0.3.10...v0.3.11) (2023-08-26)


### Documentation

* **readme:** make print statements in streaming examples flush ([#123](https://github.com/anthropics/anthropic-sdk-python/issues/123)) ([d24dfaf](https://github.com/anthropics/anthropic-sdk-python/commit/d24dfaffbfd7e82c20c7d846eeddd2af1404e26b))


### Chores

* **internal:** update anyio ([#125](https://github.com/anthropics/anthropic-sdk-python/issues/125)) ([34c7fa1](https://github.com/anthropics/anthropic-sdk-python/commit/34c7fa16006cb2842ccc59c416441b930ed855e7))

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
