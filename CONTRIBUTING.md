# Contributing to Kite Trading App

Thank you for your interest in contributing to the Kite Trading App! We welcome all contributions, including bug reports, feature requests, and code contributions.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Code Style](#code-style)
- [Commit Message Guidelines](#commit-message-guidelines)
- [Pull Request Process](#pull-request-process)
- [Reporting Bugs](#reporting-bugs)
- [Feature Requests](#feature-requests)
- [License](#license)

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## Getting Started

1. **Fork the repository** on GitHub.
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/your-username/kite-trading-app.git
   cd kite-trading-app
   ```
3. **Set up the development environment** as described in the [README.md](README.md).
4. **Create a new branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Workflow

1. **Install pre-commit hooks** (recommended):
   ```bash
   pre-commit install
   ```
   This will automatically run linters and formatters before each commit.

2. **Make your changes** following the code style guidelines below.

3. **Run tests** to ensure nothing is broken:
   ```bash
   # Run backend tests
   cd backend
   pytest
   
   # Run frontend tests
   cd ../frontend
   npm test
   ```

4. **Commit your changes** with a descriptive commit message:
   ```bash
   git commit -m "feat: add new trading strategy"
   ```

5. **Push your changes** to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Open a Pull Request** from your fork to the main repository.

## Code Style

### Backend (Python)

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide.
- Use type hints for all function parameters and return values.
- Keep functions small and focused on a single responsibility.
- Write docstrings for all public functions, classes, and methods following the Google style:
  ```python
  def example_function(param1: str, param2: int) -> bool:
      """Short description of what the function does.
  
      Args:
          param1: Description of the first parameter.
          param2: Description of the second parameter.
  
      Returns:
          Description of the return value.
  
      Raises:
          ValueError: If parameters are invalid.
      """
  ```

### Frontend (TypeScript/React)

- Follow the [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript).
- Use functional components with hooks.
- Use TypeScript for type safety.
- Keep components small and focused on a single responsibility.
- Use meaningful variable and function names.
- Use destructuring for props and state.
- Use CSS modules or Tailwind CSS for styling.

## Commit Message Guidelines

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification. Each commit message consists of a **type**, an optional **scope**, and a **description**:

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

### Types

- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation only changes
- **style**: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc.)
- **refactor**: A code change that neither fixes a bug nor adds a feature
- **perf**: A code change that improves performance
- **test**: Adding missing tests or correcting existing tests
- **build**: Changes that affect the build system or external dependencies
- **ci**: Changes to CI configuration files and scripts
- **chore**: Other changes that don't modify src or test files
- **revert**: Reverts a previous commit

### Examples

```
feat(auth): add login with Google

docs: update README with installation instructions

fix(api): handle null values in trade history endpoint

chore: update dependencies
```

## Pull Request Process

1. Ensure any install or build dependencies are removed before the end of the layer when doing a build.
2. Update the README.md with details of changes to the interface, including new environment variables, exposed ports, useful file locations, and container parameters.
3. Increase the version numbers in any example files and the README.md to the new version that this Pull Request would represent. The versioning scheme we use is [SemVer](http://semver.org/).
4. You may merge the Pull Request once you have the sign-off of two other developers, or if you do not have permission to do that, you may request the second reviewer to merge it for you.

## Reporting Bugs

Before submitting a bug report, please check the [issue tracker](https://github.com/yourusername/kite-trading-app/issues) to see if the issue has already been reported.

When creating a bug report, please include the following information:

1. A clear and descriptive title.
2. Steps to reproduce the issue.
3. Expected behavior.
4. Actual behavior.
5. Screenshots or error messages (if applicable).
6. Your environment (OS, browser, Node.js version, Python version, etc.).

## Feature Requests

We welcome feature requests! Before submitting a new feature request, please check if a similar feature has already been requested. When creating a feature request, please include:

1. A clear and descriptive title.
2. A description of the problem you're trying to solve.
3. Any alternative solutions or features you've considered.
4. Any additional context or screenshots about the feature request.

## License

By contributing to this project, you agree that your contributions will be licensed under the [MIT License](LICENSE).
