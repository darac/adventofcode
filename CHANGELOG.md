# CHANGELOG


## v2024.2.0 (2024-12-03)

### Build System

- Remove requirements.txt
  ([`e55f8d4`](https://github.com/darac/adventofcode/commit/e55f8d47c44560c00faa75573e12650ab0744e68))

### Chores

- **deps**: Update docker/build-push-action digest to 48aba3b
  ([#132](https://github.com/darac/adventofcode/pull/132),
  [`3c5af61`](https://github.com/darac/adventofcode/commit/3c5af612498ba72e91792777c589fd53c82dde61))

Co-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>

- **deps**: Update docker/dockerfile docker tag to v1.12
  ([#136](https://github.com/darac/adventofcode/pull/136),
  [`ed1ab92`](https://github.com/darac/adventofcode/commit/ed1ab92927ba9fc05b1fd652cccc74db8c70ee3c))

- **deps**: Update docker/login-action digest to 7ca3450
  ([#133](https://github.com/darac/adventofcode/pull/133),
  [`55a42c2`](https://github.com/darac/adventofcode/commit/55a42c22be53705527275dcff0c6a45be0fe66c9))

Co-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>

- **deps**: Update docker/metadata-action digest to b53be03
  ([#135](https://github.com/darac/adventofcode/pull/135),
  [`745f22c`](https://github.com/darac/adventofcode/commit/745f22c300c934ef3a7bdb7b9b0211c3836b4f57))

- **deps**: Update python-semantic-release/publish-action action to v9.15.0
  ([#137](https://github.com/darac/adventofcode/pull/137),
  [`2e3ea44`](https://github.com/darac/adventofcode/commit/2e3ea4422f4634861d8c6691efe339c686aaee5e))

- **deps**: Update python-semantic-release/python-semantic-release action to v9.15.0
  ([#138](https://github.com/darac/adventofcode/pull/138),
  [`f5f7b86`](https://github.com/darac/adventofcode/commit/f5f7b869209017acaa19693909c5819a51e13a40))

### Continuous Integration

- Don't build docker image on PRs
  ([`7ba1255`](https://github.com/darac/adventofcode/commit/7ba1255cc4227edbc1f90c7762a710dea76d33b7))

- Update to 2024 leaderboard
  ([`166272e`](https://github.com/darac/adventofcode/commit/166272eeb3fa571e22586ebb7622825712ed904e))

### Features

- 2024 Day 3 complete
  ([`1abd3bf`](https://github.com/darac/adventofcode/commit/1abd3bfe9041733749da7fa1342d271c21612e39))

### Refactoring

- **deps**: Remove bpython as a dependency
  ([`d803816`](https://github.com/darac/adventofcode/commit/d80381617d9ef89dee6c37e2fa6be52b12375c0a))

### Testing

- Define a coheret test id
  ([`86351ae`](https://github.com/darac/adventofcode/commit/86351ae8ee9d5505e4b184fb080e189a88cc2580))


## v2024.1.0 (2024-12-02)

### Features

- 2024 Day 2 complete
  ([`9d1d3e1`](https://github.com/darac/adventofcode/commit/9d1d3e15cec4ef19b5ed3337c083e97651546ec2))

### Testing

- Increase coverage
  ([`fd46040`](https://github.com/darac/adventofcode/commit/fd460401ec6274326217c0656f2eaac343c0840d))


## v2024.0.0 (2024-12-01)

### Features

- 2024 day 1 complete
  ([`4e809de`](https://github.com/darac/adventofcode/commit/4e809de688755c0a14629b9829527885e36672ef))

BREAKING CHANGE: A new year begins!

### BREAKING CHANGES

- A new year begins!


## v2023.4.3 (2024-11-25)

### Bug Fixes

- Checkout before installing UV
  ([`ef90254`](https://github.com/darac/adventofcode/commit/ef90254b4d05b68f6ef70dc8def5c89569fcde12))

- Install UV for release
  ([`548723a`](https://github.com/darac/adventofcode/commit/548723a9e485a9f9b7dab70a9f392d6b43e4a41a))

- Semantic-release needs the package name specified
  ([`0409bde`](https://github.com/darac/adventofcode/commit/0409bde6347513144483fa6588b1bbe24ac0479b))

### Chores

- Bump versions
  ([`1eb28a3`](https://github.com/darac/adventofcode/commit/1eb28a363c20cf1d0812f12cdf35c74c82a87193))

- Force Python version
  ([`c4f9a9a`](https://github.com/darac/adventofcode/commit/c4f9a9a4ac04f80c33666f4bb88cc0c9ca788e0e))

- Upload to git
  ([`8d239f9`](https://github.com/darac/adventofcode/commit/8d239f9873002174a29b61f2cc83f97582b90ada))

- Use recommended release workflow
  ([`4b99cc9`](https://github.com/darac/adventofcode/commit/4b99cc9498b43b852778419e9b4b94d1102a3db3))

- **github-actions**: Add release-drafter ([#96](https://github.com/darac/adventofcode/pull/96),
  [`c36a7ac`](https://github.com/darac/adventofcode/commit/c36a7ac3606b80fd8273b9ee69dbe2aacbbc39e6))

* chore(github-actions): add release-drafter

* chore: Switch to using UV

* chore(github-actions): Fix test workflow

* chore(github-actions): Do a UV sync

* chore(github-actions): Deduplicate proj-version step

* chore(github-actions,dependencies): Add Dev Dependencies

* chore(github-actions): Read the project version from the TOML

* chore(github-actions): Build using the right variable

* chore(github-actions): Add CA certificates

- **github-actions**: Install UV for semantic-release
  ([#98](https://github.com/darac/adventofcode/pull/98),
  [`5e4e03d`](https://github.com/darac/adventofcode/commit/5e4e03dab7367be8f9b4e70ed3b39e7ce4a94645))

### Code Style

- Enable more ruff fixes
  ([`1f4fd62`](https://github.com/darac/adventofcode/commit/1f4fd628993bf29aef5e7b77de8f28c906abeda1))


## v2023.4.2 (2023-12-06)


## v2023.1.0 (2023-12-01)


## v2022.10.5 (2023-10-18)


## v2022.10.3 (2023-10-05)
