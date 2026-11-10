# Security Policy

## Supported Versions

Only the latest version on the `main` branch is actively supported with security updates.

| Version | Supported |
| :--- | :--- |
| `main` (Latest) | :white_check_mark: |
| Older releases | :x: |

---

## Reporting a Vulnerability

If you identify a security issue or vulnerability (such as unintended key exposure or scraping vulnerabilities), please do **not** open a public issue.

Instead, report it responsibly:
- Email the maintainer directly at: `jitendrasingh27406@gmail.com`
- Include detailed reproduction steps and affected components.

We will review the report promptly and coordinate an appropriate fix before public disclosure.

---

## Safe Handling of API Keys

- Never commit `.env` or any file containing live API keys (`OPENAI_API_KEY`, `TAVILY_API_KEY`).
- Use `.env.example` as a template for public reference.
- If a key is accidentally committed, revoke and regenerate it immediately in the respective provider console.
