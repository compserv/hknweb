# Contributing to HKN Website

Thank you for your interest in contributing to the HKN (IEEE-Eta Kappa Nu) Berkeley Mu Chapter website! We welcome contributions from everyone.

## Table of Contents

- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Workflow](#development-workflow)
- [Code Style Guidelines](#code-style-guidelines)
- [Submitting a Pull Request](#submitting-a-pull-request)
- [Reporting Issues](#reporting-issues)
- [Communication](#communication)

## Getting Started

Before you begin contributing, please:

1. Read the [README.md](README.md) to understand the project structure and setup instructions
2. Set up your local development environment following the setup guide
3. Look for issues labeled with `good first issue` if you're new to the project

## How to Contribute

There are several ways you can contribute to this project:

### Code Contributions

- Fix bugs or implement new features
- Improve existing functionality
- Write or update tests
- Optimize performance

### Documentation

- Improve existing documentation
- Add missing documentation
- Fix typos or clarify confusing sections
- Create tutorials or guides

### Testing

- Report bugs
- Test new features
- Verify bug fixes

## Development Workflow

### 1. Fork and Clone

Fork the repository and clone it to your local machine:

```bash
git clone https://github.com/YOUR-USERNAME/hknweb.git
cd hknweb
```

### 2. Create a Branch

Create a new branch for your work:

```bash
git checkout -b feature/your-feature-name
```

Or for bug fixes:

```bash
git checkout -b fix/issue-description
```

### 3. Set Up Development Environment

Follow the setup instructions in the README.md:

```bash
# Install Poetry
pipx install poetry

# Install dependencies
poetry install

# Activate virtual environment
poetry shell

# Apply migrations
python manage.py migrate

# Run the development server
python manage.py runserver
```

### 4. Make Your Changes

- Write clean, readable code
- Follow the existing code style
- Add comments where necessary
- Update documentation if needed

### 5. Test Your Changes

Before submitting, make sure:

- Your code works as expected
- You haven't broken any existing functionality
- All tests pass (if applicable)
- The development server runs without errors

### 6. Commit Your Changes

Write clear, descriptive commit messages:

```bash
git add .
git commit -m "Add feature: brief description of what you did"
```

Good commit message examples:
- `Fix: Resolve login authentication bug`
- `Add: Implement event calendar filtering`
- `Update: Improve README setup instructions`
- `Docs: Add Docker setup documentation`

### 7. Push to Your Fork

```bash
git push origin feature/your-feature-name
```

## Code Style Guidelines

### Python Code

- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Keep functions small and focused
- Add docstrings to functions and classes
- Use type hints where appropriate

### Django Best Practices

- Follow Django's coding conventions
- Use Django's built-in features when possible
- Write database queries efficiently
- Keep views, models, and templates organized

### HTML/CSS/JavaScript

- Use semantic HTML
- Keep CSS organized and modular
- Follow Vue.js best practices for frontend code
- Ensure responsive design

## Submitting a Pull Request

1. **Push your changes** to your forked repository
2. **Create a Pull Request** from your branch to the `master` branch of the main repository
3. **Fill out the PR template** with:
   - Clear description of what changes you made
   - Why these changes are necessary
   - Any related issue numbers (e.g., "Fixes #123")
   - Screenshots (if applicable)
4. **Wait for review** - A maintainer will review your PR and may request changes
5. **Make requested changes** if needed
6. **Get merged** - Once approved, your PR will be merged!

### PR Title Guidelines

Use clear, descriptive titles:
- `Fix: Resolve event calendar display bug`
- `Feature: Add user profile editing`
- `Docs: Update contribution guidelines`
- `Refactor: Improve database query performance`

## Reporting Issues

If you find a bug or have a feature request:

1. **Check existing issues** to avoid duplicates
2. **Use the issue template** if available
3. **Provide detailed information:**
   - Clear title and description
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - Screenshots or error messages
   - Your environment (OS, Python version, etc.)

## Communication

- Be respectful and constructive
- Ask questions if you're unsure
- Provide feedback on others' contributions
- Help review pull requests

## Need Help?

If you need assistance:
- Check the [README.md](README.md) first
- Look through existing issues and pull requests
- Ask questions in your issue or PR
- Reach out to project maintainers

## License

By contributing, you agree that your contributions will be licensed under the same [MIT License](LICENSE) that covers this project.

Thank you for contributing to the HKN website! 🎉
