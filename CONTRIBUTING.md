# Contributing to Blackjack Simulator

Thank you for considering contributing to the Blackjack Simulator! This document provides guidelines for contributing.

## 🚀 Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/Blackjack-Simulator.git`
3. Create a branch: `git checkout -b feature/amazing-feature`
4. Make your changes
5. Run tests: `pytest`
6. Commit: `git commit -m 'Add amazing feature'`
7. Push: `git push origin feature/amazing-feature`
8. Open a Pull Request

## 📝 Development Setup

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements-dev.txt

# Run tests
pytest --cov=src

# Format code
black src/ tests/

# Lint
flake8 src/ tests/
mypy src/
```

## ✅ Pull Request Checklist

- [ ] Code follows PEP 8 style guide
- [ ] All tests pass (`pytest`)
- [ ] New features have tests (maintain >90% coverage)
- [ ] Documentation is updated
- [ ] Commit messages are clear and descriptive
- [ ] No breaking changes (or clearly documented)

## 🧪 Testing Guidelines

- Write unit tests for all new functions
- Include edge cases and error handling
- Use meaningful test names (test_what_when_expected)
- Mock external dependencies
- Aim for >90% code coverage

## 📚 Documentation

- Add docstrings to all public functions/classes
- Update README.md for new features
- Include code examples for complex features
- Keep CHANGELOG.md updated

## 🎨 Code Style

- Follow PEP 8
- Use type hints
- Maximum line length: 100 characters
- Use meaningful variable names
- Add comments for complex logic

## 🐛 Bug Reports

Include:
- Python version
- Steps to reproduce
- Expected behavior
- Actual behavior
- Error messages/stack traces

## 💡 Feature Requests

- Describe the feature clearly
- Explain the use case
- Provide examples if possible
- Consider implementation complexity

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## ❓ Questions

Open an issue or contact via GitHub.

Thank you for contributing! 🃏
