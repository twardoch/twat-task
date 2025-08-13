# twat-task Repository File Catalog

## Filesystem Tree
```
.
├── .cursor/                        # Cursor IDE configuration
│   └── rules/                      # Cursor coding rules and guidelines
│       ├── cleanup.mdc             # Cleanup automation rules
│       ├── filetree.mdc            # File tree documentation rules
│       └── quality.mdc             # Code quality standards
├── .github/                        # GitHub configuration and workflows
│   └── workflows/                  # CI/CD workflow definitions
│       ├── push.yml                # Build & test workflow for pushes
│       └── release.yml             # PyPI release workflow for tags
├── .pre-commit-config.yaml         # Pre-commit hooks configuration
├── CHANGELOG.md                    # Project change documentation
├── CLEANUP.txt                     # Generated cleanup log file
├── IMPLEMENTATION_SUMMARY.md       # Git tag-based versioning summary
├── LICENSE                         # MIT license file
├── LOG.md                          # Project activity log
├── PLAN.md                         # Detailed project improvement plan
├── README.md                       # Main project documentation
├── REPO_CONTENT.txt                # Generated repository content dump
├── REVIEW/                         # Review and analysis folder (this folder)
├── TODO.md                         # Task tracking checklist
├── VERSION.txt                     # Version tracking file
├── cleanup.py                      # Repository maintenance script
├── examples/                       # Usage examples
│   └── testprefect_example.py      # Prefect workflow example
├── llms.txt                        # Generated log for LLM context
├── pyproject.toml                  # Python project configuration
├── src/                            # Source code directory
│   └── twat_task/                  # Main package directory
│       ├── __init__.py             # Package initialization
│       └── task.py                 # Core video processing tasks
└── tests/                          # Test suite
    ├── test_flows.py               # Flow integration tests
    ├── test_package.py             # Package-level tests
    ├── test_tasks.py               # Unit tests for tasks
    └── test_video_transcript.py    # VideoTranscript class tests
```

## File Descriptions by Category

### Core Package Files

#### `src/twat_task/__init__.py`
- **Purpose**: Package initialization and public API definition
- **Contents**: Imports and exposes main classes (`VideoTranscript`) and functions
- **Dependencies**: Uses hatch-vcs for version management
- **Key Exports**: `VideoTranscript`, task functions, `__version__`

#### `src/twat_task/task.py`
- **Purpose**: Core video processing functionality using Prefect workflows
- **Contains**:
  - `extract_audio_task()`: Prefect task for audio extraction (currently mock)
  - `generate_transcript_task()`: Prefect task for speech-to-text (currently mock)
  - `process_video_flow()`: Prefect flow orchestrating the tasks
  - `VideoTranscript`: Pydantic model providing high-level interface
- **Architecture**: Uses lazy evaluation with `@cached_property` and `@computed_field`
- **Mock Implementation**: Simulates real processing with delays and JSON metadata

### Configuration Files

#### `pyproject.toml`
- **Purpose**: Comprehensive Python project configuration
- **Sections**:
  - Build system configuration (hatchling, hatch-vcs)
  - Project metadata and dependencies
  - Development environment setup (hatch)
  - Code quality tools (ruff, mypy, pytest)
  - Optional dependencies for testing and development
- **Dependencies**: prefect>=3.1.0, pydantic>=2.0.0, twat>=1.8.1
- **Plugin Registration**: Registers as twat ecosystem plugin

#### `.pre-commit-config.yaml`
- **Purpose**: Defines pre-commit hooks for code quality
- **Hooks**: Likely includes ruff linting/formatting, mypy type checking
- **Integration**: Works with the hatch scripts for consistent code quality

### Documentation Files

#### `README.md`
- **Purpose**: Main project documentation and user guide
- **Sections**:
  - Project overview and purpose
  - Installation instructions (PyPI and development)
  - Usage examples with `VideoTranscript` class
  - Technical deep dive into architecture
  - Development workflow and contribution guidelines
- **Target Audience**: Developers, data engineers, Prefect users
- **Code Examples**: Demonstrates lazy-loading video processing

#### `CHANGELOG.md`
- **Purpose**: Documents project changes following Keep a Changelog format
- **Current State**: Initial setup with placeholder sections
- **Format**: Semantic versioning with Added/Changed/Removed sections

#### `PLAN.md`
- **Purpose**: Detailed roadmap for codebase streamlining and MVP preparation
- **Content**: 9-step plan covering cleanup, consolidation, and quality improvements
- **Focus**: Removing redundant files, fixing linting issues, streamlining dependencies

#### `TODO.md`
- **Purpose**: Flat checklist representation of PLAN.md items
- **Format**: Checkbox-style task list for tracking progress
- **Status**: Partially completed with initial setup tasks done

#### `IMPLEMENTATION_SUMMARY.md`
- **Purpose**: Documents the git tag-based semver CI implementation
- **Content**: Summary of automated versioning system using GitHub Actions

### Development and Automation

#### `cleanup.py`
- **Purpose**: Comprehensive repository maintenance and automation script
- **Features**:
  - Status checking with tree generation, git status, code quality checks
  - Virtual environment management with uv
  - Package installation in development mode
  - Automated commit and push workflows
  - Repository content mixing with repomix
- **Commands**: status, venv, install, update, push
- **Integration**: Uses uv, ruff, mypy, pytest for development workflow

#### `.github/workflows/push.yml`
- **Purpose**: CI/CD workflow for pushes and pull requests
- **Jobs**:
  - Code quality checks (ruff linting/formatting, mypy type checking)
  - Multi-version testing (Python 3.10-3.12)
  - Distribution building
- **Tools**: Uses uv for dependency management, pytest for testing

#### `.github/workflows/release.yml`
- **Purpose**: Automated PyPI release workflow triggered by version tags
- **Process**: Build distributions, verify files, publish to PyPI, create GitHub release
- **Security**: Uses PYPI_TOKEN secret and trusted publishing

### Test Suite

#### `tests/test_tasks.py`
- **Purpose**: Unit tests for core task functions
- **Coverage**: Tests `extract_audio_task` and `generate_transcript_task`
- **Mocking**: Uses monkeypatch and mock to simulate time delays
- **Validation**: Checks JSON output format, processing simulation, return types

#### `tests/test_flows.py`
- **Purpose**: Integration tests for Prefect flows
- **Scope**: Tests the `process_video_flow` orchestration

#### `tests/test_package.py`
- **Purpose**: Package-level tests and imports
- **Validation**: Ensures proper package structure and API availability

#### `tests/test_video_transcript.py`
- **Purpose**: Tests for the `VideoTranscript` Pydantic model
- **Coverage**: Tests lazy evaluation, caching behavior, property access

### Examples and Usage

#### `examples/testprefect_example.py`
- **Purpose**: Demonstrates Prefect workflow usage
- **Status**: May be generic and not twat-task specific
- **Evaluation Needed**: Determine if it adds value to the package MVP

### Generated and Temporary Files

#### `CLEANUP.txt`
- **Purpose**: Generated log file from cleanup.py operations
- **Content**: Timestamps and outputs from repository maintenance
- **Git Status**: Should be in .gitignore

#### `REPO_CONTENT.txt`
- **Purpose**: Generated repository content dump from repomix tool
- **Usage**: Provides consolidated view of codebase for analysis
- **Git Status**: Should be in .gitignore

#### `llms.txt`
- **Purpose**: Generated log file for LLM context and operations
- **Content**: Timestamps and command outputs from cleanup.py
- **Git Status**: Should be in .gitignore

#### `LOG.md`
- **Purpose**: Project activity log for tracking changes and decisions
- **Format**: Markdown with dated entries

#### `VERSION.txt`
- **Purpose**: Version tracking file for manual version management
- **Integration**: May be redundant with hatch-vcs automatic versioning

### Configuration Directories

#### `.cursor/`
- **Purpose**: Cursor IDE-specific configuration and rules
- **Contains**: Coding standards, cleanup rules, file tree documentation
- **Usage**: IDE-specific guidance for development workflow

### Legal and Licensing

#### `LICENSE`
- **Purpose**: MIT license file defining usage terms
- **Standard**: Permissive open-source license
- **Required**: For public distribution and PyPI publishing

## Architecture Overview

The repository follows a modern Python package structure with:

1. **Hatch-based build system** for dependency and environment management
2. **Prefect workflow orchestration** for video processing tasks
3. **Pydantic models** for data validation and computed properties
4. **Comprehensive testing** with pytest and coverage reporting
5. **Automated CI/CD** with GitHub Actions for quality checks and releases
6. **Development automation** with cleanup.py for maintenance tasks

## Key Dependencies

- **Core**: prefect (>=3.1.0), pydantic (>=2.0.0), twat (>=1.8.1)
- **Development**: pytest, ruff, mypy, hatch
- **Build**: hatchling, hatch-vcs
- **CI/CD**: uv for package management

## Quality Assurance

The project implements multiple layers of quality assurance:
- **Pre-commit hooks** for automatic code formatting and linting
- **Multi-version testing** across Python 3.10-3.12
- **Type checking** with mypy for static analysis
- **Code formatting** with ruff for consistent style
- **Automated testing** with pytest and coverage reporting