# Security Policy

## Supported versions

This is a Cookiecutter template, not a runtime dependency. Security fixes
are applied only to the latest released version on the `main` branch (and
the matching PyPI release).

| Version | Supported |
| --- | --- |
| latest release | ✅ |
| older releases | ❌ |

## Reporting a vulnerability

**Please do not open a public issue.** GitHub's
[private vulnerability reporting](https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing-information-about-vulnerabilities/privately-reporting-a-security-vulnerability)
is the preferred channel:

1. Go to the repository's **Security** tab.
2. Click **Report a vulnerability**.
3. Describe the issue (e.g. an insecure default in a generated Kubernetes
   manifest or in the generation hooks), with reproduction steps and a
   suggested mitigation.

If you cannot use GitHub's form, email **goabonga@pm.me** with the same
information. PGP encryption is available on request.

You can expect an acknowledgement within **3 business days**, a triage
assessment within **10 business days**, and a fix or written mitigation
plan before any public disclosure.

## Scope

Because this project generates Kubernetes deployment manifests and runs a
post-generation hook (helm), security-relevant reports typically concern
**insecure defaults in the rendered output** (the template under
`{{cookiecutter.name}}/`) or the hook behavior (`hooks/`). Both are in
scope.

Thanks for helping keep the template and its users safe.
