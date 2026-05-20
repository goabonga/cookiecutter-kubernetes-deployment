# Contributing to cookiecutter-kubernetes-deployment

Thanks for taking the time to contribute. This document is the short
version of how to propose a change and what the project expects in return.

## Code of Conduct

Participation in this project is governed by the
[Code of Conduct](CODE_OF_CONDUCT.md). By contributing you agree to abide
by its terms.

## Repository layout

```
.
├── cookiecutter.json              # template prompts / defaults
├── {{cookiecutter.name}}/         # the templated deployment tree
├── hooks/                         # post-generation hook (Jinja-templated)
├── tests/                         # bake smoke tests (pytest-cookies)
├── scripts/                       # SPDX header helper
├── pyproject.toml                 # uv project + hatchling build
└── multicz.toml                   # Conventional Commits releasing
```

The template (`{{cookiecutter.name}}/`) is rendered into the user's
generated project, so its files intentionally do **not** carry this
repository's SPDX header. The `hooks/` are Jinja-templated Python that
run at generation time (not shipped into the output); they are excluded
from ruff but do carry the header.

## Development setup

```bash
git clone https://github.com/goabonga/cookiecutter-kubernetes-deployment.git
cd cookiecutter-kubernetes-deployment
uv sync
uv run pre-commit install
```

The post-generation hook calls **Helm** (and **helm-docs**) to resolve
chart versions and render `values.yaml`, so baking the template requires
both on your `PATH` (plus network access to the chart repository):

- [Helm](https://helm.sh/docs/intro/install/)
- [helm-docs](https://github.com/norwoodj/helm-docs)

## Running the tests

```bash
uv run pytest          # bakes the template (needs Helm + helm-docs + network)
```

Generate a project from your working copy to eyeball the output:

```bash
uvx cookiecutter .
```

## Lint and headers

```bash
uv run ruff check .
uv run ruff format --check .
python scripts/add_license_header.py --path . --types py,yml,toml --check
```

The template tree and the Jinja hooks are excluded from ruff.

## Packaging

The template (cookiecutter.json, the tree and the hooks) is force-included
into a hatchling-built wheel so it can be published to PyPI while still
working via `cookiecutter gh:...`. Verify a build before changing
packaging:

```bash
uv build
# inspect dist/*.whl - the {{ }} filenames must be preserved
```

## Commit messages

Commit messages MUST follow
[Conventional Commits](https://www.conventionalcommits.org/). They drive
the version bump and CHANGELOG computed by
[multicz](https://github.com/goabonga/multicz).

| Type | Effect on version | Use it for |
| --- | --- | --- |
| `feat` | minor | new template capability |
| `fix` | patch | bug fix in the template or hooks |
| `refactor`, `docs`, `test`, `chore`, `ci`, `build`, `style` | none | maintenance |
| `feat!` / `BREAKING CHANGE:` | major | incompatible change to the generated output |

Only changes under the tracked paths (`cookiecutter.json`, the template
tree, `hooks/`, `pyproject.toml`) trigger a release. Do not append
`Co-Authored-By` trailers.

## Releasing

Releases are automated: on every push to `main`, the workflow runs
`multicz bump --commit --tag --push` and publishes the packaged template
to PyPI. Maintainers do not bump versions or edit the changelog by hand.

## Reporting bugs and asking for features

Please open a GitHub issue. For security-sensitive reports, follow
[SECURITY.md](SECURITY.md) instead of the public tracker.
