# CHANGELOG


## v2024.4.4 (2025-05-11)

### Bug Fixes

- Patch some newer Ruff recommendations
  ([`a957ac6`](https://github.com/darac/adventofcode/commit/a957ac662a55388d0eef4c4e33eeb29091d59131))

- **ci**: Always upload Test reports
  ([`838d4a3`](https://github.com/darac/adventofcode/commit/838d4a3edf82bf99e2980daf1111ca7fed68a52d))

- **ci**: Run Test Reporter after tests, not after sonar
  ([`45afab0`](https://github.com/darac/adventofcode/commit/45afab00736d1c1f80d3841988b4a9ed6db0efef))

### Build System

- **deps**: Bump astral-sh/setup-uv from 5 to 6
  ([`7f64856`](https://github.com/darac/adventofcode/commit/7f64856d8e19f0f94d6cc79800ec7db2aca65cc0))

Bumps [astral-sh/setup-uv](https://github.com/astral-sh/setup-uv) from 5 to 6. - [Release
  notes](https://github.com/astral-sh/setup-uv/releases) -
  [Commits](https://github.com/astral-sh/setup-uv/compare/v5...v6)

--- updated-dependencies: - dependency-name: astral-sh/setup-uv dependency-version: '6'

dependency-type: direct:production

update-type: version-update:semver-major ...

Signed-off-by: dependabot[bot] <support@github.com>

### Chores

- **deps**: Update lock file
  ([`f244513`](https://github.com/darac/adventofcode/commit/f24451327c282a6ec823f9e0d1e3eabca8b9e886))


## v2024.4.3 (2025-04-07)

### Bug Fixes

- Attempt to get y2022d07 to work on Windows
  ([`2d63080`](https://github.com/darac/adventofcode/commit/2d63080d2e630ce9e3a4fc21efeb427cd1cef4e1))

- Attempt to get y2022d07 to work on Windows
  ([`6708fab`](https://github.com/darac/adventofcode/commit/6708faba4c24874783099474a45ee86ca9a014ab))

- Disable testing on Windows
  ([`b1889d0`](https://github.com/darac/adventofcode/commit/b1889d0ed308dea94f3f86728c7157cf3b6778ab))

- Tidy up mypy checks
  ([`e4b1903`](https://github.com/darac/adventofcode/commit/e4b1903e92951fc8e41b028af326ae3b767a5b49))

- Update pandas deprecations
  ([`ce6fd4a`](https://github.com/darac/adventofcode/commit/ce6fd4aec93931d33ca5e4bcaf5a458097edb644))

- **ci**: Attempt to fix GH builds
  ([`cdd4293`](https://github.com/darac/adventofcode/commit/cdd4293cd2c998927ec026d6525d383aa4182a52))

- **ci**: Copy Coverage reports, too
  ([`d801f6e`](https://github.com/darac/adventofcode/commit/d801f6e4cf86522353befeb675e430957eb8e84c))

- **ci**: Disable uv-venv-lock-runner until it's fixed
  ([`fec87df`](https://github.com/darac/adventofcode/commit/fec87df0af8218170b3d6ede1f1e476a9cbb2b0b))

- **ci**: Don't use tox-gh for now
  ([`20cf77f`](https://github.com/darac/adventofcode/commit/20cf77fbce895535f9afd20899a1257e8ab22fec))

- **ci**: Download all artifacts
  ([`02e4720`](https://github.com/darac/adventofcode/commit/02e472070791e7f28e4c2f1245db6a1c315c24e9))

- **ci**: Import JUnit and Ruff reports into sonar
  ([`d5c7bc6`](https://github.com/darac/adventofcode/commit/d5c7bc61f03d3ec5e3b66ab189f95ab18d9d9e10))

- **ci**: Show downloaded artifacts
  ([`7171717`](https://github.com/darac/adventofcode/commit/7171717bfe164f0d29944691111297ecee20e566))

- **ci**: Specify multiple paths correctly
  ([`adcc6df`](https://github.com/darac/adventofcode/commit/adcc6df68523e7795a9c93403e835488e3347b3e))

- **ci**: Try to work around download-artifact bugs
  ([`e869436`](https://github.com/darac/adventofcode/commit/e8694361fdf614e5b52252d0c2c22ddeec0f79fc))

### Build System

- **deps**: Bump docker/login-action
  ([`bbd55a9`](https://github.com/darac/adventofcode/commit/bbd55a929e5540cb322cf38a91eaa271fefedceb))

Bumps [docker/login-action](https://github.com/docker/login-action) from
  327cd5a69de6c009b9ce71bce8395f28e651bf99 to 74a5d142397b4f367a81961eba4e8cd7edddf772. - [Release
  notes](https://github.com/docker/login-action/releases) -
  [Commits](https://github.com/docker/login-action/compare/327cd5a69de6c009b9ce71bce8395f28e651bf99...74a5d142397b4f367a81961eba4e8cd7edddf772)

--- updated-dependencies: - dependency-name: docker/login-action dependency-type: direct:production
  ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump python-semantic-release/publish-action
  ([`36b4795`](https://github.com/darac/adventofcode/commit/36b4795a4b3d3d5e4764829613d3775c5bde7049))

Bumps
  [python-semantic-release/publish-action](https://github.com/python-semantic-release/publish-action)
  from 9.16.1 to 9.17.0. - [Release
  notes](https://github.com/python-semantic-release/publish-action/releases) -
  [Changelog](https://github.com/python-semantic-release/publish-action/blob/main/releaserc.toml) -
  [Commits](https://github.com/python-semantic-release/publish-action/compare/v9.16.1...v9.17.0)

--- updated-dependencies: - dependency-name: python-semantic-release/publish-action dependency-type:
  direct:production

update-type: version-update:semver-minor ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump python-semantic-release/python-semantic-release
  ([`4347751`](https://github.com/darac/adventofcode/commit/4347751787530e2d371ab9ece060356709f0b096))

Bumps
  [python-semantic-release/python-semantic-release](https://github.com/python-semantic-release/python-semantic-release)
  from 9.16.1 to 9.17.0. - [Release
  notes](https://github.com/python-semantic-release/python-semantic-release/releases) -
  [Changelog](https://github.com/python-semantic-release/python-semantic-release/blob/master/CHANGELOG.rst)
  -
  [Commits](https://github.com/python-semantic-release/python-semantic-release/compare/v9.16.1...v9.17.0)

--- updated-dependencies: - dependency-name: python-semantic-release/python-semantic-release
  dependency-type: direct:production

update-type: version-update:semver-minor ...

Signed-off-by: dependabot[bot] <support@github.com>

### Chores

- **deps**: Update astral-sh/setup-uv action to v5
  ([`11c1c3d`](https://github.com/darac/adventofcode/commit/11c1c3dde4c082618af482c367137e20498fc8d6))

- **deps**: Update docker/build-push-action digest to 0adf995
  ([`690dedc`](https://github.com/darac/adventofcode/commit/690dedca0bbafbfd2d78b8121a9e54b6898f1101))

- **deps**: Update docker/build-push-action digest to 31ca4e5
  ([`54b7621`](https://github.com/darac/adventofcode/commit/54b7621785b65499955e578ae131caf9c3b97e28))

- **deps**: Update docker/build-push-action digest to 471d1dc
  ([`ca349f4`](https://github.com/darac/adventofcode/commit/ca349f45f1b3fab91894568f1abf11248356f926))

- **deps**: Update docker/build-push-action digest to 7e09459
  ([`aaafb96`](https://github.com/darac/adventofcode/commit/aaafb962402131dcf9669c2d5b97782f7834f0a9))

- **deps**: Update docker/build-push-action digest to 84ad562
  ([`fc9f8e3`](https://github.com/darac/adventofcode/commit/fc9f8e3c6249e6aca1d3802af65f4506cefd07df))

- **deps**: Update docker/build-push-action digest to b16f42f
  ([`19f5908`](https://github.com/darac/adventofcode/commit/19f590824a57521a7e247199d0228af6a5bfd044))

- **deps**: Update docker/build-push-action digest to ca877d9
  ([`5e46239`](https://github.com/darac/adventofcode/commit/5e46239cd2f83744abfc0365b3ee8d2c917b01aa))

- **deps**: Update docker/dockerfile docker tag to v1.13
  ([`5aaaed7`](https://github.com/darac/adventofcode/commit/5aaaed75115f084e19e59cf4eb8bda17b0e9b60c))

- **deps**: Update docker/dockerfile docker tag to v1.14
  ([`74d5bd6`](https://github.com/darac/adventofcode/commit/74d5bd65c68c4eae98dbab2880c73a0416274f71))

- **deps**: Update docker/login-action digest to 327cd5a
  ([`077c894`](https://github.com/darac/adventofcode/commit/077c89499efa508c94ada5dd47447b707744c621))

- **deps**: Update docker/login-action digest to 74a5d14
  ([`96db97b`](https://github.com/darac/adventofcode/commit/96db97bc53768a21273d7b156a62fe2b779bd4f4))

- **deps**: Update docker/metadata-action digest to 8e1d546
  ([`f0dfdd9`](https://github.com/darac/adventofcode/commit/f0dfdd9c38b750a9f5341e2047b3dac43b01977e))

- **deps**: Update docker/metadata-action digest to 902fa8e
  ([`43415f9`](https://github.com/darac/adventofcode/commit/43415f9076c3b84eb8749744585140b6990fab15))

- **deps**: Update pre-commit hook astral-sh/ruff-pre-commit to v0.11.3
  ([`0748697`](https://github.com/darac/adventofcode/commit/0748697f9c4b958bec7b9faf42e3df389db69ab3))

- **deps**: Update pre-commit hook astral-sh/uv-pre-commit to v0.6.12
  ([`dc1ad90`](https://github.com/darac/adventofcode/commit/dc1ad900bd961550c62a1c3792f7a60e2ce86f59))

- **deps**: Update pre-commit hook gitleaks/gitleaks to v8.24.2
  ([`47edcdb`](https://github.com/darac/adventofcode/commit/47edcdb32b09f545f90077f74c0ffa58014b546a))

- **deps**: Update python-semantic-release/publish-action action to v9.16.1
  ([`46017a6`](https://github.com/darac/adventofcode/commit/46017a6226945197fdb1ddd8757f1f1610d13ce4))

- **deps**: Update python-semantic-release/publish-action action to v9.18.1
  ([`fa36fa6`](https://github.com/darac/adventofcode/commit/fa36fa67aff6480562ca46275cba856dcf43c8a6))

- **deps**: Update python-semantic-release/publish-action action to v9.20.0
  ([`f5477e8`](https://github.com/darac/adventofcode/commit/f5477e861855583fd22743b1d8ac64831f487c5a))

- **deps**: Update python-semantic-release/publish-action action to v9.21.0
  ([`504f3d0`](https://github.com/darac/adventofcode/commit/504f3d086f5373602627fb7ba708c27c5fb0dfaa))

- **deps**: Update python-semantic-release/python-semantic-release action to v9.16.1
  ([`b9859bf`](https://github.com/darac/adventofcode/commit/b9859bf01a6061bd1d8bdc8f0ab16c4bc45958fd))

- **deps**: Update python-semantic-release/python-semantic-release action to v9.18.0
  ([`d15a3fe`](https://github.com/darac/adventofcode/commit/d15a3fe13fd52d99ced8ca79eb56ad492d10765f))

- **deps**: Update python-semantic-release/python-semantic-release action to v9.18.1
  ([`a6e837d`](https://github.com/darac/adventofcode/commit/a6e837deec9593ffc4ea265aa94188c0857d38de))

- **deps**: Update python-semantic-release/python-semantic-release action to v9.20.0
  ([`b1634d7`](https://github.com/darac/adventofcode/commit/b1634d7fa7ffb3eda54fe751f16be454bb8f4629))

- **deps**: Update python-semantic-release/python-semantic-release action to v9.21.0
  ([`4d5abc5`](https://github.com/darac/adventofcode/commit/4d5abc5adc57de4d6d665a91318cd56f6de1ff70))

### Continuous Integration

- Enable pre-commit renovate
  ([`ea5e058`](https://github.com/darac/adventofcode/commit/ea5e058e6b011a0781dacf728cef7484ba590f45))

- Only run Sonar Scanner once per build
  ([`bff3bd0`](https://github.com/darac/adventofcode/commit/bff3bd0b57a12f4f9a9bf474f623a8b8562472c6))

- Use tox as a test runner
  ([`30d9195`](https://github.com/darac/adventofcode/commit/30d919549c806c6df79e0b6b453f9503fd796fd1))


## v2024.4.2 (2024-12-18)

### Bug Fixes

- Reduce Sonar smells
  ([`8f076b7`](https://github.com/darac/adventofcode/commit/8f076b79b4b0c1654bd023884f694fb29d233aa6))

### Build System

- Add coverage.xml to Sonar
  ([`20c87b0`](https://github.com/darac/adventofcode/commit/20c87b09b56afe143c6a62615450dec3da723ee0))

- Add devcontainers spec
  ([`4d149da`](https://github.com/darac/adventofcode/commit/4d149daab20f8527f1b8f550342b268d26b3a010))

### Chores

- **deps**: Update actions/attest-build-provenance action to v2
  ([`67ef1d8`](https://github.com/darac/adventofcode/commit/67ef1d899840bd5613f69f53381070f5fc5c42a8))

- **deps**: Update docker/build-push-action digest to 11be14d
  ([`6df5acd`](https://github.com/darac/adventofcode/commit/6df5acdb6a34e246400195e5452fe46a65a487ec))

- **deps**: Update docker/metadata-action digest to 906ecf0
  ([`45ee226`](https://github.com/darac/adventofcode/commit/45ee2269b2aaff3b0492f3586e5f13acb51ec229))

- **deps**: Update python-semantic-release/publish-action action to v9.15.2
  ([`1767516`](https://github.com/darac/adventofcode/commit/1767516e44bbabac03042a7592b8eec97a1855a2))

- **deps**: Update python-semantic-release/python-semantic-release action to v9.15.2
  ([`b7a1e49`](https://github.com/darac/adventofcode/commit/b7a1e499194d3df44e47a844537322e5f5443f85))

### Continuous Integration

- Cache Sonar files
  ([`7d257f3`](https://github.com/darac/adventofcode/commit/7d257f3814ea152989ea03409e5e2a3f75d76c47))


## v2024.4.1 (2024-12-06)

### Bug Fixes

- 2024 Day 6, second part
  ([`570b48b`](https://github.com/darac/adventofcode/commit/570b48b78571eb867091c9203b6b05903c2fbaf6))

### Chores

- Update uv.lock
  ([`f441292`](https://github.com/darac/adventofcode/commit/f4412922f6ef1290fe441d946ed771740a51080f))


## v2024.4.0 (2024-12-06)

### Continuous Integration

- Move Docker Image into main workflow
  ([`7bf97ed`](https://github.com/darac/adventofcode/commit/7bf97ed09b2437651df88fd98332b77469817cf8))

- Only run Docker if release was actually produced
  ([`11c9536`](https://github.com/darac/adventofcode/commit/11c9536a1be8dce6800c95e2aa9aa6a766edaaf5))

- Trigger Docker Image after completion of Test
  ([`fb79388`](https://github.com/darac/adventofcode/commit/fb7938814bb364e18e47a12dcdf64c9d0bcfa716))

- Update pre-commit config
  ([`434d4cf`](https://github.com/darac/adventofcode/commit/434d4cfca4330235644e3761b3c5716d3c5866eb))

### Features

- 2024 Day 6, first part
  ([`acb7e0f`](https://github.com/darac/adventofcode/commit/acb7e0f592b6f018f80ceed4f2f04bb5a3a6822a))


## v2024.3.0 (2024-12-04)

### Chores

- **deps**: Update docker/build-push-action digest to 8796455
  ([#140](https://github.com/darac/adventofcode/pull/140),
  [`e2a495d`](https://github.com/darac/adventofcode/commit/e2a495d5d4f1779061ee32f54fcf71005caa91e7))

Co-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>

- **deps**: Update python-semantic-release/publish-action action to v9.15.1
  ([`0670714`](https://github.com/darac/adventofcode/commit/0670714c55c86fd102e674c8b7505e6e0efa154d))

- **deps**: Update python-semantic-release/python-semantic-release action to v9.15.1
  ([#139](https://github.com/darac/adventofcode/pull/139),
  [`2bf5c6f`](https://github.com/darac/adventofcode/commit/2bf5c6f3fb395aab6ebf01b380e744159564e2ed))

Co-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>

### Continuous Integration

- Build docker image upon release
  ([`3746026`](https://github.com/darac/adventofcode/commit/3746026db8cc8bd1d5579421548589d7cfa91a66))

### Documentation

- Hyperlink the Tests badge to the tests
  ([`d8d7d86`](https://github.com/darac/adventofcode/commit/d8d7d86cbebbf05ef3cfc0feb6f4e18451c07a99))

### Features

- 2024 Day 4 complete
  ([`0743119`](https://github.com/darac/adventofcode/commit/074311943845f9aa066aca6aa8f0b1737f7da39d))


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

### Breaking Changes

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
