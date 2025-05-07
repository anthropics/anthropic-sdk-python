# Changelog

## 0.51.0 (2025-05-07)

Full Changelog: [v0.50.0...v0.51.0](https://github.com/anthropics/anthropic-sdk-python/compare/v0.50.0...v0.51.0)

### Features

* **api:** adds web search capabilities to the Claude API ([bec0cf9](https://github.com/anthropics/anthropic-sdk-python/commit/bec0cf93c2d7cb47c921236a14c8569e0e22793e))


### Bug Fixes

* **pydantic v1:** more robust ModelField.annotation check ([c50f406](https://github.com/anthropics/anthropic-sdk-python/commit/c50f406767d8e7737a2754d6e1488d8a19216ac0))
* **sockets:** handle non-portable socket flags ([#935](https://github.com/anthropics/anthropic-sdk-python/issues/935)) ([205c8dd](https://github.com/anthropics/anthropic-sdk-python/commit/205c8dda371caa3b393d3cfb4d323714b1fab336))


### Chores

* broadly detect json family of content-type headers ([66bbb3a](https://github.com/anthropics/anthropic-sdk-python/commit/66bbb3a6689a4e2dd4915a7a2940dec53e2b8eb9))
* **ci:** only use depot for staging repos ([c867a11](https://github.com/anthropics/anthropic-sdk-python/commit/c867a11af37416c0d513aa177f77e1bcd0d70949))
* **ci:** run on more branches and use depot runners ([95f5f17](https://github.com/anthropics/anthropic-sdk-python/commit/95f5f17be0ab05ed4e258ccc488d8cf55ffb8f29))
* **internal:** add back missing custom modifications for Web Search ([f43ba69](https://github.com/anthropics/anthropic-sdk-python/commit/f43ba69d5337e5d99f7ca9bd2e773cc57bae5d1c))
* **internal:** minor formatting changes ([8afef08](https://github.com/anthropics/anthropic-sdk-python/commit/8afef086af194df1e4b0d6d25b7fbe4d74bd6850))
* use lazy imports for resources ([704be81](https://github.com/anthropics/anthropic-sdk-python/commit/704be817f436d92d96915cf02608b6827e06945f))

## 0.50.0 (2025-04-22)

Full Changelog: [v0.49.0...v0.50.0](https://github.com/anthropics/anthropic-sdk-python/compare/v0.49.0...v0.50.0)

### Features

* **api:** extract ContentBlockDelta events into their own schemas ([#920](https://github.com/anthropics/anthropic-sdk-python/issues/920)) ([ae773d6](https://github.com/anthropics/anthropic-sdk-python/commit/ae773d673a7d3cbb28eebce0df9c526f1e855435))
* **api:** manual updates ([46ac1f8](https://github.com/anthropics/anthropic-sdk-python/commit/46ac1f8d1cfa21fbe9df4545d748211c0f3c10e0))
* **api:** manual updates ([48d9739](https://github.com/anthropics/anthropic-sdk-python/commit/48d9739ad741c72d6ecab5200ca53151a604416f))
* **api:** manual updates ([66e8cc3](https://github.com/anthropics/anthropic-sdk-python/commit/66e8cc3fb207a889b1df1028db73291b9800f8f9))
* **api:** manual updates ([a74746e](https://github.com/anthropics/anthropic-sdk-python/commit/a74746e0df0b3c9b85a42e95a80c1db763379e1b))


### Bug Fixes

* **ci:** ensure pip is always available ([#907](https://github.com/anthropics/anthropic-sdk-python/issues/907)) ([3632687](https://github.com/anthropics/anthropic-sdk-python/commit/36326871c1304fbb1dad56e3e5bc71659bbf0df1))
* **ci:** remove publishing patch ([#908](https://github.com/anthropics/anthropic-sdk-python/issues/908)) ([cae0323](https://github.com/anthropics/anthropic-sdk-python/commit/cae032381bd73e86174b5fde2efaf046e96f5e6a))
* **client:** deduplicate stop reason type ([#913](https://github.com/anthropics/anthropic-sdk-python/issues/913)) ([3ab0194](https://github.com/anthropics/anthropic-sdk-python/commit/3ab0194550aa9893cc948c3d658a965817d64ccd))
* **client:** send all configured auth headers ([#929](https://github.com/anthropics/anthropic-sdk-python/issues/929)) ([9d2581e](https://github.com/anthropics/anthropic-sdk-python/commit/9d2581e79f31effb34958e633b59b19aa3681875))
* **perf:** optimize some hot paths ([cff76cb](https://github.com/anthropics/anthropic-sdk-python/commit/cff76cb00ba0b7839141d84d1f751516a11240c3))
* **perf:** skip traversing types for NotGiven values ([dadac7f](https://github.com/anthropics/anthropic-sdk-python/commit/dadac7fa7207bef547db39b9003a46512a945a78))
* **project:** bump httpx minimum version to 0.25.0 ([b554138](https://github.com/anthropics/anthropic-sdk-python/commit/b554138c2f5d73dd915092972411f7ab787cfe42)), closes [#902](https://github.com/anthropics/anthropic-sdk-python/issues/902)
* **types:** handle more discriminated union shapes ([#906](https://github.com/anthropics/anthropic-sdk-python/issues/906)) ([2fc179a](https://github.com/anthropics/anthropic-sdk-python/commit/2fc179a4d29b720263e84c90f37d078ffab860ad))
* **vertex:** explicitly include requests extra ([2b1221b](https://github.com/anthropics/anthropic-sdk-python/commit/2b1221b76bfcc0dfaa14d94e7f6a3ddc303f3715))


### Chores

* add hash of OpenAPI spec/config inputs to .stats.yml ([#912](https://github.com/anthropics/anthropic-sdk-python/issues/912)) ([ddf7835](https://github.com/anthropics/anthropic-sdk-python/commit/ddf78352c9e589f6102f9373cc01bee9333d15d8))
* **ci:** add timeout thresholds for CI jobs ([7226a5c](https://github.com/anthropics/anthropic-sdk-python/commit/7226a5ccef181041fcea0fffcbc0ed395a700df3))
* **client:** minor internal fixes ([99b9a38](https://github.com/anthropics/anthropic-sdk-python/commit/99b9a387c60347471763c9970f7767ecd4cc04d1))
* **internal:** add back release workflow ([ce18972](https://github.com/anthropics/anthropic-sdk-python/commit/ce189722eefedc794111899d54048bddaa82d17d))
* **internal:** base client updates ([2e08c71](https://github.com/anthropics/anthropic-sdk-python/commit/2e08c714cebd4a7df87f80902220b1502d371d04))
* **internal:** bump pyright version ([d9ea30e](https://github.com/anthropics/anthropic-sdk-python/commit/d9ea30ead2cf76676a3b3ac0181a1616afe8323b))
* **internal:** bump rye to 0.44.0 ([#905](https://github.com/anthropics/anthropic-sdk-python/issues/905)) ([e1a1b14](https://github.com/anthropics/anthropic-sdk-python/commit/e1a1b142c8f385d288cf5395917e6380add556ea))
* **internal:** expand CI branch coverage ([#934](https://github.com/anthropics/anthropic-sdk-python/issues/934)) ([b23fdc9](https://github.com/anthropics/anthropic-sdk-python/commit/b23fdc940d5a8eff35746b39a59678e8c633c289))
* **internal:** fix list file params ([cfbaaf9](https://github.com/anthropics/anthropic-sdk-python/commit/cfbaaf9650a963cf15febb4d141f40f18b37c2ef))
* **internal:** import ordering changes ([#895](https://github.com/anthropics/anthropic-sdk-python/issues/895)) ([b8da2f7](https://github.com/anthropics/anthropic-sdk-python/commit/b8da2f748f478fc83c5f13f1d0dcd2eaf85922e0))
* **internal:** import reformatting ([5e6cd74](https://github.com/anthropics/anthropic-sdk-python/commit/5e6cd74bc383b812698b2d572ff9b016aae94b5e))
* **internal:** reduce CI branch coverage ([07e813f](https://github.com/anthropics/anthropic-sdk-python/commit/07e813f9c1873c5addc1d2adacdb387e8db5f3da))
* **internal:** refactor retries to not use recursion ([4354e82](https://github.com/anthropics/anthropic-sdk-python/commit/4354e82dc891cfa973d056aabada54f461979d2c))
* **internal:** remove CI condition ([#916](https://github.com/anthropics/anthropic-sdk-python/issues/916)) ([043b56b](https://github.com/anthropics/anthropic-sdk-python/commit/043b56b9772d49965cdeec649f2b6c7bdf0249a5))
* **internal:** remove extra empty newlines ([#904](https://github.com/anthropics/anthropic-sdk-python/issues/904)) ([cfe8f6e](https://github.com/anthropics/anthropic-sdk-python/commit/cfe8f6e4e1a5be51a2bd7ced23258b4159564ae7))
* **internal:** remove trailing character ([#924](https://github.com/anthropics/anthropic-sdk-python/issues/924)) ([dc8e781](https://github.com/anthropics/anthropic-sdk-python/commit/dc8e7816a9e8cae3f4f8ccf4b9723f9093b3f05e))
* **internal:** remove unused http client options forwarding ([#890](https://github.com/anthropics/anthropic-sdk-python/issues/890)) ([e0428bf](https://github.com/anthropics/anthropic-sdk-python/commit/e0428bfdffb6adb2e21c6ca365a26816eb699006))
* **internal:** slight transform perf improvement ([#931](https://github.com/anthropics/anthropic-sdk-python/issues/931)) ([3ed4e5e](https://github.com/anthropics/anthropic-sdk-python/commit/3ed4e5eebb7bc5d42c6888cda0388c84ce74fa12))
* **internal:** update config ([#914](https://github.com/anthropics/anthropic-sdk-python/issues/914)) ([a697234](https://github.com/anthropics/anthropic-sdk-python/commit/a697234637b84b2a488309bdb851db2efe17190c))
* **internal:** update models test ([b1e031d](https://github.com/anthropics/anthropic-sdk-python/commit/b1e031dfee560629007dab1120872ca489e1e6c2))
* **internal:** update pyright settings ([38bdc6c](https://github.com/anthropics/anthropic-sdk-python/commit/38bdc6cd3436734f29a39b3e4b2c011733a4c0d3))
* **internal:** variable name and test updates ([#925](https://github.com/anthropics/anthropic-sdk-python/issues/925)) ([f5d0809](https://github.com/anthropics/anthropic-sdk-python/commit/f5d08095216744373f1b5d25f65873ca674796e8))
* **tests:** improve enum examples ([#932](https://github.com/anthropics/anthropic-sdk-python/issues/932)) ([808aaf3](https://github.com/anthropics/anthropic-sdk-python/commit/808aaf32d77ab82e79bb8e37c0cb371403726be1))
* **vertex:** improve error message when missing extra ([15dc4cb](https://github.com/anthropics/anthropic-sdk-python/commit/15dc4cb5297304420fd1d7be8e87697bf60d8b2d))


### Documentation

* revise readme docs about nested params ([#900](https://github.com/anthropics/anthropic-sdk-python/issues/900)) ([0f80ab0](https://github.com/anthropics/anthropic-sdk-python/commit/0f80ab0ffcd5c2d854f01364b1cfe2517e04b40b))
* swap examples used in readme ([#928](https://github.com/anthropics/anthropic-sdk-python/issues/928)) ([96ff1c7](https://github.com/anthropics/anthropic-sdk-python/commit/96ff1c7b6a09907c33def5afd9f61bb597e897b1))

## 0.49.0 (2025-02-28)

Full Changelog: [v0.48.0...v0.49.0](https://github.com/anthropics/anthropic-sdk-python/compare/v0.48.0...v0.49.0)

### Features

* **api:** add support for disabling tool calls ([#888](https://github.com/anthropics/anthropic-sdk-python/issues/888)) ([bfde3d2](https://github.com/anthropics/anthropic-sdk-python/commit/bfde3d2978f78ee43db351a78fe1b078eb073394))


### Chores

* **docs:** update client docstring ([#887](https://github.com/anthropics/anthropic-sdk-python/issues/887)) ([4d3ec5e](https://github.com/anthropics/anthropic-sdk-python/commit/4d3ec5ec5b9c9aabb7cc7f27345809c347c56d89))


### Documentation

* update URLs from stainlessapi.com to stainless.com ([#885](https://github.com/anthropics/anthropic-sdk-python/issues/885)) ([312364b](https://github.com/anthropics/anthropic-sdk-python/commit/312364b9b5025ba16f0081e6e53b478c3a4fb089))

## 0.48.0 (2025-02-27)

Full Changelog: [v0.47.2...v0.48.0](https://github.com/anthropics/anthropic-sdk-python/compare/v0.47.2...v0.48.0)

### Features

* **api:** add URL source blocks for images and PDFs ([#884](https://github.com/anthropics/anthropic-sdk-python/issues/884)) ([e6b3a70](https://github.com/anthropics/anthropic-sdk-python/commit/e6b3a70ffbd830a8bdd87c0938897eebc6d5ee33))


### Documentation

* add thinking examples ([f463248](https://github.com/anthropics/anthropic-sdk-python/commit/f46324863dabe4efc4adec7361be5d6888fe4dd5))

## 0.47.2 (2025-02-25)

Full Changelog: [v0.47.1...v0.47.2](https://github.com/anthropics/anthropic-sdk-python/compare/v0.47.1...v0.47.2)

### Bug Fixes

* **beta:** add thinking to beta.messages.stream ([69e3db1](https://github.com/anthropics/anthropic-sdk-python/commit/69e3db1de0c584c06ac450cc181144abc1602f13))


### Chores

* **internal:** properly set __pydantic_private__ ([#879](https://github.com/anthropics/anthropic-sdk-python/issues/879)) ([3537a3b](https://github.com/anthropics/anthropic-sdk-python/commit/3537a3bb229412bcd89e79bfda45e89727187244))

## 0.47.1 (2025-02-24)

Full Changelog: [v0.47.0...v0.47.1](https://github.com/anthropics/anthropic-sdk-python/compare/v0.47.0...v0.47.1)

### Chores

* **internal:** update spec ([#871](https://github.com/anthropics/anthropic-sdk-python/issues/871)) ([916be18](https://github.com/anthropics/anthropic-sdk-python/commit/916be1806d3a86ec5abaef7c00227cd918b92274))
* update large max_tokens error message ([40c71df](https://github.com/anthropics/anthropic-sdk-python/commit/40c71df4b6e7760648f42a5f0995bcc93dafbd17))

## 0.47.0 (2025-02-24)

Full Changelog: [v0.46.0...v0.47.0](https://github.com/anthropics/anthropic-sdk-python/compare/v0.46.0...v0.47.0)

### Features

* **api:** add claude-3.7 + support for thinking ([c5387e6](https://github.com/anthropics/anthropic-sdk-python/commit/c5387e69e799f14e44006ea4e54fdf32f2f74393))
* **client:** add more status exceptions ([#854](https://github.com/anthropics/anthropic-sdk-python/issues/854)) ([00d9512](https://github.com/anthropics/anthropic-sdk-python/commit/00d95126aff50158c7849d651c35a88ea81ff969))
* **client:** allow passing `NotGiven` for body ([#868](https://github.com/anthropics/anthropic-sdk-python/issues/868)) ([8ab445e](https://github.com/anthropics/anthropic-sdk-python/commit/8ab445e6a837854421f358f4977ff80c5e0635c8))


### Bug Fixes

* **client:** mark some request bodies as optional ([8ab445e](https://github.com/anthropics/anthropic-sdk-python/commit/8ab445e6a837854421f358f4977ff80c5e0635c8))


### Chores

* **internal:** fix devcontainers setup ([#870](https://github.com/anthropics/anthropic-sdk-python/issues/870)) ([1a21c6a](https://github.com/anthropics/anthropic-sdk-python/commit/1a21c6a3fb6969a07e9b8483ed116fb3af7bd3b2))

## 0.46.0 (2025-02-18)

Full Changelog: [v0.45.2...v0.46.0](https://github.com/anthropics/anthropic-sdk-python/compare/v0.45.2...v0.46.0)

### Features

* **client:** send `X-Stainless-Read-Timeout` header ([#858](https://github.com/anthropics/anthropic-sdk-python/issues/858)) ([0e75983](https://github.com/anthropics/anthropic-sdk-python/commit/0e759835ddfa7d72d0926cab0101601e7c1e8f22))
* **jsonl:** add .close() method ([#862](https://github.com/anthropics/anthropic-sdk-python/issues/862)) ([137335c](https://github.com/anthropics/anthropic-sdk-python/commit/137335c649f3dc886875bb60bddeb0c8d8abb67b))
* **pagination:** avoid fetching when has_more: false ([#860](https://github.com/anthropics/anthropic-sdk-python/issues/860)) ([0cdb81d](https://github.com/anthropics/anthropic-sdk-python/commit/0cdb81d106c48c851fff5c9532c675b414f474b4))


### Bug Fixes

* asyncify on non-asyncio runtimes ([#864](https://github.com/anthropics/anthropic-sdk-python/issues/864)) ([f92b36d](https://github.com/anthropics/anthropic-sdk-python/commit/f92b36d4a87c6b5455945ce38e3ab3db24e9a529))
* **internal:** add back custom header naming support ([#861](https://github.com/anthropics/anthropic-sdk-python/issues/861)) ([cf851ae](https://github.com/anthropics/anthropic-sdk-python/commit/cf851ae9ee57635250beec8bedb0134aa2d79a42))
* **jsonl:** lower chunk size ([#863](https://github.com/anthropics/anthropic-sdk-python/issues/863)) ([38fb720](https://github.com/anthropics/anthropic-sdk-python/commit/38fb72043b436afc02839ad4e2a966a5ef0b0bc1))


### Chores

* **api:** update openapi spec url ([#852](https://github.com/anthropics/anthropic-sdk-python/issues/852)) ([461d821](https://github.com/anthropics/anthropic-sdk-python/commit/461d821965c61d98bf35a8b6fab5da55a2ddddef))
* **internal:** bummp ruff dependency ([#856](https://github.com/anthropics/anthropic-sdk-python/issues/856)) ([590c3fa](https://github.com/anthropics/anthropic-sdk-python/commit/590c3fa154e38f85c3cc6fcc518a6c68ee2bd234))
* **internal:** change default timeout to an int ([#855](https://github.com/anthropics/anthropic-sdk-python/issues/855)) ([3152e1a](https://github.com/anthropics/anthropic-sdk-python/commit/3152e1a135a07430404f3209fbbcb924d9d2b9a2))
* **internal:** fix tests ([fc41ba2](https://github.com/anthropics/anthropic-sdk-python/commit/fc41ba21b492e864685384e82b3eeca1ca56f4eb))
* **internal:** fix type traversing dictionary params ([#859](https://github.com/anthropics/anthropic-sdk-python/issues/859)) ([c5b700d](https://github.com/anthropics/anthropic-sdk-python/commit/c5b700d9abea1fcebc43fe12ac514512fedff0db))
* **internal:** reorder model constants ([#847](https://github.com/anthropics/anthropic-sdk-python/issues/847)) ([aadd531](https://github.com/anthropics/anthropic-sdk-python/commit/aadd5315868ce2eec17cc7d0e8ec4f0b6a4c3c87))
* **internal:** update models used in tests ([aadd531](https://github.com/anthropics/anthropic-sdk-python/commit/aadd5315868ce2eec17cc7d0e8ec4f0b6a4c3c87))

## 0.45.2 (2025-01-27)

Full Changelog: [v0.45.1...v0.45.2](https://github.com/anthropics/anthropic-sdk-python/compare/v0.45.1...v0.45.2)

### Bug Fixes

* **streaming:** avoid invalid deser type error ([#845](https://github.com/anthropics/anthropic-sdk-python/issues/845)) ([72a2585](https://github.com/anthropics/anthropic-sdk-python/commit/72a2585680a4cc5d007bf93935424dbc4cecf2bd))

## 0.45.1 (2025-01-27)

Full Changelog: [v0.45.0...v0.45.1](https://github.com/anthropics/anthropic-sdk-python/compare/v0.45.0...v0.45.1)

### Bug Fixes

* **streaming:** accumulate citations ([#844](https://github.com/anthropics/anthropic-sdk-python/issues/844)) ([e665f2f](https://github.com/anthropics/anthropic-sdk-python/commit/e665f2fefd4573fc45cd4c546a9480f15d18d1cd))


### Chores

* **docs:** updates ([#841](https://github.com/anthropics/anthropic-sdk-python/issues/841)) ([fb10a7d](https://github.com/anthropics/anthropic-sdk-python/commit/fb10a7d658044062e5023cd8495c80d3344af8df))

## 0.45.0 (2025-01-23)

Full Changelog: [v0.44.0...v0.45.0](https://github.com/anthropics/anthropic-sdk-python/compare/v0.44.0...v0.45.0)

### Features

* **api:** add citations ([#839](https://github.com/anthropics/anthropic-sdk-python/issues/839)) ([2ec74b6](https://github.com/anthropics/anthropic-sdk-python/commit/2ec74b6ff106c6e3d7d55e3c189e345098f8575e))
* **client:** support results endpoint ([#835](https://github.com/anthropics/anthropic-sdk-python/issues/835)) ([5dd88bf](https://github.com/anthropics/anthropic-sdk-python/commit/5dd88bf2d20b8909736cc0bc1e81296ba6e322a9))


### Chores

* **internal:** minor formatting changes ([#838](https://github.com/anthropics/anthropic-sdk-python/issues/838)) ([31eb826](https://github.com/anthropics/anthropic-sdk-python/commit/31eb826deb96a17d3c0bb953c728f39412c12ada))

## 0.44.0 (2025-01-21)

Full Changelog: [v0.43.1...v0.44.0](https://github.com/anthropics/anthropic-sdk-python/compare/v0.43.1...v0.44.0)

### Features

* **streaming:** add request_id getter ([#831](https://github.com/anthropics/anthropic-sdk-python/issues/831)) ([fb397e0](https://github.com/anthropics/anthropic-sdk-python/commit/fb397e0851bd874a10a69a9531483fd196fc8a55))


### Bug Fixes

* **tests:** make test_get_platform less flaky ([#830](https://github.com/anthropics/anthropic-sdk-python/issues/830)) ([f2c10ca](https://github.com/anthropics/anthropic-sdk-python/commit/f2c10cae0cbff6881bba2a41c93efdcc17e8d2ab))


### Chores

* deprecate more models ([c647e25](https://github.com/anthropics/anthropic-sdk-python/commit/c647e25c3735e4276195ee8eb0011ace3e3e0d2f))
* **internal:** avoid pytest-asyncio deprecation warning ([#832](https://github.com/anthropics/anthropic-sdk-python/issues/832)) ([2b3ceff](https://github.com/anthropics/anthropic-sdk-python/commit/2b3ceff7ef9c953e28044442821069d7de3b0154))
* **internal:** minor style changes ([#833](https://github.com/anthropics/anthropic-sdk-python/issues/833)) ([65cfb7b](https://github.com/anthropics/anthropic-sdk-python/commit/65cfb7b13324e52e2d2987c4de3ed9e5c122a40b))


### Documentation

* **raw responses:** fix duplicate `the` ([#828](https://github.com/anthropics/anthropic-sdk-python/issues/828)) ([ff850f8](https://github.com/anthropics/anthropic-sdk-python/commit/ff850f8081a72090eaaa31e09e560acd3ce18b09))

## 0.43.1 (2025-01-17)

Full Changelog: [v0.43.0...v0.43.1](https://github.com/anthropics/anthropic-sdk-python/compare/v0.43.0...v0.43.1)

### Bug Fixes

* **docs:** correct results return type ([69ad511](https://github.com/anthropics/anthropic-sdk-python/commit/69ad5112596f6e9aaf5cd2d495cb57516f2afbd4))


### Chores

* **internal:** bump pyright dependency ([#822](https://github.com/anthropics/anthropic-sdk-python/issues/822)) ([f8ddb90](https://github.com/anthropics/anthropic-sdk-python/commit/f8ddb90112a432a750fd4123c747ca581cff54ab))
* **internal:** fix lint ([483cc27](https://github.com/anthropics/anthropic-sdk-python/commit/483cc277b66cb5b1a767e9d91347f22bcf69dc28))
* **streaming:** add runtime type check for better error messages ([#826](https://github.com/anthropics/anthropic-sdk-python/issues/826)) ([cf69e09](https://github.com/anthropics/anthropic-sdk-python/commit/cf69e091d230aa0befb6ace74e64357b1cf2e4cd))
* **types:** add more discriminator metadata ([#825](https://github.com/anthropics/anthropic-sdk-python/issues/825)) ([d0de8e5](https://github.com/anthropics/anthropic-sdk-python/commit/d0de8e564038cc6f801dc663b1938ac571ab47be))

## 0.43.0 (2025-01-14)

Full Changelog: [v0.42.0...v0.43.0](https://github.com/anthropics/anthropic-sdk-python/compare/v0.42.0...v0.43.0)

### Features

* **api:** add message batch delete endpoint ([#802](https://github.com/anthropics/anthropic-sdk-python/issues/802)) ([9cf1e99](https://github.com/anthropics/anthropic-sdk-python/commit/9cf1e9920d3e0ce8496859b119f19eed8cd75e2b))
* **beta:** add streaming helpers for beta messages ([#819](https://github.com/anthropics/anthropic-sdk-python/issues/819)) ([d913ba3](https://github.com/anthropics/anthropic-sdk-python/commit/d913ba35eb3a95e80154b9d35e4c0a9f4a8dfeb1))


### Bug Fixes

* **client:** only call .close() when needed ([#811](https://github.com/anthropics/anthropic-sdk-python/issues/811)) ([21e0eb3](https://github.com/anthropics/anthropic-sdk-python/commit/21e0eb3c2bb043814541c9dcb68498066be1fc78))
* correctly handle deserialising `cls` fields ([#817](https://github.com/anthropics/anthropic-sdk-python/issues/817)) ([60e56a5](https://github.com/anthropics/anthropic-sdk-python/commit/60e56a5fb4413a97586df84c86765947b7ff92e5))
* **types:** allow extra properties in input schemas ([d0961c2](https://github.com/anthropics/anthropic-sdk-python/commit/d0961c2fcbe7370f145512facad8aab175798158))


### Chores

* add missing isclass check ([#806](https://github.com/anthropics/anthropic-sdk-python/issues/806)) ([1fc034d](https://github.com/anthropics/anthropic-sdk-python/commit/1fc034d784e9a8b30866a8058a4bd50ec2605fd3))
* bump testing data uri ([#800](https://github.com/anthropics/anthropic-sdk-python/issues/800)) ([641ae8d](https://github.com/anthropics/anthropic-sdk-python/commit/641ae8d412e365e44c8965222f487e30a63d57ee))
* **internal:** bump httpx dependency ([#809](https://github.com/anthropics/anthropic-sdk-python/issues/809)) ([7d678f1](https://github.com/anthropics/anthropic-sdk-python/commit/7d678f19b86ac1ad5d18ed47739d3df64187c843))
* **internal:** minor reformatting ([5a80668](https://github.com/anthropics/anthropic-sdk-python/commit/5a806684c4aaaf7d493bf9ef193e8031f7290b78))
* **internal:** update deps ([#820](https://github.com/anthropics/anthropic-sdk-python/issues/820)) ([32c3e1a](https://github.com/anthropics/anthropic-sdk-python/commit/32c3e1a63da74919dc0cb10a16b731afc2589cf5))
* **internal:** update examples ([#810](https://github.com/anthropics/anthropic-sdk-python/issues/810)) ([bb588ca](https://github.com/anthropics/anthropic-sdk-python/commit/bb588ca71a374b38797390c62bee66a0329c28a0))
* **vertex:** remove deprecated HTTP client options ([3f4eada](https://github.com/anthropics/anthropic-sdk-python/commit/3f4eada664421accec6f33a7ead44101323d0b14))
* **vertex:** remove deprecated HTTP client options ([c82f3e8](https://github.com/anthropics/anthropic-sdk-python/commit/c82f3e8ce16e8840cce94e023a82c596432f5c98))


### Documentation

* fix typos ([#812](https://github.com/anthropics/anthropic-sdk-python/issues/812)) ([8f46cae](https://github.com/anthropics/anthropic-sdk-python/commit/8f46cae8af228c9520bf95383afd1dce49198517))
* fix typos ([#813](https://github.com/anthropics/anthropic-sdk-python/issues/813)) ([ac44348](https://github.com/anthropics/anthropic-sdk-python/commit/ac443484c21e89bf0c491179613ae61709f87cb9))
* **readme:** fix misplaced period ([#816](https://github.com/anthropics/anthropic-sdk-python/issues/816)) ([4358226](https://github.com/anthropics/anthropic-sdk-python/commit/4358226929ffc3a7f1cb49489b7288ab870e636b))


### Refactors

* **stream:** make `MessageStream` wrap `Stream` directly ([#805](https://github.com/anthropics/anthropic-sdk-python/issues/805)) ([5669399](https://github.com/anthropics/anthropic-sdk-python/commit/56693993cce931fb0ae12d8890099069c4c95dff))
* **vertex:** remove deprecated HTTP client options ([#808](https://github.com/anthropics/anthropic-sdk-python/issues/808)) ([3f4eada](https://github.com/anthropics/anthropic-sdk-python/commit/3f4eada664421accec6f33a7ead44101323d0b14))

## 0.42.0 (2024-12-17)

Full Changelog: [v0.41.0...v0.42.0](https://github.com/anthropics/anthropic-sdk-python/compare/v0.41.0...v0.42.0)

### Features

* **api:** general availability updates ([#795](https://github.com/anthropics/anthropic-sdk-python/issues/795)) ([0954c48](https://github.com/anthropics/anthropic-sdk-python/commit/0954c488e64a8d80d2dfa160b0ffdd8366996d2e))


### Bug Fixes

* **vertex:** remove `anthropic_version` deletion for token counting ([f613929](https://github.com/anthropics/anthropic-sdk-python/commit/f613929150591e8927af590554e71f197fc243fc))


### Chores

* **internal:** fix some typos ([#799](https://github.com/anthropics/anthropic-sdk-python/issues/799)) ([45addb6](https://github.com/anthropics/anthropic-sdk-python/commit/45addb671fde3c7e06735fbd09fee278e0ddff18))

## 0.41.0 (2024-12-17)

Full Changelog: [v0.40.0...v0.41.0](https://github.com/anthropics/anthropic-sdk-python/compare/v0.40.0...v0.41.0)

### Features

* **api:** general availability updates ([5db8538](https://github.com/anthropics/anthropic-sdk-python/commit/5db8538cca2ab957ccb5460bf3f33636de0a5106))
* **api:** general availability updates ([#795](https://github.com/anthropics/anthropic-sdk-python/issues/795)) ([c8d5e43](https://github.com/anthropics/anthropic-sdk-python/commit/c8d5e43d00e0e68a68b9ecac15414135750495ff))
* **vertex:** support token counting ([6c3eded](https://github.com/anthropics/anthropic-sdk-python/commit/6c3ededeb68f878a94998d61d0c78209ec640d0c))


### Bug Fixes

* **internal:** correct support for TypeAliasType ([2f6ba9e](https://github.com/anthropics/anthropic-sdk-python/commit/2f6ba9e9f827b39b373a4b2904df04fef940001a))


### Chores

* **api:** update spec version ([#792](https://github.com/anthropics/anthropic-sdk-python/issues/792)) ([f54c1da](https://github.com/anthropics/anthropic-sdk-python/commit/f54c1daf964d0cca09e023bd89adf7d9c97f385d))
* **bedrock/vertex:** explicit error for unsupported messages endpoints ([c4cf816](https://github.com/anthropics/anthropic-sdk-python/commit/c4cf8164c20081cc75fefbe39db5b76be1c724e1))
* **internal:** add support for TypeAliasType ([#786](https://github.com/anthropics/anthropic-sdk-python/issues/786)) ([287ebd2](https://github.com/anthropics/anthropic-sdk-python/commit/287ebd2287ca90408999fe6be3b6f8c0295b46ef))
* **internal:** bump pydantic dependency ([#775](https://github.com/anthropics/anthropic-sdk-python/issues/775)) ([99b4d06](https://github.com/anthropics/anthropic-sdk-python/commit/99b4d06e73cdae3f2c97c304b8c0b64ec4758768))
* **internal:** bump pyright ([#769](https://github.com/anthropics/anthropic-sdk-python/issues/769)) ([81f7d70](https://github.com/anthropics/anthropic-sdk-python/commit/81f7d70fa85029f86de30ac1701ec39d01dde8f9))
* **internal:** bump pyright ([#785](https://github.com/anthropics/anthropic-sdk-python/issues/785)) ([44ab333](https://github.com/anthropics/anthropic-sdk-python/commit/44ab3339b7f3860e3a492a1784f247702bea5be0))
* **internal:** remove some duplicated imports ([#788](https://github.com/anthropics/anthropic-sdk-python/issues/788)) ([576ae9b](https://github.com/anthropics/anthropic-sdk-python/commit/576ae9b83214fd78fb02c420abfc0760270ffba8))
* **internal:** update spec ([#793](https://github.com/anthropics/anthropic-sdk-python/issues/793)) ([7cffc99](https://github.com/anthropics/anthropic-sdk-python/commit/7cffc992b17c475ceaef90868660c5a536e51624))
* **internal:** updated imports ([#789](https://github.com/anthropics/anthropic-sdk-python/issues/789)) ([d163c08](https://github.com/anthropics/anthropic-sdk-python/commit/d163c08caa9515fc5f59f284d236b16e7f0adb40))
* make the `Omit` type public ([#772](https://github.com/anthropics/anthropic-sdk-python/issues/772)) ([4ed0419](https://github.com/anthropics/anthropic-sdk-python/commit/4ed041961b59a7943b00a8e592ead0e962f36174))
* remove deprecated HTTP client options ([#777](https://github.com/anthropics/anthropic-sdk-python/issues/777)) ([3933368](https://github.com/anthropics/anthropic-sdk-python/commit/3933368e8a54d1f81c9503576e461c3d75292c39))


### Documentation

* **readme:** example snippet for client context manager ([#791](https://github.com/anthropics/anthropic-sdk-python/issues/791)) ([d0a5f0c](https://github.com/anthropics/anthropic-sdk-python/commit/d0a5f0c0568afcac5680d4c38943c8d634521c06))
* **readme:** fix http client proxies example ([#778](https://github.com/anthropics/anthropic-sdk-python/issues/778)) ([df1a549](https://github.com/anthropics/anthropic-sdk-python/commit/df1a5494d2d3be86717c344654ce54e2f97f19be))
* use latest sonnet in example snippets ([#781](https://github.com/anthropics/anthropic-sdk-python/issues/781)) ([1ad9e4f](https://github.com/anthropics/anthropic-sdk-python/commit/1ad9e4ff559f16760de15e2352a64bb2b3103071))

## 0.40.0 (2024-11-28)

Full Changelog: [v0.39.0...v0.40.0](https://github.com/anthropics/anthropic-sdk-python/compare/v0.39.0...v0.40.0)

### Features

* **client:** add ._request_id property to object responses ([#743](https://github.com/anthropics/anthropic-sdk-python/issues/743)) ([9fb64a6](https://github.com/anthropics/anthropic-sdk-python/commit/9fb64a627821730fcf48662f6326d4c0f8c623ab))


### Bug Fixes

* **asyncify:** avoid hanging process under certain conditions ([#756](https://github.com/anthropics/anthropic-sdk-python/issues/756)) ([c71bba2](https://github.com/anthropics/anthropic-sdk-python/commit/c71bba2ad5248400c0142fca5e53c505f9e6d417))
* **bedrock:** correct URL encoding for model params ([#759](https://github.com/anthropics/anthropic-sdk-python/issues/759)) ([be4e73a](https://github.com/anthropics/anthropic-sdk-python/commit/be4e73a6d6ced33c887cc338c7755f5fe1697e54))
* **client:** compat with new httpx 0.28.0 release ([#765](https://github.com/anthropics/anthropic-sdk-python/issues/765)) ([de51f60](https://github.com/anthropics/anthropic-sdk-python/commit/de51f6089f7b025db5d150438caf78a615431cde))
* don't use dicts as iterables in transform ([#750](https://github.com/anthropics/anthropic-sdk-python/issues/750)) ([1f71464](https://github.com/anthropics/anthropic-sdk-python/commit/1f71464a818066687bf6c1bcae0abb991d6ed9cd))
* **types:** remove anthropic-instant-1.2 model ([#744](https://github.com/anthropics/anthropic-sdk-python/issues/744)) ([23637de](https://github.com/anthropics/anthropic-sdk-python/commit/23637de028c6c870f062fc0fbaefa9ae54a0e053))


### Chores

* **api:** update spec version ([#751](https://github.com/anthropics/anthropic-sdk-python/issues/751)) ([4ec986c](https://github.com/anthropics/anthropic-sdk-python/commit/4ec986ccfa601a78f9fff721710390c1fb4727cc))
* **ci:** remove unneeded workflow ([#742](https://github.com/anthropics/anthropic-sdk-python/issues/742)) ([472b7d3](https://github.com/anthropics/anthropic-sdk-python/commit/472b7d362c4bd32e7b32c5a10ed3d40e6821f052))
* **internal:** exclude mypy from running on tests ([#764](https://github.com/anthropics/anthropic-sdk-python/issues/764)) ([bce763a](https://github.com/anthropics/anthropic-sdk-python/commit/bce763a35f5420d0e811ff3cd4d2bf7494f11081))
* **internal:** fix compat model_dump method when warnings are passed ([#760](https://github.com/anthropics/anthropic-sdk-python/issues/760)) ([0e09236](https://github.com/anthropics/anthropic-sdk-python/commit/0e0923612bb1ce4eb18f82966055df4fb8cd348d))
* **internal:** minor formatting changes ([493020e](https://github.com/anthropics/anthropic-sdk-python/commit/493020eed859bd20e49f4ac7ec0b6c3293c7d3fd))
* remove now unused `cached-property` dep ([#762](https://github.com/anthropics/anthropic-sdk-python/issues/762)) ([b9ffefe](https://github.com/anthropics/anthropic-sdk-python/commit/b9ffefec20279705a86e4ad342597886bd7064ca))
* **tests:** adjust retry timeout values ([#736](https://github.com/anthropics/anthropic-sdk-python/issues/736)) ([27ed781](https://github.com/anthropics/anthropic-sdk-python/commit/27ed7816aa8ae32f179652ea6171dd621ef8a6b5))
* **tests:** limit array example length ([#754](https://github.com/anthropics/anthropic-sdk-python/issues/754)) ([6cab2b9](https://github.com/anthropics/anthropic-sdk-python/commit/6cab2b9237c9679ce40e319d035fb4267bca03a7))


### Documentation

* add info log level to readme ([#761](https://github.com/anthropics/anthropic-sdk-python/issues/761)) ([5966b85](https://github.com/anthropics/anthropic-sdk-python/commit/5966b855f3e58d735d8ccfe3244f549baa3a87ed))
* move comments in example snippets ([#749](https://github.com/anthropics/anthropic-sdk-python/issues/749)) ([f887930](https://github.com/anthropics/anthropic-sdk-python/commit/f887930773cbb2d5cb0d4d46ec6cd4f320d045ea))

## 0.39.0 (2024-11-04)

Full Changelog: [v0.38.0...v0.39.0](https://github.com/anthropics/anthropic-sdk-python/compare/v0.38.0...v0.39.0)

### ⚠ BREAKING CHANGES

* **client:** remove legacy `client.count_tokens()` & `client.get_tokenizer()` methods ([#726](https://github.com/anthropics/anthropic-sdk-python/issues/726))
  * This functionality has been replaced by the `client.beta.messages.count_tokens()` API which supports newer models and all content functionality, such as images and PDFs.

### Features

* **api:** add new haiku model ([#731](https://github.com/anthropics/anthropic-sdk-python/issues/731)) ([77eaaf9](https://github.com/anthropics/anthropic-sdk-python/commit/77eaaf9c76f9b267706c830a5f7c1d81df6013d9))
* **project:** drop support for Python 3.7 ([#729](https://github.com/anthropics/anthropic-sdk-python/issues/729)) ([7f897e2](https://github.com/anthropics/anthropic-sdk-python/commit/7f897e253ae09e6a85fe64ba8004c2c3a8133e4e))


### Bug Fixes

* don't use dicts as iterables in transform ([#724](https://github.com/anthropics/anthropic-sdk-python/issues/724)) ([62bb863](https://github.com/anthropics/anthropic-sdk-python/commit/62bb8636a3d7156bc0caab5f574b1fa72445cead))
* support json safe serialization for basemodel subclasses ([#727](https://github.com/anthropics/anthropic-sdk-python/issues/727)) ([5be855e](https://github.com/anthropics/anthropic-sdk-python/commit/5be855e20f40042f59e839c7747dd994dc88c456))
* **types:** add missing token-counting-2024-11-01 ([#722](https://github.com/anthropics/anthropic-sdk-python/issues/722)) ([c549736](https://github.com/anthropics/anthropic-sdk-python/commit/c5497360a385f5dbaa5ab775bc19a0d7eee713bc))


### Documentation

* **readme:** mention new token counting endpoint ([#728](https://github.com/anthropics/anthropic-sdk-python/issues/728)) ([72a4636](https://github.com/anthropics/anthropic-sdk-python/commit/72a4636a7798170d69e7551ba58a0213d82d1711))


### Refactors

* **client:** remove legacy `client.count_tokens()` method ([#726](https://github.com/anthropics/anthropic-sdk-python/issues/726)) ([14e4244](https://github.com/anthropics/anthropic-sdk-python/commit/14e4244752b656cedfe7d160088e9744d07470a1))

## 0.38.0 (2024-11-01)

Full Changelog: [v0.37.1...v0.38.0](https://github.com/anthropics/anthropic-sdk-python/compare/v0.37.1...v0.38.0)

### Features

* **api:** add message token counting & PDFs support ([#721](https://github.com/anthropics/anthropic-sdk-python/issues/721)) ([e4856dd](https://github.com/anthropics/anthropic-sdk-python/commit/e4856dd6be698e797eaee2d6a669a6aaa6719e7d))


### Bug Fixes

* **count_tokens:** correctly set beta header ([e5b4b54](https://github.com/anthropics/anthropic-sdk-python/commit/e5b4b54e3ea1b4fc2d947d45df17996f66900387))
* **types:** add missing token-counting-2024-11-01 ([1897883](https://github.com/anthropics/anthropic-sdk-python/commit/1897883d6332bd0ad10cf13ad09e30563c3e7232))


### Chores

* **internal:** bump mypy ([#720](https://github.com/anthropics/anthropic-sdk-python/issues/720)) ([fe8d19e](https://github.com/anthropics/anthropic-sdk-python/commit/fe8d19e265c57fa9e34a09e46e808322e70c721d))
* **internal:** bump pytest to v8 & pydantic ([#716](https://github.com/anthropics/anthropic-sdk-python/issues/716)) ([00fe1f8](https://github.com/anthropics/anthropic-sdk-python/commit/00fe1f8b0c9c1312c7f1e62ce6ef9c5c56478ede))
* **internal:** update spec version ([#712](https://github.com/anthropics/anthropic-sdk-python/issues/712)) ([f71b0f5](https://github.com/anthropics/anthropic-sdk-python/commit/f71b0f5e54aab20b93cd13609151aa833583145a))
* **tests:** move lazy tokenizer test outside of pytest ([d8f2402](https://github.com/anthropics/anthropic-sdk-python/commit/d8f24023c7110b89528b7b37ddf9c1e6630562c4))

## 0.37.1 (2024-10-22)

Full Changelog: [v0.37.0...v0.37.1](https://github.com/anthropics/anthropic-sdk-python/compare/v0.37.0...v0.37.1)

### Bug Fixes

* **bedrock:** correct handling of messages beta ([#711](https://github.com/anthropics/anthropic-sdk-python/issues/711)) ([4cba32b](https://github.com/anthropics/anthropic-sdk-python/commit/4cba32b41e82377e155612e05c847baf2ca166d0))
* **vertex:** use correct beta url ([b76db5c](https://github.com/anthropics/anthropic-sdk-python/commit/b76db5c90a9b22d4078a15ac6844a4f75dcbc857))

## 0.37.0 (2024-10-22)

Full Changelog: [v0.36.2...v0.37.0](https://github.com/anthropics/anthropic-sdk-python/compare/v0.36.2...v0.37.0)

### Features

* **api:** add new model and `computer-use-2024-10-22` beta ([dd93d87](https://github.com/anthropics/anthropic-sdk-python/commit/dd93d872dd00a52b5bd65f84451fc9d368692cde))
* **bedrock:** add messages beta ([2566c93](https://github.com/anthropics/anthropic-sdk-python/commit/2566c93a7d7a861136ebdfde0eb90287977d43d1))
* **vertex:** add messages beta ([0d1f1a6](https://github.com/anthropics/anthropic-sdk-python/commit/0d1f1a663a7bd43f1f524ddaad1d6e18d6d68a61))


### Bug Fixes

* **client/async:** correctly retry in all cases ([#704](https://github.com/anthropics/anthropic-sdk-python/issues/704)) ([ee6febc](https://github.com/anthropics/anthropic-sdk-python/commit/ee6febc4b5c58db9aed835b021e476b46f68033e))


### Chores

* **api:** add title ([#703](https://github.com/anthropics/anthropic-sdk-python/issues/703)) ([a046817](https://github.com/anthropics/anthropic-sdk-python/commit/a046817e9181d35f145249eeb070cfbfd2c36901))
* **internal:** bump ruff dependency ([#700](https://github.com/anthropics/anthropic-sdk-python/issues/700)) ([d5bf9e1](https://github.com/anthropics/anthropic-sdk-python/commit/d5bf9e1f88486552dfba1409cfc699994a1e9aab))
* **internal:** remove unused black config ([#705](https://github.com/anthropics/anthropic-sdk-python/issues/705)) ([3259eb0](https://github.com/anthropics/anthropic-sdk-python/commit/3259eb0a740e65ec649da41667a703d0a4ec1eee))
* **internal:** update spec ([#706](https://github.com/anthropics/anthropic-sdk-python/issues/706)) ([6ab0ce9](https://github.com/anthropics/anthropic-sdk-python/commit/6ab0ce9acf3fdfb217c3885198f88a9ece0969af))

## 0.36.2 (2024-10-17)

Full Changelog: [v0.36.1...v0.36.2](https://github.com/anthropics/anthropic-sdk-python/compare/v0.36.1...v0.36.2)

### Bug Fixes

* **types:** remove misleading betas TypedDict property for the Batch API ([#697](https://github.com/anthropics/anthropic-sdk-python/issues/697)) ([e1b9e31](https://github.com/anthropics/anthropic-sdk-python/commit/e1b9e311644103466904fdce78469380d971ccad))


### Chores

* **internal:** update test syntax ([#699](https://github.com/anthropics/anthropic-sdk-python/issues/699)) ([a836157](https://github.com/anthropics/anthropic-sdk-python/commit/a836157d1c0cefc452f5f27fe90eea3b4ff687d2))

## 0.36.1 (2024-10-15)

Full Changelog: [v0.36.0...v0.36.1](https://github.com/anthropics/anthropic-sdk-python/compare/v0.36.0...v0.36.1)

### Bug Fixes

* allow header params to override default headers ([#690](https://github.com/anthropics/anthropic-sdk-python/issues/690)) ([56f195f](https://github.com/anthropics/anthropic-sdk-python/commit/56f195ff1a67f2ba6e546ad897cbb0fe39f36a3b))
* **beta:** merge betas param with the default value ([#695](https://github.com/anthropics/anthropic-sdk-python/issues/695)) ([f52eac9](https://github.com/anthropics/anthropic-sdk-python/commit/f52eac9357c0c496f1307def2628376d8a36e5ba))


### Chores

* **internal:** update spec URL ([#694](https://github.com/anthropics/anthropic-sdk-python/issues/694)) ([1b437cc](https://github.com/anthropics/anthropic-sdk-python/commit/1b437cc40f2e02e59df06744cc1458ee0cae202a))

## 0.36.0 (2024-10-08)

Full Changelog: [v0.35.0...v0.36.0](https://github.com/anthropics/anthropic-sdk-python/compare/v0.35.0...v0.36.0)

### Features

* **api:** add message batches api ([cd1ffcb](https://github.com/anthropics/anthropic-sdk-python/commit/cd1ffcb5e506c62e82e6f1365718949840724b9a))


### Bug Fixes

* **client:** avoid OverflowError with very large retry counts ([#676](https://github.com/anthropics/anthropic-sdk-python/issues/676)) ([93d6eeb](https://github.com/anthropics/anthropic-sdk-python/commit/93d6eeb80e63424b8a97f949d5354052b6b16cf4))


### Chores

* add repr to PageInfo class ([#678](https://github.com/anthropics/anthropic-sdk-python/issues/678)) ([53e87e8](https://github.com/anthropics/anthropic-sdk-python/commit/53e87e8abed82fe90fb2d877f69a2cc695662e86))


### Refactors

* **types:** improve metadata type names ([#683](https://github.com/anthropics/anthropic-sdk-python/issues/683)) ([59f2088](https://github.com/anthropics/anthropic-sdk-python/commit/59f208855039bb7b31266ae5e12d7454ecd69f3b))
* **types:** improve metadata types ([#682](https://github.com/anthropics/anthropic-sdk-python/issues/682)) ([e037d1c](https://github.com/anthropics/anthropic-sdk-python/commit/e037d1c310a6487e4f94a751232399e75f10b46d))
* **types:** improve tool type names ([#679](https://github.com/anthropics/anthropic-sdk-python/issues/679)) ([f6f3afe](https://github.com/anthropics/anthropic-sdk-python/commit/f6f3afe2e26ba004a24f7c3bdd36c7b4c1ae4697))
* **types:** improve tool type names ([#680](https://github.com/anthropics/anthropic-sdk-python/issues/680)) ([fe2e417](https://github.com/anthropics/anthropic-sdk-python/commit/fe2e4178dbdea42e84fd925e9e259fef6134c3d3))

## 0.35.0 (2024-10-04)

Full Changelog: [v0.34.2...v0.35.0](https://github.com/anthropics/anthropic-sdk-python/compare/v0.34.2...v0.35.0)

### Features

* **api:** support disabling parallel tool use ([#674](https://github.com/anthropics/anthropic-sdk-python/issues/674)) ([9079a99](https://github.com/anthropics/anthropic-sdk-python/commit/9079a99fffe5cf7bc91f052ed46b568e55792abf))
* **bedrock:** add `profile` argument to client ([#648](https://github.com/anthropics/anthropic-sdk-python/issues/648)) ([6ea5fce](https://github.com/anthropics/anthropic-sdk-python/commit/6ea5fce3b3a4d1ef4d5d3bbce8e27ea11e6dae72))
* **client:** allow overriding retry count header ([#670](https://github.com/anthropics/anthropic-sdk-python/issues/670)) ([1fb081f](https://github.com/anthropics/anthropic-sdk-python/commit/1fb081fa2005ad30d78a97755f14f81cbcfe28ab))
* **client:** send retry count header ([#664](https://github.com/anthropics/anthropic-sdk-python/issues/664)) ([17c26d5](https://github.com/anthropics/anthropic-sdk-python/commit/17c26d5761b3ee686525f43b22ab6d5e40fc90b1))


### Bug Fixes

* **client:** handle domains with underscores ([#663](https://github.com/anthropics/anthropic-sdk-python/issues/663)) ([84ad451](https://github.com/anthropics/anthropic-sdk-python/commit/84ad451bf1fa9ddff1f409472e8b63ae7678aa83))
* **types:** correctly mark stream discriminator as optional ([#657](https://github.com/anthropics/anthropic-sdk-python/issues/657)) ([2386f98](https://github.com/anthropics/anthropic-sdk-python/commit/2386f983593613034e6ca106be6a0cf95009ea4c))


### Chores

* add docstrings to raw response properties ([#654](https://github.com/anthropics/anthropic-sdk-python/issues/654)) ([35e6cf7](https://github.com/anthropics/anthropic-sdk-python/commit/35e6cf7c39d715181fb68f8fea6b835bf5d2085d))
* **internal:** add support for parsing bool response content ([#675](https://github.com/anthropics/anthropic-sdk-python/issues/675)) ([0bbc0a3](https://github.com/anthropics/anthropic-sdk-python/commit/0bbc0a365b9d64be93cfc8e6b992df95d83c06d7))
* **internal:** bump pyright / mypy version ([#662](https://github.com/anthropics/anthropic-sdk-python/issues/662)) ([c03a71f](https://github.com/anthropics/anthropic-sdk-python/commit/c03a71f71af845eef0b38ff29cdbaa444464fc6e))
* **internal:** bump ruff ([#660](https://github.com/anthropics/anthropic-sdk-python/issues/660)) ([0a34018](https://github.com/anthropics/anthropic-sdk-python/commit/0a34018057f818bf11ec0019ed1e9f413919b682))
* **internal:** update pydantic v1 compat helpers ([#666](https://github.com/anthropics/anthropic-sdk-python/issues/666)) ([ee8e2bd](https://github.com/anthropics/anthropic-sdk-python/commit/ee8e2bdd66b017ef87431ac8ff0b550b18548a3d))
* **internal:** use `typing_extensions.overload` instead of `typing` ([#667](https://github.com/anthropics/anthropic-sdk-python/issues/667)) ([153361d](https://github.com/anthropics/anthropic-sdk-python/commit/153361d4f24cc3497bd62a0a403007c889a8ed51))
* pyproject.toml formatting changes ([#650](https://github.com/anthropics/anthropic-sdk-python/issues/650)) ([4c229dc](https://github.com/anthropics/anthropic-sdk-python/commit/4c229dcdddb59785469390f330f82763d052cf4d))


### Documentation

* fix typo in fenced code block language ([#673](https://github.com/anthropics/anthropic-sdk-python/issues/673)) ([a03414e](https://github.com/anthropics/anthropic-sdk-python/commit/a03414e2d84c76db2cdf5e7ef2d04fef3b74b01a))
* improve and reference contributing documentation ([#672](https://github.com/anthropics/anthropic-sdk-python/issues/672)) ([5bd9690](https://github.com/anthropics/anthropic-sdk-python/commit/5bd96900d56338336efa37156ea144df7b69c624))
* **readme:** add section on determining installed version ([#655](https://github.com/anthropics/anthropic-sdk-python/issues/655)) ([5898f42](https://github.com/anthropics/anthropic-sdk-python/commit/5898f42ec2b794bcc26c98336768a10d6efed44f))
* update CONTRIBUTING.md ([#659](https://github.com/anthropics/anthropic-sdk-python/issues/659)) ([2df25bf](https://github.com/anthropics/anthropic-sdk-python/commit/2df25bf6d65a39fea6f526b692298e25667b1148))

## 0.34.2 (2024-09-04)

Full Changelog: [v0.34.1...v0.34.2](https://github.com/anthropics/anthropic-sdk-python/compare/v0.34.1...v0.34.2)

### Chores

* **api:** deprecate claude-1 model ([eab07dc](https://github.com/anthropics/anthropic-sdk-python/commit/eab07dc1984ea20918bb0d902108a1ce4646a1e0))
* **ci:** also run pydantic v1 tests ([#644](https://github.com/anthropics/anthropic-sdk-python/issues/644)) ([c61fe89](https://github.com/anthropics/anthropic-sdk-python/commit/c61fe899e79f21691c7a19d40f1bc397b3f3f82d))

## 0.34.1 (2024-08-19)

Full Changelog: [v0.34.0...v0.34.1](https://github.com/anthropics/anthropic-sdk-python/compare/v0.34.0...v0.34.1)

### Chores

* **ci:** add CODEOWNERS file ([#639](https://github.com/anthropics/anthropic-sdk-python/issues/639)) ([33001cc](https://github.com/anthropics/anthropic-sdk-python/commit/33001ccf80f6ec2ac43b74f5f41034ec6a12552b))
* **client:** fix parsing union responses when non-json is returned ([#643](https://github.com/anthropics/anthropic-sdk-python/issues/643)) ([45be91d](https://github.com/anthropics/anthropic-sdk-python/commit/45be91dbcc2789a71a048a34f1f23977b9829818))
* **docs/api:** update prompt caching helpers ([6a55aee](https://github.com/anthropics/anthropic-sdk-python/commit/6a55aeeaca83ade0adc18eae0f8682558769d5ff))
* **internal:** use different 32bit detection method ([#640](https://github.com/anthropics/anthropic-sdk-python/issues/640)) ([d6b2b63](https://github.com/anthropics/anthropic-sdk-python/commit/d6b2b630613f7c5f01fc3cd005a055989e7d8e71))

## 0.34.0 (2024-08-14)

Full Changelog: [v0.33.1...v0.34.0](https://github.com/anthropics/anthropic-sdk-python/compare/v0.33.1...v0.34.0)

### Features

* **api:** add prompt caching beta ([3978411](https://github.com/anthropics/anthropic-sdk-python/commit/397841125164a2420d5abf8f45d47f2467e36cd9))
* **client:** add streaming helpers for prompt caching ([98a0a7b](https://github.com/anthropics/anthropic-sdk-python/commit/98a0a7b9c679539c98d212b12c0a9a950fd6371d))


### Chores

* **examples:** minor formatting changes ([#633](https://github.com/anthropics/anthropic-sdk-python/issues/633)) ([20487ea](https://github.com/anthropics/anthropic-sdk-python/commit/20487ea0080969511e7c41f199387b87a84f6ab4))

## 0.33.1 (2024-08-12)

Full Changelog: [v0.33.0...v0.33.1](https://github.com/anthropics/anthropic-sdk-python/compare/v0.33.0...v0.33.1)

### Chores

* **ci:** bump prism mock server version ([#630](https://github.com/anthropics/anthropic-sdk-python/issues/630)) ([29545ee](https://github.com/anthropics/anthropic-sdk-python/commit/29545eee2e7bfdfe73b590d9301aa68bbf2c361d))
* **internal:** ensure package is importable in lint cmd ([#632](https://github.com/anthropics/anthropic-sdk-python/issues/632)) ([d685824](https://github.com/anthropics/anthropic-sdk-python/commit/d685824b2c080bd1b17f677f4af422b5cb0e7ed5))

## 0.33.0 (2024-08-09)

Full Changelog: [v0.32.0...v0.33.0](https://github.com/anthropics/anthropic-sdk-python/compare/v0.32.0...v0.33.0)

### Features

* **client:** add `retries_taken` to raw response class ([43fb587](https://github.com/anthropics/anthropic-sdk-python/commit/43fb5874b0a2398221d1f1d0fea316faca9f6484))


### Chores

* **internal:** bump pyright ([#622](https://github.com/anthropics/anthropic-sdk-python/issues/622)) ([9480109](https://github.com/anthropics/anthropic-sdk-python/commit/9480109c380ff571487429d5f50f50e23947d788))
* **internal:** bump ruff version ([#625](https://github.com/anthropics/anthropic-sdk-python/issues/625)) ([b1a4e7b](https://github.com/anthropics/anthropic-sdk-python/commit/b1a4e7b9a8c17184038d1816ff08619cb03f6296))
* **internal:** test updates ([#624](https://github.com/anthropics/anthropic-sdk-python/issues/624)) ([2cea1f5](https://github.com/anthropics/anthropic-sdk-python/commit/2cea1f52bad2fb6b8f0705fd672f75d8a6281ba0))
* **internal:** update pydantic compat helper function ([#627](https://github.com/anthropics/anthropic-sdk-python/issues/627)) ([dc18ee0](https://github.com/anthropics/anthropic-sdk-python/commit/dc18ee0af5a86429ee8bcc9d5c186493f8d5c622))
* **internal:** updates ([#629](https://github.com/anthropics/anthropic-sdk-python/issues/629)) ([d6357a6](https://github.com/anthropics/anthropic-sdk-python/commit/d6357a6172a38d7cf5ab51d9d7b699d44d2adc21))
* **internal:** use `TypeAlias` marker for type assignments ([#621](https://github.com/anthropics/anthropic-sdk-python/issues/621)) ([a4bff9c](https://github.com/anthropics/anthropic-sdk-python/commit/a4bff9cee99d3ee2083426ec41b40bdcf70d6b4f))
* sync openapi version ([#617](https://github.com/anthropics/anthropic-sdk-python/issues/617)) ([9c0ad95](https://github.com/anthropics/anthropic-sdk-python/commit/9c0ad95b530f1fbd2293a15dcce7f583a982aad0))
* sync openapi version ([#620](https://github.com/anthropics/anthropic-sdk-python/issues/620)) ([0a3f3fa](https://github.com/anthropics/anthropic-sdk-python/commit/0a3f3fa8d89f90f321c27b0cb8c4187b68161fc5))
* sync openapi version ([#628](https://github.com/anthropics/anthropic-sdk-python/issues/628)) ([cfad41f](https://github.com/anthropics/anthropic-sdk-python/commit/cfad41f8a36836060d1b2bba0f32ee291ff8df05))

## 0.32.0 (2024-07-29)

Full Changelog: [v0.31.2...v0.32.0](https://github.com/anthropics/anthropic-sdk-python/compare/v0.31.2...v0.32.0)

### Features

* add back compat alias for InputJsonDelta ([25a5b6c](https://github.com/anthropics/anthropic-sdk-python/commit/25a5b6c81ffb5996ef697aab22a22d8be5751bc1))


### Bug Fixes

* change signatures for the stream function ([c9eb11b](https://github.com/anthropics/anthropic-sdk-python/commit/c9eb11b1f9656202ee88e9869e59160bc37f5434))
* **client:** correctly apply client level timeout for messages ([#615](https://github.com/anthropics/anthropic-sdk-python/issues/615)) ([5f8d88f](https://github.com/anthropics/anthropic-sdk-python/commit/5f8d88f6fcc2ba05cd9fc6f8ae7aa8c61dc6b0d0))


### Chores

* **docs:** document how to do per-request http client customization ([#603](https://github.com/anthropics/anthropic-sdk-python/issues/603)) ([5161f62](https://github.com/anthropics/anthropic-sdk-python/commit/5161f626a0bec757b96217dc0f81e8908546f29a))
* **internal:** add type construction helper ([#613](https://github.com/anthropics/anthropic-sdk-python/issues/613)) ([5e36940](https://github.com/anthropics/anthropic-sdk-python/commit/5e36940a42e401c3f0c1e42aa248d431fdf7192c))
* sync spec ([#605](https://github.com/anthropics/anthropic-sdk-python/issues/605)) ([6b7707f](https://github.com/anthropics/anthropic-sdk-python/commit/6b7707f62788fca2e166209e82935a2a2fa8204a))
* **tests:** update prism version ([#607](https://github.com/anthropics/anthropic-sdk-python/issues/607)) ([1797dc6](https://github.com/anthropics/anthropic-sdk-python/commit/1797dc6139ffaca6436ed897972471e67ba1b828))


### Refactors

* extract model out to a named type and rename partialjson ([#612](https://github.com/anthropics/anthropic-sdk-python/issues/612)) ([c53efc7](https://github.com/anthropics/anthropic-sdk-python/commit/c53efc786fa95831a398f37740a81b42f7b64c94))

## 0.31.2 (2024-07-17)

Full Changelog: [v0.31.1...v0.31.2](https://github.com/anthropics/anthropic-sdk-python/compare/v0.31.1...v0.31.2)

### Bug Fixes

* **vertex:** also refresh auth if there is no token ([4a8d02d](https://github.com/anthropics/anthropic-sdk-python/commit/4a8d02d0616c04a2acc31a3179b7d50093d6371e))
* **vertex:** correct request options in retries ([460547b](https://github.com/anthropics/anthropic-sdk-python/commit/460547b7e6bafa4044127760946d141d1e49131b))


### Chores

* **docs:** minor update to formatting of API link in README ([#594](https://github.com/anthropics/anthropic-sdk-python/issues/594)) ([113b6ac](https://github.com/anthropics/anthropic-sdk-python/commit/113b6ac65de2a670b0d957d11d48b060106150d3))
* **internal:** update formatting ([#597](https://github.com/anthropics/anthropic-sdk-python/issues/597)) ([565dfcd](https://github.com/anthropics/anthropic-sdk-python/commit/565dfcd4610c26b598f6c72e9182e8c60bffc2a0))
* **tests:** faster bedrock retry tests ([4ff067f](https://github.com/anthropics/anthropic-sdk-python/commit/4ff067f48e8e177ebdb8f06d6a4a0ffe9a096a8b))

## 0.31.1 (2024-07-15)

Full Changelog: [v0.31.0...v0.31.1](https://github.com/anthropics/anthropic-sdk-python/compare/v0.31.0...v0.31.1)

### Bug Fixes

* **bedrock:** correct request options for retries ([#593](https://github.com/anthropics/anthropic-sdk-python/issues/593)) ([f68c81d](https://github.com/anthropics/anthropic-sdk-python/commit/f68c81d072fceb46d4c0d8ee62cf274eeea99415))


### Chores

* **ci:** also run workflows for PRs targeting `next` ([#587](https://github.com/anthropics/anthropic-sdk-python/issues/587)) ([f7e49f2](https://github.com/anthropics/anthropic-sdk-python/commit/f7e49f2f2ceb62cccd6961fc1bd799655ccd83ab))
* **internal:** minor changes to tests ([#591](https://github.com/anthropics/anthropic-sdk-python/issues/591)) ([fabd591](https://github.com/anthropics/anthropic-sdk-python/commit/fabd5910f2e769b8bfbeaaa8b65ca8383b4954e3))
* **internal:** minor formatting changes ([a71927b](https://github.com/anthropics/anthropic-sdk-python/commit/a71927b7c7cff4e83eb485d3b0eef928a18acef6))
* **internal:** minor import restructuring ([#588](https://github.com/anthropics/anthropic-sdk-python/issues/588)) ([1d9db4f](https://github.com/anthropics/anthropic-sdk-python/commit/1d9db4f6c1393c3879e83e1a3e1d1b4fedc33b5a))
* **internal:** minor options / compat functions updates ([#592](https://github.com/anthropics/anthropic-sdk-python/issues/592)) ([d41a880](https://github.com/anthropics/anthropic-sdk-python/commit/d41a8807057958d4505e16325e4a06359a760260))
* **internal:** update mypy ([#584](https://github.com/anthropics/anthropic-sdk-python/issues/584)) ([0a0edce](https://github.com/anthropics/anthropic-sdk-python/commit/0a0edce53e9eebd47770e71493302527e7f43751))

## 0.31.0 (2024-07-10)

Full Changelog: [v0.30.1...v0.31.0](https://github.com/anthropics/anthropic-sdk-python/compare/v0.30.1...v0.31.0)

### Features

* **client:** make request-id header more accessible ([#581](https://github.com/anthropics/anthropic-sdk-python/issues/581)) ([130d470](https://github.com/anthropics/anthropic-sdk-python/commit/130d470fc624a25defb9d8e787462b77bdc0aad5))
* **vertex:** add copy and with_options ([#578](https://github.com/anthropics/anthropic-sdk-python/issues/578)) ([fcd425f](https://github.com/anthropics/anthropic-sdk-python/commit/fcd425f724fee45195118aa218bd5c51fb9abed0))


### Bug Fixes

* **client:** always respect content-type multipart/form-data if provided ([#574](https://github.com/anthropics/anthropic-sdk-python/issues/574)) ([6051763](https://github.com/anthropics/anthropic-sdk-python/commit/6051763d886aa7107389d8b8aeacf74d296eed3d))
* **streaming/messages:** more robust event type construction ([#576](https://github.com/anthropics/anthropic-sdk-python/issues/576)) ([98e2075](https://github.com/anthropics/anthropic-sdk-python/commit/98e2075869d816cd85af1a0588bd27719eff02a4))
* **types:** allow arbitrary types in image block param ([#582](https://github.com/anthropics/anthropic-sdk-python/issues/582)) ([ebd6590](https://github.com/anthropics/anthropic-sdk-python/commit/ebd659014b63b51fa2f67fe88ef3fc9922be830d))
* Updated doc typo ([17be06b](https://github.com/anthropics/anthropic-sdk-python/commit/17be06bf3e39eff9de588d99cd59fa509c5ee6a6))
* **vertex:** avoid credentials refresh on every request ([#575](https://github.com/anthropics/anthropic-sdk-python/issues/575)) ([37bd433](https://github.com/anthropics/anthropic-sdk-python/commit/37bd4337828f3efa14b194fa3025638229129416))


### Chores

* **ci:** update rye to v0.35.0 ([#577](https://github.com/anthropics/anthropic-sdk-python/issues/577)) ([e271d69](https://github.com/anthropics/anthropic-sdk-python/commit/e271d694babfb4bcb506064aa353ee29a8394c1d))
* **internal:** add helper method for constructing `BaseModel`s ([#572](https://github.com/anthropics/anthropic-sdk-python/issues/572)) ([8e626ac](https://github.com/anthropics/anthropic-sdk-python/commit/8e626ac7c88bab413bc1e2d83b7556aa4a44fb63))
* **internal:** fix formatting ([a912917](https://github.com/anthropics/anthropic-sdk-python/commit/a912917686d6e4a46d192abf002ac69357b1d955))
* **internal:** minor request options handling changes ([#580](https://github.com/anthropics/anthropic-sdk-python/issues/580)) ([d1dcf42](https://github.com/anthropics/anthropic-sdk-python/commit/d1dcf427ea78f57dd267d891c276b03d4010de78))

## 0.30.1 (2024-07-01)

Full Changelog: [v0.30.0...v0.30.1](https://github.com/anthropics/anthropic-sdk-python/compare/v0.30.0...v0.30.1)

### Bug Fixes

* **build:** include more files in sdist builds ([#559](https://github.com/anthropics/anthropic-sdk-python/issues/559)) ([9170d08](https://github.com/anthropics/anthropic-sdk-python/commit/9170d08e056ecb33f1441f50b8407a1c60c45d94))


### Chores

* **deps:** bump anyio to v4.4.0 ([#562](https://github.com/anthropics/anthropic-sdk-python/issues/562)) ([70fc936](https://github.com/anthropics/anthropic-sdk-python/commit/70fc9361848e4825f8036da2b76a189d602e0baf))
* gitignore test server logs ([#567](https://github.com/anthropics/anthropic-sdk-python/issues/567)) ([f7b9283](https://github.com/anthropics/anthropic-sdk-python/commit/f7b928386b9f6dfdea6842ce729024afdc55da3f))
* **internal:** add reflection helper function ([#565](https://github.com/anthropics/anthropic-sdk-python/issues/565)) ([9483573](https://github.com/anthropics/anthropic-sdk-python/commit/948357378f2234e7ddc3843c0427cfa0b9914a21))
* **internal:** add rich as a dev dependency ([#568](https://github.com/anthropics/anthropic-sdk-python/issues/568)) ([07903ac](https://github.com/anthropics/anthropic-sdk-python/commit/07903acb9388ce6a3c35058880c89e1275aab1e3))

## 0.30.0 (2024-06-26)

Full Changelog: [v0.29.2...v0.30.0](https://github.com/anthropics/anthropic-sdk-python/compare/v0.29.2...v0.30.0)

### Features

* **vertex:** add credentials argument ([#542](https://github.com/anthropics/anthropic-sdk-python/issues/542)) ([3bfb2ea](https://github.com/anthropics/anthropic-sdk-python/commit/3bfb2eaf59410053870c7a598bef6404f2201145))

## 0.29.2 (2024-06-26)

Full Changelog: [v0.29.1...v0.29.2](https://github.com/anthropics/anthropic-sdk-python/compare/v0.29.1...v0.29.2)

### Bug Fixes

* temporarily patch upstream version to fix broken release flow ([#555](https://github.com/anthropics/anthropic-sdk-python/issues/555)) ([5471710](https://github.com/anthropics/anthropic-sdk-python/commit/54717101f3844791bdde8b9b76f47abf04c6a971))

## 0.29.1 (2024-06-25)

Full Changelog: [v0.29.0...v0.29.1](https://github.com/anthropics/anthropic-sdk-python/compare/v0.29.0...v0.29.1)

### Bug Fixes

* **api:** add string to tool result block ([#554](https://github.com/anthropics/anthropic-sdk-python/issues/554)) ([f283b4e](https://github.com/anthropics/anthropic-sdk-python/commit/f283b4eb9e4f118bb4ada38479747b22dd5282fa))
* **docs:** fix link to advanced python httpx docs ([#550](https://github.com/anthropics/anthropic-sdk-python/issues/550)) ([474ff7c](https://github.com/anthropics/anthropic-sdk-python/commit/474ff7cad99039f3539a787ec535b5b13e2832a9))

## 0.29.0 (2024-06-20)

Full Changelog: [v0.28.1...v0.29.0](https://github.com/anthropics/anthropic-sdk-python/compare/v0.28.1...v0.29.0)

### Features

* **api:** add new claude-3-5-sonnet-20240620 model ([#545](https://github.com/anthropics/anthropic-sdk-python/issues/545)) ([5ea6b18](https://github.com/anthropics/anthropic-sdk-python/commit/5ea6b182715cd355cc405554b81f3d0f725486f6))


### Bug Fixes

* **client/async:** avoid blocking io call for platform headers ([#544](https://github.com/anthropics/anthropic-sdk-python/issues/544)) ([3c2b75f](https://github.com/anthropics/anthropic-sdk-python/commit/3c2b75fac662e48effc8ec032266d966e548007d))


### Chores

* **internal:** add a `default_query` method ([#540](https://github.com/anthropics/anthropic-sdk-python/issues/540)) ([0253ebc](https://github.com/anthropics/anthropic-sdk-python/commit/0253ebc9cda491ab909cc752d719e797086691ed))

## 0.28.1 (2024-06-14)

Full Changelog: [v0.28.0...v0.28.1](https://github.com/anthropics/anthropic-sdk-python/compare/v0.28.0...v0.28.1)

### Documentation

* **readme:** tool use is no longer in beta ([d2be3c0](https://github.com/anthropics/anthropic-sdk-python/commit/d2be3c0438429b6521fc49f5a5ff17fae71fb589))

## 0.28.0 (2024-05-30)

Full Changelog: [v0.27.0...v0.28.0](https://github.com/anthropics/anthropic-sdk-python/compare/v0.27.0...v0.28.0)

### ⚠ BREAKING CHANGES

* **streaming:** remove old event_handler API ([#532](https://github.com/anthropics/anthropic-sdk-python/issues/532))

### Refactors

* **streaming:** remove old event_handler API ([#532](https://github.com/anthropics/anthropic-sdk-python/issues/532)) ([d9acfd4](https://github.com/anthropics/anthropic-sdk-python/commit/d9acfd427e3d7d8c6bc3d6ed8994194a07ed6a92))

## 0.27.0 (2024-05-30)

Full Changelog: [v0.26.2...v0.27.0](https://github.com/anthropics/anthropic-sdk-python/compare/v0.26.2...v0.27.0)

### Features

* **api:** tool use is GA and available on 3P ([#530](https://github.com/anthropics/anthropic-sdk-python/issues/530)) ([ad7adbd](https://github.com/anthropics/anthropic-sdk-python/commit/ad7adbd2a732db98665333c27065ff4f4c946f15))
* **streaming/messages:** refactor to event iterator structure ([997af69](https://github.com/anthropics/anthropic-sdk-python/commit/997af696a713a604d4146f36caf91397ba488e33))
* **streaming/tools:** refactor to event iterator structure ([bdcc283](https://github.com/anthropics/anthropic-sdk-python/commit/bdcc28303206fde2da01296cdae553c1e8efb60a))
* **streaming:** add tools support ([9f00950](https://github.com/anthropics/anthropic-sdk-python/commit/9f00950b81d388f14027c48aca1ca3c044b93a03))


### Bug Fixes

* **beta:** streaming breakage due to breaking change in dependency ([afe3c87](https://github.com/anthropics/anthropic-sdk-python/commit/afe3c8726576cdc7e0503707f53fa9a80caed962))


### Chores

* add missing __all__ definitions ([#526](https://github.com/anthropics/anthropic-sdk-python/issues/526)) ([5021787](https://github.com/anthropics/anthropic-sdk-python/commit/5021787caeda8a38775c69449a5794b1072dbfe5))
* **examples:** update tools ([56edecc](https://github.com/anthropics/anthropic-sdk-python/commit/56edecc2de1e943d6ca09a788c4fabac5978ea2d))
* **formatting:** misc fixups ([fbad5a0](https://github.com/anthropics/anthropic-sdk-python/commit/fbad5a0e0d7f4dbeeffa8a038600c9acb88002fc))
* **internal:** fix lint issues in tests ([d857640](https://github.com/anthropics/anthropic-sdk-python/commit/d857640c1e30b580e7e94e034a1fbc07f655acc6))
* **internal:** update bootstrap script ([#527](https://github.com/anthropics/anthropic-sdk-python/issues/527)) ([93ae152](https://github.com/anthropics/anthropic-sdk-python/commit/93ae1528c0404631f32c49341032ca0d11314b80))
* **internal:** update some references to rye-up.com ([00e34e7](https://github.com/anthropics/anthropic-sdk-python/commit/00e34e7fbbb3a797d55bb94c07d551ad083dc7d9))
* **tests:** ensure messages.create() and messages.stream() stay in sync ([52bd67b](https://github.com/anthropics/anthropic-sdk-python/commit/52bd67b041283adeee662355d8df297ca4b1d560))


### Documentation

* **helpers:** mention input json event ([02d482c](https://github.com/anthropics/anthropic-sdk-python/commit/02d482c03c039bc635c4d35e04cebe4670e1762c))
* **helpers:** update for new event iterator ([26f9533](https://github.com/anthropics/anthropic-sdk-python/commit/26f9533df19ee3da55c590238eba745051cccf6c))


### Refactors

* **api:** add Raw prefix to API stream event type names ([#529](https://github.com/anthropics/anthropic-sdk-python/issues/529)) ([bb62980](https://github.com/anthropics/anthropic-sdk-python/commit/bb629806887de6cd3e5d517af4d9615f40076542))

## 0.26.2 (2024-05-27)

Full Changelog: [v0.26.1...v0.26.2](https://github.com/anthropics/anthropic-sdk-python/compare/v0.26.1...v0.26.2)

### Bug Fixes

* **vertex:** don't error if project_id couldn't be loaded if it was already explicitly given ([#513](https://github.com/anthropics/anthropic-sdk-python/issues/513)) ([e7159d8](https://github.com/anthropics/anthropic-sdk-python/commit/e7159d87b207592eff364c1d75bab348dd414257))


### Chores

* **ci:** update rye install location ([#516](https://github.com/anthropics/anthropic-sdk-python/issues/516)) ([a6e347a](https://github.com/anthropics/anthropic-sdk-python/commit/a6e347a2c4aa75d00ee3ada3dfa707a080d890b6))
* **ci:** update rye install location ([#518](https://github.com/anthropics/anthropic-sdk-python/issues/518)) ([5122420](https://github.com/anthropics/anthropic-sdk-python/commit/51224208a732136caeb30d839685a91d7a26beda))
* **internal:** bump pyright ([196e4b0](https://github.com/anthropics/anthropic-sdk-python/commit/196e4b06cb4794a06d813b4e59dd8c5fbb61d71d))
* **internal:** remove unused __events stream property ([472b831](https://github.com/anthropics/anthropic-sdk-python/commit/472b831a552e7ebe20a9d503b129d8c1e1cef0c8))
* **internal:** restructure streaming implementation to use composition ([b1a1c03](https://github.com/anthropics/anthropic-sdk-python/commit/b1a1c0354a9aca450a7d512fdbdeb59c0ead688a))
* **messages:** add back-compat for isinstance() checks ([7794bcb](https://github.com/anthropics/anthropic-sdk-python/commit/7794bcb680300249cd9be48562ce190eed8b9cff))
* **tests:** fix lints ([#521](https://github.com/anthropics/anthropic-sdk-python/issues/521)) ([d96fc53](https://github.com/anthropics/anthropic-sdk-python/commit/d96fc530902bfe4b6a0c75044bf60e90f32997e4))


### Documentation

* **contributing:** update references to rye-up.com ([6486898](https://github.com/anthropics/anthropic-sdk-python/commit/6486898e874784f39be36a0a011867dd2fe8a5d5))

## 0.26.1 (2024-05-21)

Full Changelog: [v0.26.0...v0.26.1](https://github.com/anthropics/anthropic-sdk-python/compare/v0.26.0...v0.26.1)

### Chores

* **docs:** fix typo ([#511](https://github.com/anthropics/anthropic-sdk-python/issues/511)) ([d7401bd](https://github.com/anthropics/anthropic-sdk-python/commit/d7401bdca637958171bad6b17406e8201c5bc6f6))
* **tools:** rely on pydantic's JSON parser instead of pydantic ([#510](https://github.com/anthropics/anthropic-sdk-python/issues/510)) ([8e7edca](https://github.com/anthropics/anthropic-sdk-python/commit/8e7edca45525be97a4a12a365db72b1668b3e4a1))

## 0.26.0 (2024-05-16)

Full Changelog: [v0.25.9...v0.26.0](https://github.com/anthropics/anthropic-sdk-python/compare/v0.25.9...v0.26.0)

### Features

* **api:** add `tool_choice` param, image block params inside `tool_result.content`, and streaming for `tool_use` blocks ([#502](https://github.com/anthropics/anthropic-sdk-python/issues/502)) ([e0bc274](https://github.com/anthropics/anthropic-sdk-python/commit/e0bc2749d4be57fe9f0d60635b3198de89608bb9))


### Chores

* **internal:** minor formatting changes ([#500](https://github.com/anthropics/anthropic-sdk-python/issues/500)) ([8b32558](https://github.com/anthropics/anthropic-sdk-python/commit/8b32558e95d83badea1bfe4084fb5db86f7f78cd))

## 0.25.9 (2024-05-14)

Full Changelog: [v0.25.8...v0.25.9](https://github.com/anthropics/anthropic-sdk-python/compare/v0.25.8...v0.25.9)

### Bug Fixes

* **types:** correct type for InputSchema ([#498](https://github.com/anthropics/anthropic-sdk-python/issues/498)) ([b86936c](https://github.com/anthropics/anthropic-sdk-python/commit/b86936ccb4ebe27bfb04a8fda2cbfdf88bbdc111))


### Chores

* **docs:** add SECURITY.md ([#493](https://github.com/anthropics/anthropic-sdk-python/issues/493)) ([d5cba46](https://github.com/anthropics/anthropic-sdk-python/commit/d5cba4634213b57f39dbc0f339c3320c651cf1bc))
* **internal:** add slightly better logging to scripts ([#497](https://github.com/anthropics/anthropic-sdk-python/issues/497)) ([acb0149](https://github.com/anthropics/anthropic-sdk-python/commit/acb0149b4659c932ca6f3abac46c4de166b5341b))
* **internal:** bump pydantic dependency ([#495](https://github.com/anthropics/anthropic-sdk-python/issues/495)) ([00cd840](https://github.com/anthropics/anthropic-sdk-python/commit/00cd8408254622d7e95812c0208fe09396d07ca4))
* **types:** add union discriminator metadata ([#491](https://github.com/anthropics/anthropic-sdk-python/issues/491)) ([95544a9](https://github.com/anthropics/anthropic-sdk-python/commit/95544a9e9fec7cfaab034355426a2f4634b8e26a))

## 0.25.8 (2024-05-07)

Full Changelog: [v0.25.7...v0.25.8](https://github.com/anthropics/anthropic-sdk-python/compare/v0.25.7...v0.25.8)

### Chores

* **client:** log response headers in debug mode ([#480](https://github.com/anthropics/anthropic-sdk-python/issues/480)) ([d1c4d14](https://github.com/anthropics/anthropic-sdk-python/commit/d1c4d14c881b0e754ca220cdcda4d06fe23c81ab))
* **internal:** add link to openapi spec ([#484](https://github.com/anthropics/anthropic-sdk-python/issues/484)) ([876cd0d](https://github.com/anthropics/anthropic-sdk-python/commit/876cd0d5b30ca823c4088124ec303e0765d993b8))
* **internal:** add scripts/test, scripts/mock and add ci job ([#486](https://github.com/anthropics/anthropic-sdk-python/issues/486)) ([6111fe8](https://github.com/anthropics/anthropic-sdk-python/commit/6111fe897d8111f8b3e301923a94eabe1cb96558))
* **internal:** bump prism version ([#487](https://github.com/anthropics/anthropic-sdk-python/issues/487)) ([98fb3e6](https://github.com/anthropics/anthropic-sdk-python/commit/98fb3e63f16adccb6ff46d4c259d1953c91f041e))


### Documentation

* **readme:** fix misleading timeout example value ([#489](https://github.com/anthropics/anthropic-sdk-python/issues/489)) ([b465bce](https://github.com/anthropics/anthropic-sdk-python/commit/b465bce54de95d30190154dbfc53446b1586dade))

## 0.25.7 (2024-04-29)

Full Changelog: [v0.25.6...v0.25.7](https://github.com/anthropics/anthropic-sdk-python/compare/v0.25.6...v0.25.7)

### Bug Fixes

* **docs:** doc improvements ([#472](https://github.com/anthropics/anthropic-sdk-python/issues/472)) ([1b6d4e2](https://github.com/anthropics/anthropic-sdk-python/commit/1b6d4e2c6be01dd794824a912cd78545d5bba135))


### Chores

* **internal:** minor reformatting ([#478](https://github.com/anthropics/anthropic-sdk-python/issues/478)) ([de4b2e0](https://github.com/anthropics/anthropic-sdk-python/commit/de4b2e088a997760e177abc765172bb495ccb978))
* **internal:** reformat imports ([#477](https://github.com/anthropics/anthropic-sdk-python/issues/477)) ([553e955](https://github.com/anthropics/anthropic-sdk-python/commit/553e955de5d6aae29ee28e1edfcc24d1ee9f3c25))
* **internal:** restructure imports ([#470](https://github.com/anthropics/anthropic-sdk-python/issues/470)) ([49e0044](https://github.com/anthropics/anthropic-sdk-python/commit/49e0044bcf1949699275d67dbed8dbf1c5412366))
* **internal:** update test helper function ([#476](https://github.com/anthropics/anthropic-sdk-python/issues/476)) ([f46e454](https://github.com/anthropics/anthropic-sdk-python/commit/f46e454f04ccb320fed2639235f9b382f3de27cd))
* **internal:** use actions/checkout@v4 for codeflow ([#474](https://github.com/anthropics/anthropic-sdk-python/issues/474)) ([8b18b52](https://github.com/anthropics/anthropic-sdk-python/commit/8b18b5211a200a1e09647441cd16244dfda05253))
* **tests:** rename test file ([#473](https://github.com/anthropics/anthropic-sdk-python/issues/473)) ([5b8261c](https://github.com/anthropics/anthropic-sdk-python/commit/5b8261c251e765ac239f1c0176ec3001b12769dd))

## 0.25.6 (2024-04-18)

Full Changelog: [v0.25.5...v0.25.6](https://github.com/anthropics/anthropic-sdk-python/compare/v0.25.5...v0.25.6)

### Chores

* **internal:** bump pyright to 1.1.359 ([#466](https://github.com/anthropics/anthropic-sdk-python/issues/466)) ([8088160](https://github.com/anthropics/anthropic-sdk-python/commit/808816044cb33499c45e12b609f7a7664c628c88))

## 0.25.5 (2024-04-17)

Full Changelog: [v0.25.4...v0.25.5](https://github.com/anthropics/anthropic-sdk-python/compare/v0.25.4...v0.25.5)

### Chores

* **internal:** ban usage of lru_cache ([#464](https://github.com/anthropics/anthropic-sdk-python/issues/464)) ([dc8ca22](https://github.com/anthropics/anthropic-sdk-python/commit/dc8ca22b1994af994ce9502494f4df1741c0559d))

## 0.25.4 (2024-04-17)

Full Changelog: [v0.25.3...v0.25.4](https://github.com/anthropics/anthropic-sdk-python/compare/v0.25.3...v0.25.4)

### Bug Fixes

* **bedrock:** correct auth implementation ([#462](https://github.com/anthropics/anthropic-sdk-python/issues/462)) ([2f456f5](https://github.com/anthropics/anthropic-sdk-python/commit/2f456f59f42876dfabde94b6e36f9349fc409aef))

## 0.25.3 (2024-04-17)

Full Changelog: [v0.25.2...v0.25.3](https://github.com/anthropics/anthropic-sdk-python/compare/v0.25.2...v0.25.3)

### Chores

* **bedrock:** cache boto sessions ([#455](https://github.com/anthropics/anthropic-sdk-python/issues/455)) ([d58adef](https://github.com/anthropics/anthropic-sdk-python/commit/d58adefc7097d98e25bb1665be2037f968000d76))

## 0.25.2 (2024-04-15)

Full Changelog: [v0.25.1...v0.25.2](https://github.com/anthropics/anthropic-sdk-python/compare/v0.25.1...v0.25.2)

### Chores

* **internal:** formatting ([#452](https://github.com/anthropics/anthropic-sdk-python/issues/452)) ([8ac016b](https://github.com/anthropics/anthropic-sdk-python/commit/8ac016b3be19247a7323f3f9fb5aad4d4f30ced5))

## 0.25.1 (2024-04-11)

Full Changelog: [v0.25.0...v0.25.1](https://github.com/anthropics/anthropic-sdk-python/compare/v0.25.0...v0.25.1)

### Chores

* fix typo ([#449](https://github.com/anthropics/anthropic-sdk-python/issues/449)) ([420a6c5](https://github.com/anthropics/anthropic-sdk-python/commit/420a6c5081ecd58e16b40ca5dfca582aa704c34a))

## 0.25.0 (2024-04-09)

Full Changelog: [v0.24.0...v0.25.0](https://github.com/anthropics/anthropic-sdk-python/compare/v0.24.0...v0.25.0)

### Features

* **bedrock:** add `copy` / `with_options` to bedrock client ([8af7c41](https://github.com/anthropics/anthropic-sdk-python/commit/8af7c41886c9e599a2199e3e496d9d04157699da))


### Chores

* unknown commit message ([8af7c41](https://github.com/anthropics/anthropic-sdk-python/commit/8af7c41886c9e599a2199e3e496d9d04157699da))

## 0.24.0 (2024-04-09)

Full Changelog: [v0.23.1...v0.24.0](https://github.com/anthropics/anthropic-sdk-python/compare/v0.23.1...v0.24.0)

### Features

* **client:** add DefaultHttpxClient and DefaultAsyncHttpxClient ([#444](https://github.com/anthropics/anthropic-sdk-python/issues/444)) ([51d2427](https://github.com/anthropics/anthropic-sdk-python/commit/51d2427c0bb51cbd17d55f827da7fb9cc05f5d06))
* **models:** add to_dict & to_json helper methods ([#446](https://github.com/anthropics/anthropic-sdk-python/issues/446)) ([6709f58](https://github.com/anthropics/anthropic-sdk-python/commit/6709f58d0980669100ea0b7935259d3c05cf9648))

## 0.23.1 (2024-04-04)

Full Changelog: [v0.23.0...v0.23.1](https://github.com/anthropics/anthropic-sdk-python/compare/v0.23.0...v0.23.1)

### Documentation

* **readme:** mention tool use ([#441](https://github.com/anthropics/anthropic-sdk-python/issues/441)) ([e6cd916](https://github.com/anthropics/anthropic-sdk-python/commit/e6cd916b5f4d9cbbae4610828ffb51d81404d74f))

## 0.23.0 (2024-04-04)

Full Changelog: [v0.22.1...v0.23.0](https://github.com/anthropics/anthropic-sdk-python/compare/v0.22.1...v0.23.0)

### Features

* **api:** tool use beta ([#438](https://github.com/anthropics/anthropic-sdk-python/issues/438)) ([5e35ffe](https://github.com/anthropics/anthropic-sdk-python/commit/5e35ffeec0a38055bba2f3998aa3e7c85790627a))

## 0.22.1 (2024-04-04)

Full Changelog: [v0.22.0...v0.22.1](https://github.com/anthropics/anthropic-sdk-python/compare/v0.22.0...v0.22.1)

### Bug Fixes

* **types:** correctly mark type as a required property in requests ([#435](https://github.com/anthropics/anthropic-sdk-python/issues/435)) ([efc35ec](https://github.com/anthropics/anthropic-sdk-python/commit/efc35ec7b87b4e7033509431e828fdf42579f74d))


### Chores

* **types:** consistent naming for text block types ([#437](https://github.com/anthropics/anthropic-sdk-python/issues/437)) ([e979fe1](https://github.com/anthropics/anthropic-sdk-python/commit/e979fe14f868e1bc428440c00092decc590bb545))

## 0.22.0 (2024-04-04)

Full Changelog: [v0.21.3...v0.22.0](https://github.com/anthropics/anthropic-sdk-python/compare/v0.21.3...v0.22.0)

### Features

* **client:** increase default HTTP max_connections to 1000 and max_keepalive_connections to 100 ([#428](https://github.com/anthropics/anthropic-sdk-python/issues/428)) ([9a43940](https://github.com/anthropics/anthropic-sdk-python/commit/9a4394008db937a9ad851589b9adfbd9e15333ef))
* **package:** export default constants ([#423](https://github.com/anthropics/anthropic-sdk-python/issues/423)) ([0d694e1](https://github.com/anthropics/anthropic-sdk-python/commit/0d694e157b040993d937f136c5072c98b87434ff))


### Bug Fixes

* **client:** correct logic for line decoding in streaming ([#433](https://github.com/anthropics/anthropic-sdk-python/issues/433)) ([6bf9379](https://github.com/anthropics/anthropic-sdk-python/commit/6bf93794127a62a077f2e50a2acfe01464742319))
* **project:** use absolute github links on PyPi ([#427](https://github.com/anthropics/anthropic-sdk-python/issues/427)) ([cbd8b1c](https://github.com/anthropics/anthropic-sdk-python/commit/cbd8b1c789e83d2c84ba10165778e4ad2af1ac20))
* revert regression with 3.7 support ([#419](https://github.com/anthropics/anthropic-sdk-python/issues/419)) ([fa21f36](https://github.com/anthropics/anthropic-sdk-python/commit/fa21f3643714d985b10b45dc8bfc3887ed20eba7))
* **streaming:** correct accumulation of output tokens ([#426](https://github.com/anthropics/anthropic-sdk-python/issues/426)) ([b50ed05](https://github.com/anthropics/anthropic-sdk-python/commit/b50ed05a991f02bccfd9f65a1c59e56540adba08))


### Chores

* **client:** validate that max_retries is not None ([#430](https://github.com/anthropics/anthropic-sdk-python/issues/430)) ([31b2a2f](https://github.com/anthropics/anthropic-sdk-python/commit/31b2a2fd4069a670c795eeaf51b641fbf2097af1))
* **internal:** bump dependencies ([#421](https://github.com/anthropics/anthropic-sdk-python/issues/421)) ([30e8031](https://github.com/anthropics/anthropic-sdk-python/commit/30e8031469a4c4beb0bb906920f53d5d4da2e2c3))
* **internal:** defer model build for import latency ([#431](https://github.com/anthropics/anthropic-sdk-python/issues/431)) ([51d4783](https://github.com/anthropics/anthropic-sdk-python/commit/51d47832ae44415604725bb763cf567fb9dc1b34))
* **internal:** formatting change ([#415](https://github.com/anthropics/anthropic-sdk-python/issues/415)) ([1474f44](https://github.com/anthropics/anthropic-sdk-python/commit/1474f443201949c9b8a7d0a8562968d57d421fb5))


### Documentation

* **contributing:** fix typo ([#414](https://github.com/anthropics/anthropic-sdk-python/issues/414)) ([aeaf995](https://github.com/anthropics/anthropic-sdk-python/commit/aeaf99573a9140b6bb5c0af4cefddbd6f469a6a5))
* **readme:** change undocumented params wording ([#429](https://github.com/anthropics/anthropic-sdk-python/issues/429)) ([1336958](https://github.com/anthropics/anthropic-sdk-python/commit/13369583fc74101e002427079c9871e05e5536e8))

## 0.21.3 (2024-03-21)

Full Changelog: [v0.21.2...v0.21.3](https://github.com/anthropics/anthropic-sdk-python/compare/v0.21.2...v0.21.3)

### Bug Fixes

* **types:** correct typo claude-2.1' to claude-2.1 ([#400](https://github.com/anthropics/anthropic-sdk-python/issues/400)) ([7f82aa3](https://github.com/anthropics/anthropic-sdk-python/commit/7f82aa3aa28c7134b69eeb42d5f0b7523c7cb5df))
* **types:** correct typo claude-2.1' to claude-2.1 ([#413](https://github.com/anthropics/anthropic-sdk-python/issues/413)) ([bb1aebe](https://github.com/anthropics/anthropic-sdk-python/commit/bb1aebe6225b7d854b8125344846e77c6e13f3f9))

## 0.21.2 (2024-03-21)

Full Changelog: [v0.21.1...v0.21.2](https://github.com/anthropics/anthropic-sdk-python/compare/v0.21.1...v0.21.2)

### Documentation

* **readme:** consistent use of sentence case in headings ([#405](https://github.com/anthropics/anthropic-sdk-python/issues/405)) ([495ca87](https://github.com/anthropics/anthropic-sdk-python/commit/495ca87e95ac645d4f387614adac1a20c26729b9))
* **readme:** document how to make undocumented requests ([#407](https://github.com/anthropics/anthropic-sdk-python/issues/407)) ([b046d0d](https://github.com/anthropics/anthropic-sdk-python/commit/b046d0dd5be5fc9a21f9ac352627b7bb5e2b9ced))

## 0.21.1 (2024-03-20)

Full Changelog: [v0.21.0...v0.21.1](https://github.com/anthropics/anthropic-sdk-python/compare/v0.21.0...v0.21.1)

### Chores

* **internal:** loosen input type for util function ([#402](https://github.com/anthropics/anthropic-sdk-python/issues/402)) ([9a6ca55](https://github.com/anthropics/anthropic-sdk-python/commit/9a6ca5528ee5b96577df4d657937c35cdc263f85))

## 0.21.0 (2024-03-19)

Full Changelog: [v0.20.0...v0.21.0](https://github.com/anthropics/anthropic-sdk-python/compare/v0.20.0...v0.21.0)

### Features

* **vertex:** api is no longer in private beta ([#399](https://github.com/anthropics/anthropic-sdk-python/issues/399)) ([4cb0e64](https://github.com/anthropics/anthropic-sdk-python/commit/4cb0e6453ed185646b652b7942ed75f8e49be8e3))


### Performance Improvements

* cache TypeAdapters ([#396](https://github.com/anthropics/anthropic-sdk-python/issues/396)) ([a902c47](https://github.com/anthropics/anthropic-sdk-python/commit/a902c472b986d7c7bfda52fc20d737f0bcf80b6a))


### Chores

* **internal:** update generated pragma comment ([#398](https://github.com/anthropics/anthropic-sdk-python/issues/398)) ([330b61e](https://github.com/anthropics/anthropic-sdk-python/commit/330b61eccfd8af3ee587a91dd2491d66abfe159a))


### Documentation

* fix typo in CONTRIBUTING.md ([#397](https://github.com/anthropics/anthropic-sdk-python/issues/397)) ([d46629f](https://github.com/anthropics/anthropic-sdk-python/commit/d46629f385b65a0c099ca7a94ebaae9bcb0ecb2c))
* **helpers:** fix example code ([#391](https://github.com/anthropics/anthropic-sdk-python/issues/391)) ([9fe0c8b](https://github.com/anthropics/anthropic-sdk-python/commit/9fe0c8b9b257d18e7f5fb7ac03de2073552c083d))

## 0.20.0 (2024-03-13)

Full Changelog: [v0.19.2...v0.20.0](https://github.com/anthropics/anthropic-sdk-python/compare/v0.19.2...v0.20.0)

### Features

* **api:** add haiku model ([#390](https://github.com/anthropics/anthropic-sdk-python/issues/390)) ([43b57fc](https://github.com/anthropics/anthropic-sdk-python/commit/43b57fca5426774929bfcac81bf00659740db796))


### Documentation

* **readme:** mention vertex API ([#388](https://github.com/anthropics/anthropic-sdk-python/issues/388)) ([8bb6b98](https://github.com/anthropics/anthropic-sdk-python/commit/8bb6b9841db322db8c5e8357c2c379482be15441))

## 0.19.2 (2024-03-11)

Full Changelog: [v0.19.1...v0.19.2](https://github.com/anthropics/anthropic-sdk-python/compare/v0.19.1...v0.19.2)

### Bug Fixes

* **vertex:** use correct auth scopes ([#385](https://github.com/anthropics/anthropic-sdk-python/issues/385)) ([e4de056](https://github.com/anthropics/anthropic-sdk-python/commit/e4de056ddc24e2d3d8f742124b0a965ff3404341))


### Chores

* export NOT_GIVEN sentinel value ([#379](https://github.com/anthropics/anthropic-sdk-python/issues/379)) ([ba127bc](https://github.com/anthropics/anthropic-sdk-python/commit/ba127bc44b70490a7c9e8ff76b7a742631e94c5c))
* **internal:** improve deserialisation of discriminated unions ([#386](https://github.com/anthropics/anthropic-sdk-python/issues/386)) ([fbc7e0b](https://github.com/anthropics/anthropic-sdk-python/commit/fbc7e0b2cf5e8f5bcd316393a7483509ed9f790e))
* **internal:** support parsing Annotated types ([#377](https://github.com/anthropics/anthropic-sdk-python/issues/377)) ([f44efd5](https://github.com/anthropics/anthropic-sdk-python/commit/f44efd5a587fca5021bfc2c068a715a7a550a5d0))

## 0.19.1 (2024-03-06)

Full Changelog: [v0.19.0...v0.19.1](https://github.com/anthropics/anthropic-sdk-python/compare/v0.19.0...v0.19.1)

### Chores

* **internal:** add core support for deserializing into number response ([#373](https://github.com/anthropics/anthropic-sdk-python/issues/373)) ([b62c422](https://github.com/anthropics/anthropic-sdk-python/commit/b62c4224fafe0544877ebb57278526a5ddd1955d))

## 0.19.0 (2024-03-06)

Full Changelog: [v0.18.1...v0.19.0](https://github.com/anthropics/anthropic-sdk-python/compare/v0.18.1...v0.19.0)

### Features

* **api:** add enum to model param for message ([#371](https://github.com/anthropics/anthropic-sdk-python/issues/371)) ([f96765f](https://github.com/anthropics/anthropic-sdk-python/commit/f96765f188676bb688f599a3574c16dbfb27430c))


### Chores

* **client:** improve error message for invalid http_client argument ([#367](https://github.com/anthropics/anthropic-sdk-python/issues/367)) ([2f4df72](https://github.com/anthropics/anthropic-sdk-python/commit/2f4df724410bc6213bf559739724bec0242becd7))


### Documentation

* **readme:** fix async streaming snippet ([#366](https://github.com/anthropics/anthropic-sdk-python/issues/366)) ([37c469d](https://github.com/anthropics/anthropic-sdk-python/commit/37c469deecad9f6244d42dce7d3cedc289ca129b))

## 0.18.1 (2024-03-04)

Full Changelog: [v0.18.0...v0.18.1](https://github.com/anthropics/anthropic-sdk-python/compare/v0.18.0...v0.18.1)

### Chores

* **readme:** update bedrock example ([#364](https://github.com/anthropics/anthropic-sdk-python/issues/364)) ([81e4d10](https://github.com/anthropics/anthropic-sdk-python/commit/81e4d10f6b7c5e06d5d2844441350731dbddbfad))

## 0.18.0 (2024-03-04)

Full Changelog: [v0.17.0...v0.18.0](https://github.com/anthropics/anthropic-sdk-python/compare/v0.17.0...v0.18.0)

### Features

* **bedrock:** add messages API ([#362](https://github.com/anthropics/anthropic-sdk-python/issues/362)) ([5409be9](https://github.com/anthropics/anthropic-sdk-python/commit/5409be98d0fd4e65e6dd766238fc8789efb3cb49))


### Chores

* remove old examples ([4895381](https://github.com/anthropics/anthropic-sdk-python/commit/489538163ada7de07c3f4b5237c551949fee4232))

## 0.17.0 (2024-03-04)

Full Changelog: [v0.16.0...v0.17.0](https://github.com/anthropics/anthropic-sdk-python/compare/v0.16.0...v0.17.0)

### Features

* **messages:** add support for image inputs ([#359](https://github.com/anthropics/anthropic-sdk-python/issues/359)) ([579f013](https://github.com/anthropics/anthropic-sdk-python/commit/579f013dd294f34b3c44e2b331a4aa25b6cdfd6a))


### Chores

* **client:** use anyio.sleep instead of asyncio.sleep ([#351](https://github.com/anthropics/anthropic-sdk-python/issues/351)) ([2778a22](https://github.com/anthropics/anthropic-sdk-python/commit/2778a2228e82704dde9176d970274e806422c02b))
* **docs:** mention install from git repo ([#356](https://github.com/anthropics/anthropic-sdk-python/issues/356)) ([9d503ba](https://github.com/anthropics/anthropic-sdk-python/commit/9d503ba9cc462e33166594ca19f666819a3a5a87))
* **docs:** remove references to old bedrock package ([#344](https://github.com/anthropics/anthropic-sdk-python/issues/344)) ([3323883](https://github.com/anthropics/anthropic-sdk-python/commit/3323883750b9d61fa084cadc99519b2f6cf8d39c))
* **internal:** bump pyright ([#350](https://github.com/anthropics/anthropic-sdk-python/issues/350)) ([ee0161c](https://github.com/anthropics/anthropic-sdk-python/commit/ee0161c2d7d2fefd06ee5b1001131cd6d6d236d7))
* **internal:** bump rye to v0.24.0 ([#348](https://github.com/anthropics/anthropic-sdk-python/issues/348)) ([be8597b](https://github.com/anthropics/anthropic-sdk-python/commit/be8597b33c2f2f6e8b9ae77738f4c898e48c8e91))
* **internal:** improve bedrock streaming setup ([#354](https://github.com/anthropics/anthropic-sdk-python/issues/354)) ([2b55c68](https://github.com/anthropics/anthropic-sdk-python/commit/2b55c688514e4b13abce547362f0c0a3e7f0e97f))
* **internal:** refactor release environment script ([#347](https://github.com/anthropics/anthropic-sdk-python/issues/347)) ([a87443a](https://github.com/anthropics/anthropic-sdk-python/commit/a87443a90374aedaac80451f61046c6f1aefeaa9))
* **internal:** split up transforms into sync / async ([#357](https://github.com/anthropics/anthropic-sdk-python/issues/357)) ([f55ee71](https://github.com/anthropics/anthropic-sdk-python/commit/f55ee71b0b517f3e605bfd7a4aa948a9c2fc6552))
* **internal:** support more input types ([#358](https://github.com/anthropics/anthropic-sdk-python/issues/358)) ([35b0347](https://github.com/anthropics/anthropic-sdk-python/commit/35b0347bfddecc94fc8ac09b42ff3d96f4523bf8))
* **internal:** update deps ([#349](https://github.com/anthropics/anthropic-sdk-python/issues/349)) ([ab82b2d](https://github.com/anthropics/anthropic-sdk-python/commit/ab82b2d7ce16f3fed4b20e60f0c8e7981c22c191))


### Documentation

* **contributing:** improve wording ([#355](https://github.com/anthropics/anthropic-sdk-python/issues/355)) ([f9093a0](https://github.com/anthropics/anthropic-sdk-python/commit/f9093a0ee8d590185f572749d58280f7eda5ed8b))


### Refactors

* **api:** mark completions API as legacy ([#346](https://github.com/anthropics/anthropic-sdk-python/issues/346)) ([2bb25a1](https://github.com/anthropics/anthropic-sdk-python/commit/2bb25a12509b87557f3da2125ab955b60e32713f))

## 0.16.0 (2024-02-13)

Full Changelog: [v0.15.1...v0.16.0](https://github.com/anthropics/anthropic-sdk-python/compare/v0.15.1...v0.16.0)

### Features

* **api:** messages is generally available ([#343](https://github.com/anthropics/anthropic-sdk-python/issues/343)) ([f682594](https://github.com/anthropics/anthropic-sdk-python/commit/f6825941acc09b33af386b40718bd2f3c01b29ef))
* **messages:** allow message response in params ([#339](https://github.com/anthropics/anthropic-sdk-python/issues/339)) ([86c63f0](https://github.com/anthropics/anthropic-sdk-python/commit/86c63f0e7441a9fe894b3ae7cd7e871060d5ebbf))


### Documentation

* add CONTRIBUTING.md ([#340](https://github.com/anthropics/anthropic-sdk-python/issues/340)) ([78469ad](https://github.com/anthropics/anthropic-sdk-python/commit/78469ade1658bf6b12b7cb947136e228d6992303))

## 0.15.1 (2024-02-07)

Full Changelog: [v0.15.0...v0.15.1](https://github.com/anthropics/anthropic-sdk-python/compare/v0.15.0...v0.15.1)

### Bug Fixes

* prevent crash when platform.architecture() is not allowed ([#334](https://github.com/anthropics/anthropic-sdk-python/issues/334)) ([fefb5c1](https://github.com/anthropics/anthropic-sdk-python/commit/fefb5c10c10054f28fcccf0d9f44204de93e9fe3))
* **types:** loosen most List params types to Iterable ([#338](https://github.com/anthropics/anthropic-sdk-python/issues/338)) ([6e7761b](https://github.com/anthropics/anthropic-sdk-python/commit/6e7761b89c9ef226bd8f7df465445526c08fdb2f))


### Chores

* **internal:** add lint command ([#337](https://github.com/anthropics/anthropic-sdk-python/issues/337)) ([2ebaf1d](https://github.com/anthropics/anthropic-sdk-python/commit/2ebaf1d6a85b638b502661735e3ffc5b58d5c241))
* **internal:** support serialising iterable types ([#336](https://github.com/anthropics/anthropic-sdk-python/issues/336)) ([ea3ed7b](https://github.com/anthropics/anthropic-sdk-python/commit/ea3ed7b8b91314721129480d164d7bf3bafec26c))

## 0.15.0 (2024-02-02)

Full Changelog: [v0.14.1...v0.15.0](https://github.com/anthropics/anthropic-sdk-python/compare/v0.14.1...v0.15.0)

### Features

* **api:** add new usage response fields ([#332](https://github.com/anthropics/anthropic-sdk-python/issues/332)) ([554098e](https://github.com/anthropics/anthropic-sdk-python/commit/554098e544d49575d2d9d24edfb46f2fa0f77ba1))

## 0.14.1 (2024-02-02)

Full Changelog: [v0.14.0...v0.14.1](https://github.com/anthropics/anthropic-sdk-python/compare/v0.14.0...v0.14.1)

### Chores

* **interal:** make link to api.md relative ([#330](https://github.com/anthropics/anthropic-sdk-python/issues/330)) ([e393317](https://github.com/anthropics/anthropic-sdk-python/commit/e393317362d8cd74442d7a802ea965211c913115))

## 0.14.0 (2024-01-31)

Full Changelog: [v0.13.0...v0.14.0](https://github.com/anthropics/anthropic-sdk-python/compare/v0.13.0...v0.14.0)

### Features

* **bedrock:** include bedrock SDK ([#328](https://github.com/anthropics/anthropic-sdk-python/issues/328)) ([a03f21f](https://github.com/anthropics/anthropic-sdk-python/commit/a03f21fef1ab3225f9839002b69aa5cb5840b375))

## 0.13.0 (2024-01-30)

Full Changelog: [v0.12.0...v0.13.0](https://github.com/anthropics/anthropic-sdk-python/compare/v0.12.0...v0.13.0)

### Features

* **client:** support parsing custom response types ([#325](https://github.com/anthropics/anthropic-sdk-python/issues/325)) ([416633f](https://github.com/anthropics/anthropic-sdk-python/commit/416633fedb962d207fb841e80d7d7947fe52bb33))


### Chores

* **internal:** cast type in mocked test ([#326](https://github.com/anthropics/anthropic-sdk-python/issues/326)) ([fd22d8e](https://github.com/anthropics/anthropic-sdk-python/commit/fd22d8e584c5f3d6a029b4b0e87b98827746fda9))
* **internal:** enable ruff type checking misuse lint rule ([#324](https://github.com/anthropics/anthropic-sdk-python/issues/324)) ([6587598](https://github.com/anthropics/anthropic-sdk-python/commit/6587598162387c0aada958df22610a93198e813d))
* **internal:** support multipart data with overlapping keys ([#322](https://github.com/anthropics/anthropic-sdk-python/issues/322)) ([9ecab60](https://github.com/anthropics/anthropic-sdk-python/commit/9ecab6048afeca544146b9629bcdaa5250012cc9))
* **internal:** support pre-release versioning ([#327](https://github.com/anthropics/anthropic-sdk-python/issues/327)) ([78b1bfe](https://github.com/anthropics/anthropic-sdk-python/commit/78b1bfe3e694e0400477fc25ae1aaab34c28e61e))

## 0.12.0 (2024-01-25)

Full Changelog: [v0.11.0...v0.12.0](https://github.com/anthropics/anthropic-sdk-python/compare/v0.11.0...v0.12.0)

### Features

* **client:** enable follow redirects by default ([#320](https://github.com/anthropics/anthropic-sdk-python/issues/320)) ([9959c32](https://github.com/anthropics/anthropic-sdk-python/commit/9959c32d24acd7199e6ce8124a18bcfa263fac85))

## 0.11.0 (2024-01-23)

Full Changelog: [v0.10.0...v0.11.0](https://github.com/anthropics/anthropic-sdk-python/compare/v0.10.0...v0.11.0)

### Features

* **vertex:** add support for google vertex ([#319](https://github.com/anthropics/anthropic-sdk-python/issues/319)) ([5324415](https://github.com/anthropics/anthropic-sdk-python/commit/53244155d657e782d4ec9cc85f557233ee3698be))


### Chores

* **internal:** add internal helpers ([#316](https://github.com/anthropics/anthropic-sdk-python/issues/316)) ([8c75cdf](https://github.com/anthropics/anthropic-sdk-python/commit/8c75cdfe5e236c08bb6ecc09e27f69932cc523f1))
* **internal:** update resource client type ([#318](https://github.com/anthropics/anthropic-sdk-python/issues/318)) ([bdd8d84](https://github.com/anthropics/anthropic-sdk-python/commit/bdd8d84023814f390b8f5eca7bd64cb340c1e8a8))

## 0.10.0 (2024-01-18)

Full Changelog: [v0.9.0...v0.10.0](https://github.com/anthropics/anthropic-sdk-python/compare/v0.9.0...v0.10.0)

### Features

* **client:** add support for streaming raw responses ([#307](https://github.com/anthropics/anthropic-sdk-python/issues/307)) ([f295982](https://github.com/anthropics/anthropic-sdk-python/commit/f2959827fe2cd555db38a62c1b3df1a12e6dee40))


### Bug Fixes

* **ci:** ignore stainless-app edits to release PR title ([#315](https://github.com/anthropics/anthropic-sdk-python/issues/315)) ([69e8b03](https://github.com/anthropics/anthropic-sdk-python/commit/69e8b03cd12e3c12de7c528a0b2c064f709a239a))


### Chores

* add write_to_file binary helper method ([#309](https://github.com/anthropics/anthropic-sdk-python/issues/309)) ([8ac7988](https://github.com/anthropics/anthropic-sdk-python/commit/8ac7988dee11745495290f38fa5a2b8fddd0b993))
* **client:** improve debug logging for failed requests ([#303](https://github.com/anthropics/anthropic-sdk-python/issues/303)) ([5e58c25](https://github.com/anthropics/anthropic-sdk-python/commit/5e58c2537eccadbccef9aadcd6433cf35328e678))
* **internal:** fix typing util function ([#310](https://github.com/anthropics/anthropic-sdk-python/issues/310)) ([3671aa6](https://github.com/anthropics/anthropic-sdk-python/commit/3671aa6b3b05776b727a727020366bb6c349f66a))
* **internal:** remove redundant client test ([#311](https://github.com/anthropics/anthropic-sdk-python/issues/311)) ([d7140f7](https://github.com/anthropics/anthropic-sdk-python/commit/d7140f7c16554dfacdac642173516625f2540496))
* **internal:** share client instances between all tests ([#314](https://github.com/anthropics/anthropic-sdk-python/issues/314)) ([ccf731b](https://github.com/anthropics/anthropic-sdk-python/commit/ccf731b047809264d073f86c08c7f36ee360fda1))
* **internal:** speculative retry-after-ms support ([#312](https://github.com/anthropics/anthropic-sdk-python/issues/312)) ([4b27da9](https://github.com/anthropics/anthropic-sdk-python/commit/4b27da9d05ce90944f566c20b122653adc0b9ab1))
* **internal:** updates to proxy helper ([#308](https://github.com/anthropics/anthropic-sdk-python/issues/308)) ([a0b3cdb](https://github.com/anthropics/anthropic-sdk-python/commit/a0b3cdb655d150d3703f793c82e4a3945f45c82f))
* lazy load raw resource class properties ([#313](https://github.com/anthropics/anthropic-sdk-python/issues/313)) ([b13f824](https://github.com/anthropics/anthropic-sdk-python/commit/b13f8249be1a4f77611598b4cce465481af35d83))


### Documentation

* **readme:** improve api reference ([#306](https://github.com/anthropics/anthropic-sdk-python/issues/306)) ([c3ab836](https://github.com/anthropics/anthropic-sdk-python/commit/c3ab836e4654dff259f19071bf0e1cdff249a268))

## 0.9.0 (2024-01-08)

Full Changelog: [v0.8.1...v0.9.0](https://github.com/anthropics/anthropic-sdk-python/compare/v0.8.1...v0.9.0)

### Features

* add `None` default value to nullable response properties ([#299](https://github.com/anthropics/anthropic-sdk-python/issues/299)) ([da423db](https://github.com/anthropics/anthropic-sdk-python/commit/da423db5c14b213c52fe0986981c4f01aff0d2c3))


### Bug Fixes

* **client:** correctly use custom http client auth ([#296](https://github.com/anthropics/anthropic-sdk-python/issues/296)) ([6289d6e](https://github.com/anthropics/anthropic-sdk-python/commit/6289d6e205f872c02114f05333d5426055f2416f))


### Chores

* add .keep files for examples and custom code directories ([#302](https://github.com/anthropics/anthropic-sdk-python/issues/302)) ([73a07ea](https://github.com/anthropics/anthropic-sdk-python/commit/73a07ea7a5254d205b68e25c46c1f2267604ac9b))
* **internal:** loosen type var restrictions ([#301](https://github.com/anthropics/anthropic-sdk-python/issues/301)) ([5e5e1e7](https://github.com/anthropics/anthropic-sdk-python/commit/5e5e1e716a8732af66e2234307521b4620b07361))
* **internal:** replace isort with ruff ([#298](https://github.com/anthropics/anthropic-sdk-python/issues/298)) ([7c60904](https://github.com/anthropics/anthropic-sdk-python/commit/7c60904f5da10c4ef6ab8af4e8631bc938b35131))
* use property declarations for resource members ([#300](https://github.com/anthropics/anthropic-sdk-python/issues/300)) ([8671297](https://github.com/anthropics/anthropic-sdk-python/commit/8671297b87105635accefd574c44dbffd8a4f9e9))

## 0.8.1 (2023-12-22)

Full Changelog: [v0.8.0...v0.8.1](https://github.com/anthropics/anthropic-sdk-python/compare/v0.8.0...v0.8.1)

### Chores

* **internal:** add bin script ([#292](https://github.com/anthropics/anthropic-sdk-python/issues/292)) ([ba2953d](https://github.com/anthropics/anthropic-sdk-python/commit/ba2953dcaa8a8fcebaa7e8891304687c95b17499))
* **internal:** fix typos ([#287](https://github.com/anthropics/anthropic-sdk-python/issues/287)) ([4ffbcdf](https://github.com/anthropics/anthropic-sdk-python/commit/4ffbcdf1d3c8c2fbaf7152d207b24cdb0ea82ac9))
* **internal:** use ruff instead of black for formatting ([#294](https://github.com/anthropics/anthropic-sdk-python/issues/294)) ([1753887](https://github.com/anthropics/anthropic-sdk-python/commit/1753887a776f41bdc2d648329cfe6f20c91125e5))
* **package:** bump minimum typing-extensions to 4.7 ([#290](https://github.com/anthropics/anthropic-sdk-python/issues/290)) ([9ec5c57](https://github.com/anthropics/anthropic-sdk-python/commit/9ec5c57ba9a14a769d540e48755b05a1c190b45b))


### Documentation

* **messages:** improvements to helpers reference + typos ([#291](https://github.com/anthropics/anthropic-sdk-python/issues/291)) ([d18a895](https://github.com/anthropics/anthropic-sdk-python/commit/d18a895d380fc0c6610443486d73247b0cd97376))
* **readme:** remove old migration guide ([#289](https://github.com/anthropics/anthropic-sdk-python/issues/289)) ([eec4574](https://github.com/anthropics/anthropic-sdk-python/commit/eec4574f1f6668804c88bda67b901db10400fbc3))

## 0.8.0 (2023-12-19)

Full Changelog: [v0.7.8...v0.8.0](https://github.com/anthropics/anthropic-sdk-python/compare/v0.7.8...v0.8.0)

### Features

* **api:** add messages endpoint with streaming helpers ([#286](https://github.com/anthropics/anthropic-sdk-python/issues/286)) ([c464b87](https://github.com/anthropics/anthropic-sdk-python/commit/c464b87b72ebbf9255418a02c627b0f0c52d03dd))


### Chores

* **ci:** run release workflow once per day ([#282](https://github.com/anthropics/anthropic-sdk-python/issues/282)) ([3a23912](https://github.com/anthropics/anthropic-sdk-python/commit/3a239127713c68ae53fa8b338e1f60ca25840a90))
* **client:** only import tokenizers when needed ([#284](https://github.com/anthropics/anthropic-sdk-python/issues/284)) ([b9e38b2](https://github.com/anthropics/anthropic-sdk-python/commit/b9e38b2a2e2be2b5fb31842fa409b95abcbccbc6))
* **streaming:** update constructor to use direct client names ([#285](https://github.com/anthropics/anthropic-sdk-python/issues/285)) ([0c55c84](https://github.com/anthropics/anthropic-sdk-python/commit/0c55c84ab3527199401f387fbc3338572b264fef))

## 0.7.8 (2023-12-12)

Full Changelog: [v0.7.7...v0.7.8](https://github.com/anthropics/anthropic-sdk-python/compare/v0.7.7...v0.7.8)

### Bug Fixes

* avoid leaking memory when Client.with_options is used ([#275](https://github.com/anthropics/anthropic-sdk-python/issues/275)) ([5e51ebd](https://github.com/anthropics/anthropic-sdk-python/commit/5e51ebdbc6e5c23c8c237b5e0231ef66f585f964))
* **client:** correct base_url setter implementation ([#265](https://github.com/anthropics/anthropic-sdk-python/issues/265)) ([29d0c8b](https://github.com/anthropics/anthropic-sdk-python/commit/29d0c8b0eb174b499a904e02cce7fe7a6aaa1a01))
* **client:** ensure retried requests are closed ([#261](https://github.com/anthropics/anthropic-sdk-python/issues/261)) ([5d9aa75](https://github.com/anthropics/anthropic-sdk-python/commit/5d9aa754ace5d53eb90c1055dd6b1ca8e7deee4f))
* **errors:** properly assign APIError.body ([#274](https://github.com/anthropics/anthropic-sdk-python/issues/274)) ([342846f](https://github.com/anthropics/anthropic-sdk-python/commit/342846fa4d424a4d18dd2289d2b652bf53c97901))


### Chores

* **internal:** enable more lint rules ([#273](https://github.com/anthropics/anthropic-sdk-python/issues/273)) ([0ac62bc](https://github.com/anthropics/anthropic-sdk-python/commit/0ac62bc127ddf0367561427836ff19c1272fb0e1))
* **internal:** reformat imports ([#270](https://github.com/anthropics/anthropic-sdk-python/issues/270)) ([dc55724](https://github.com/anthropics/anthropic-sdk-python/commit/dc55724673dfa59911a05fe4827b8804beba0b05))
* **internal:** reformat imports ([#272](https://github.com/anthropics/anthropic-sdk-python/issues/272)) ([0d82ce4](https://github.com/anthropics/anthropic-sdk-python/commit/0d82ce4784c3a6c9599e6c09b8190e97ea028dc3))
* **internal:** remove unused file ([#264](https://github.com/anthropics/anthropic-sdk-python/issues/264)) ([1bfc69b](https://github.com/anthropics/anthropic-sdk-python/commit/1bfc69b0e2a1eb79598409cbfcba060f699d28a7))
* **internal:** replace string concatenation with f-strings ([#263](https://github.com/anthropics/anthropic-sdk-python/issues/263)) ([f545c35](https://github.com/anthropics/anthropic-sdk-python/commit/f545c350dd802079d057d34ff29444e32dc7bdcb))
* **internal:** update formatting ([#271](https://github.com/anthropics/anthropic-sdk-python/issues/271)) ([802ab59](https://github.com/anthropics/anthropic-sdk-python/commit/802ab59401b06986b8023e9ef0d0f9e0d6858b86))
* **package:** lift anyio v4 restriction ([#266](https://github.com/anthropics/anthropic-sdk-python/issues/266)) ([a217e99](https://github.com/anthropics/anthropic-sdk-python/commit/a217e9955569852d35ab1bc1351dd66ba807fc44))


### Documentation

* update examples to show claude-2.1 ([#276](https://github.com/anthropics/anthropic-sdk-python/issues/276)) ([8f562f4](https://github.com/anthropics/anthropic-sdk-python/commit/8f562f47f13ffaaab93f08b9b4c59d06e4a18b6c))


### Refactors

* **client:** simplify cleanup ([#278](https://github.com/anthropics/anthropic-sdk-python/issues/278)) ([3611ae2](https://github.com/anthropics/anthropic-sdk-python/commit/3611ae24d93fa33e55f2e9193a3c787bfd041da5))
* simplify internal error handling ([#279](https://github.com/anthropics/anthropic-sdk-python/issues/279)) ([993b51a](https://github.com/anthropics/anthropic-sdk-python/commit/993b51aa4f41bae3938a12d60919065c4865a734))

## 0.7.7 (2023-11-29)

Full Changelog: [v0.7.6...v0.7.7](https://github.com/anthropics/anthropic-sdk-python/compare/v0.7.6...v0.7.7)

### Chores

* **internal:** add tests for proxy change ([#260](https://github.com/anthropics/anthropic-sdk-python/issues/260)) ([3b52136](https://github.com/anthropics/anthropic-sdk-python/commit/3b521362f6ee33c3ff66371e4f2d3bdcea2827bb))
* **internal:** updates to proxy helper ([#258](https://github.com/anthropics/anthropic-sdk-python/issues/258)) ([94c4de8](https://github.com/anthropics/anthropic-sdk-python/commit/94c4de88b9d202d780c4dfbee6db138d7a663373))

## 0.7.6 (2023-11-28)

Full Changelog: [v0.7.5...v0.7.6](https://github.com/anthropics/anthropic-sdk-python/compare/v0.7.5...v0.7.6)

### Chores

* **deps:** bump mypy to v1.7.1 ([#256](https://github.com/anthropics/anthropic-sdk-python/issues/256)) ([02d4ed8](https://github.com/anthropics/anthropic-sdk-python/commit/02d4ed8ae8e4fb9221fc9bfb5f45357ed239de5e))

## 0.7.5 (2023-11-24)

Full Changelog: [v0.7.4...v0.7.5](https://github.com/anthropics/anthropic-sdk-python/compare/v0.7.4...v0.7.5)

### Chores

* **internal:** revert recent options change ([#252](https://github.com/anthropics/anthropic-sdk-python/issues/252)) ([d60d5c3](https://github.com/anthropics/anthropic-sdk-python/commit/d60d5c33aec2964b3dbbc69bdf8556b4100a684f))
* **internal:** send more detailed x-stainless headers ([#254](https://github.com/anthropics/anthropic-sdk-python/issues/254)) ([a268d4b](https://github.com/anthropics/anthropic-sdk-python/commit/a268d4bf4f2fb17707c5328e1ba25e623e7b9b78))

## 0.7.4 (2023-11-23)

Full Changelog: [v0.7.3...v0.7.4](https://github.com/anthropics/anthropic-sdk-python/compare/v0.7.3...v0.7.4)

### Chores

* **internal:** options updates ([#248](https://github.com/anthropics/anthropic-sdk-python/issues/248)) ([5a3b236](https://github.com/anthropics/anthropic-sdk-python/commit/5a3b2362af3b7556babb99095df88443c56579ec))

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
