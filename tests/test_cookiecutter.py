# SPDX-License-Identifier: MIT
# Copyright (c) 2024-2026 Chris <goabonga@pm.me>

from contextlib import contextmanager

from cookiecutter.utils import rmtree


@contextmanager
def bake_in_temp_dir(cookies, **kwargs):
    """Bake the template and clean up the generated project afterwards."""
    result = cookies.bake(**kwargs)
    try:
        yield result
    finally:
        if result.project_path is not None:
            rmtree(str(result.project_path))


def test_bake_with_defaults(cookies):
    # The post-generation hook calls Helm and helm-docs, so this test
    # requires both on PATH plus network access to the chart repository.
    with bake_in_temp_dir(cookies) as result:
        assert result.exit_code == 0
        assert result.exception is None
        assert result.project_path.is_dir()

        # default name "keycloak" -> project directory name.
        assert result.project_path.name == "keycloak"

        top_level = {f.name for f in result.project_path.glob("*")}
        assert "README.md" in top_level
        assert "LICENSE" in top_level  # rendered from the chosen license
        assert (result.project_path / "base" / "kustomization.yaml").is_file()
        assert (
            result.project_path / "overlays" / "production" / "kustomization.yaml"
        ).is_file()
        assert (
            result.project_path / "overlays" / "development" / "kustomization.yaml"
        ).is_file()
