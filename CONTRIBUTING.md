# Contributing to ResearchMind

Thank you for your interest in contributing to **ResearchMind**! We welcome improvements, bug reports, and suggestions to make this multi-agent research assistant even better.

---

## Code of Conduct

We are committed to providing a friendly, safe, and welcoming environment for all contributors. Please be respectful and constructive in all discussions, issues, and pull requests.

---

## How to Contribute

### 1. Reporting Bugs
- Check the [existing issues](https://github.com/itendra-kumar-dev/Multi-Agent-System/issues) to ensure the bug has not already been reported.
- Open a new issue using the **Bug Report** template.
- Include clear steps to reproduce the issue, expected outcome, and error traces.

### 2. Suggesting Features
- Open an issue using the **Feature Request** template.
- Explain the motivation behind the suggestion and provide concrete examples or use cases.

### 3. Submitting Pull Requests
1. **Fork** the repository and clone it to your local development machine.
2. Create a topic branch:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/issue-description
   ```
3. Set up the local virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```
4. Verify your code syntax and import integrity:
   ```bash
   python -m py_compile agents.py app.py pipeline.py tools.py
   ```
5. Commit your changes with descriptive messages:
   ```bash
   git commit -m "feat: describe your change clearly"
   ```
6. Push to your fork and submit a **Pull Request** to the `main` branch.

---

## Code Guidelines

- **Clean Structure**: Write clear, readable Python following PEP 8 conventions.
- **Type Annotations**: Use type hints on new functions where applicable.
- **No Secrets**: Never commit `.env` files or API keys. Ensure test scripts use environment variables or mock responses.
