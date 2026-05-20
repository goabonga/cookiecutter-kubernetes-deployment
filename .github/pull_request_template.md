## Description

<!-- Describe what this PR does and why. -->

## Type

- [ ] `feat` - New template capability
- [ ] `fix` - Bug fix
- [ ] `docs` - Documentation
- [ ] `refactor` - Refactoring
- [ ] `test` - Tests
- [ ] `chore` - Maintenance
- [ ] `ci` - CI / release pipeline

## Changes

<!-- List the main changes: -->

-

## Related Issues

<!-- Closes #123, Fixes #456 -->

## Checklist

- [ ] Commits follow [Conventional Commits](https://www.conventionalcommits.org/)
- [ ] `uv run pytest` passes (bake smoke tests; needs Helm + helm-docs)
- [ ] `uv run ruff check .` and `uv run ruff format --check .` are clean
- [ ] `uv build` succeeds and the `{{ }}` template filenames survive in the wheel
- [ ] `uv tool run multicz validate --strict` passes
- [ ] SPDX headers present on the repo's own files (`python scripts/add_license_header.py --path . --types py,yml,toml --check`) - the template tree is intentionally excluded
- [ ] No `Co-Authored-By` trailer in commit messages
