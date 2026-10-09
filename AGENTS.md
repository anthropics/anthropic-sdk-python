# AGENTS.md

Context file for AI agents working on anthropic-sdk-python.

**Dual Format**: This file combines Category A (Operations Manual) and Category B (Context Guide) for comprehensive agent guidance.

**Domain Detected:** Agent / Chatbot (Based on codebase patterns)

## Project Overview

anthropic-sdk-python is a Python project using Python (hatchling).

**Key Info:**
- **Primary Language:** Python
- **Build System:** Python (hatchling)
- **Test Framework:** pytest
- **Total Files:** 2565
- **Test Files:** 256
- **AI Readiness Score:** 70/100 (AI-Native-Plus)

---

## 🚨 AI Policy & Operations

Extracted from CONTRIBUTING.md - operational constraints and procedures.

### AI Policy

- Alternatively if you don't want to install `uv`, you can stick with the standard `pip` setup by ensuring you have the Python version specified in `.python-version`, create a virtual environment however you desire and then install dependencies using this command:

### Key Requirements

- This is useful when the endpoint hasn't changed, but your code handles the response differently and the assertions need updating.
- You can release to package managers by using [the `Publish PyPI` GitHub action](https://www.github.com/anthropics/anthropic-sdk-python/actions/workflows/publish-pypi.yml). This requires a setup organization or repository secret to be set up.

### Development Procedures

- Or [install uv manually](https://docs.astral.sh/uv/getting-started/installation/) and run:
- You can then run scripts using `uv run python script.py` or by manually activating the virtual environment:
- $ pip install -r requirements-dev.lock
- If you’d like to use the repository from source, you can either install from git or link to a cloned repository:
- To install via git:



## 🤖 Agent/Chatbot Architecture

This is an AI agent or dialogue system project.

### Key Patterns Detected

- **Intent Handling:** The project processes user intents and maps them to actions
- **Entity Extraction:** Named entity recognition and slot filling for dialogue context
- **Conversation Management:** Multi-turn dialogue flows with context preservation
- **Tool Use:** Agent actions or skills that execute external operations

### Testing Agent Conversations

When writing tests for dialogue systems:

1. **Conversation Flows:** Test end-to-end dialogue paths, not individual components
2. **Intent Accuracy:** Verify correct intent detection for various phrasings
3. **Entity Extraction:** Test slot filling accuracy and edge cases
4. **Context Preservation:** Ensure multi-turn conversations maintain state correctly
5. **Action Execution:** Mock external actions and verify correct invocation
6. **Fallback Handling:** Test graceful degradation when confidence is low



### Detected Frameworks

| Framework | Version | Detection Type |
|-----------|---------|-----------------|
| pydantic | 1.10.0-3 | Wrapped/Re-exported |
| pytest | unknown | Direct import |
| unittest | unknown | Direct import |



## 🏗️ Architecture & Context Guide

This section provides architectural context and agent-understanding for the codebase.

### Prerequisites

- **Python:** >= 3.10 (or applicable language version)
- **Package Manager:** pip or uv
- **Test Runner:** pytest



### Project Structure

```
anthropic-sdk-python/
├── pyproject.toml
├── src/                  # Source code
├── tests/                # Test suite (256 files)
└── README.md             # Project documentation
```

### Architecture Overview

#### Key Components
- **Main Entry:** Standard layout
- **Test Suite:** 256 test files
- **Build Configuration:** pyproject.toml

#### Design Principles

1. **Modularity** - Code organized by functionality with clear separation of concerns
2. **Testability** - Comprehensive test coverage across critical paths
3. **Clarity** - Explicit naming and structure for AI agent understanding
4. **Consistency** - Uniform patterns and conventions throughout codebase
5. **Maintainability** - Well-documented code with clear intent

### Directory Map

| Directory | Purpose |
|-----------|----------|
| `examples/` | Usage examples |
| `scripts/` | Build and utility scripts |
| `src/` | Source code |
| `tests/` | Test suite |


### Development Workflow

#### Initial Setup

```bash
git clone https://github.com/anthropics/anthropic-sdk-python
cd anthropic-sdk-python
pip install -e .
# or
uv sync --all-groups
```

#### Development Commands

**Running Tests:**
```bash
pytest                    # Run all tests
pytest tests/             # Run specific test directory
pytest -v                 # Verbose output with test names
pytest -x                 # Stop on first failure
coverage run -m pytest && coverage report  # With coverage report
```

#### Code Quality
```bash
ruff check .              # Lint with ruff
ruff format .             # Format code
mypy .                    # Type checking (if configured)
```

### Code Style & Conventions

- **Naming:** Use snake_case for functions and variables
- **Type Hints:** Yes (strongly encouraged)
- **Error Handling:** Yes - handle errors at boundaries; let exceptions propagate when another layer owns recovery
- **Logging:** Yes
- **Testing:** Yes - write tests alongside code changes

### Testing Strategy

**Framework:** pytest
**Test Files:** 256 found

Before committing:
1. Run the full test suite: `pytest`
2. Ensure all tests pass
3. Check type hints: `mypy .`
4. Format code: `ruff format .`

### Writing Documentation

When updating docs:
1. Always include explanatory text before code snippets
2. Describe *why* and *what* before showing *how*
3. Keep sections focused on a single concept
4. Use clear, concrete examples

## Known Gotchas & Warnings

- Alternatively if you don't want to install `uv`, you can stick with the standard `pip` setup by ensuring you have the Python version specified in `.python-version`, create a virtual environment however you desire and then install dependencies using this command:

### Contributing Guidelines

This project has a detailed contribution guide at **`CONTRIBUTING.md`**.

**Key Requirements:**
- Review the contribution guide for all requirements
- Follow established patterns in the codebase
- Ensure alignment with project's contribution policies

### Common Patterns

When contributing to this project:
1. Read existing code in the area you're modifying
2. Follow the established patterns and style
3. Write tests for new functionality
4. Use clear, descriptive variable and function names
5. Add docstrings for public APIs
6. Update tests when changing behavior

### What We Value

✅ Well-tested code with clear intent
✅ Consistent code style and naming conventions
✅ Code that is easy for AI agents to understand
✅ Clear, descriptive commit messages
✅ Modular, reusable components
✅ Comprehensive documentation

### What We Avoid

❌ Large functions doing multiple things
❌ Commented-out dead code
❌ Inconsistent naming or patterns
❌ Unclear error messages
❌ Unexplained magic numbers or strings
❌ Skipped tests or test TODOs

### AI Readiness Dimensions (Scoring)

This project is evaluated across 8 dimensions:

1. **Architecture** (0/100) - Code organization and modularity
2. **Testing** (15/100) - Test coverage and quality
3. **Dependencies** (12/100) - Dependency management
4. **Conventions** (10/100) - Consistent patterns
5. **Entry Points** (0/100) - Clear main/start locations
6. **Security** (10/100) - Input validation and error handling
7. **Build** (10/100) - Clear build/setup instructions
8. **Documentation** (8/100) - Code and project documentation

### Next Steps

Before making changes:
1. Read relevant source files to understand the existing code
2. Look at existing tests for similar functionality
3. Follow the patterns you see in the codebase
4. Write tests for your changes
5. Run `pytest` to verify nothing breaks
6. Run code quality checks: `ruff check . && mypy .`
7. Format your code: `ruff format .`

---

*Generated by Braxis - keeping AI agents in sync with your code*
