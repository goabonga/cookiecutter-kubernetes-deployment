# Changelog

All notable changes to this project are documented here. The format is
based on [Keep a Changelog](https://keepachangelog.com/) and this project
adheres to [Semantic Versioning](https://semver.org/). New entries are
generated from [Conventional Commits](https://www.conventionalcommits.org/)
by [multicz](https://github.com/goabonga/multicz).

## [0.2.5] - 2026-06-14

### Fixed

- **hooks**: default alias to "none" and treat it as no alias (`307a99b`)
- **hooks**: don't crash when upstream values cannot be fetched (`889b8d7`)
- **hooks**: avoid literal {{ }} that breaks Jinja rendering (`136f677`)

## [0.2.4] - 2026-06-14

### Fixed

- **hooks**: support OCI registries and avoid crash on missing chart metadata (`b2e528a`)
- **hooks**: treat empty alias as null (`fc096c8`)

## [0.2.3] - 2026-05-20

### Fixed

- complete PyPI package metadata (`de17090`)

## [0.2.2] - 2024-11-11

### Fixed

- generated license link should to match with license type
- project name and version do not match

## [0.2.1] - 2024-11-11

### Fixed

- update contributing template to match with deployment coding standards
- update readme template to display current helm version

## [0.2.0] - 2024-11-11

### Added

- generate clear readme, contributing and license files

## [0.1.1] - 2024-11-11

### Fixed

- use commitizen tag format without prefix
- indentation use space instead of tab when alias is defined

## [0.1.0] - 2024-11-11

### Added

- create viable `cookiecutter-kubernetes-deployment` project
