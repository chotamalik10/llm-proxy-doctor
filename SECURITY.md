# Security Policy

## Supported versions

Security fixes are applied to the latest version on the default branch. Use the latest release or commit when reporting an issue.

## Reporting a vulnerability

Please do not publish credentials, access tokens, private endpoint URLs, or exploitable details in a public issue. Use GitHub's private vulnerability reporting feature for this repository when available.

Include the affected version, Python version, impact, and minimal reproduction steps. Remove secrets and sensitive response bodies from logs before sharing.

## Safe use

- Prefer HTTPS for remote endpoints.
- Supply credentials through environment variables, not command-line arguments.
- Do not commit API keys, proxy URLs containing credentials, or provider secrets.
- Run diagnostics only against endpoints you own or are authorized to test.
- Remember that a diagnostic request sends a small prompt to the configured endpoint.
