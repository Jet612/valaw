## Description
## Metadata Checklist
- [ ] **Version Number**: Is the version in `pyproject.toml` (or `setup.py`) correct for this branch? 
    - *Example: `0.1.11.dev1` for development or `0.1.11` for stable.*
- [ ] **Development Status**: Does the Trove Classifier match the release intent?
    - *`3 - Alpha` / `4 - Beta` / `5 - Production/Stable`*
- [ ] **Dependencies**: Have any new libraries been added to the installation requirements?

## Quality Assurance
- [ ] **Tests**: Have you run `pytest` locally?
- [ ] **Linting**: Is the code formatted correctly?

## Deployment Intent
- [ ] **Production Release**: Is this PR targeting `main` and meant for the real PyPI?
- [ ] **Development/Testing**: Is this meant for TestPyPI or a pre-release version?
