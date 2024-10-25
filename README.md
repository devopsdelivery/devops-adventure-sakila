Our branching strategy is designed to streamline collaboration and ensure a smooth development workflow. This document outlines the key branches we use, naming conventions, and guidelines for branching and merging.

Branches
1. Main Branch
Name: main
Purpose: The stable version of the codebase, ready for production deployment.
Protection Rules:
Only merged via pull requests (PRs), always a review needed, restricted to other users but not to the admins.
Must pass all tests and code reviews before merging.

2. Development Branch
Name: develop
Purpose: The integration branch for features and fixes. All completed work should be merged here before release.
Merge Strategy:
PRs should be merged into develop once code reviews are approved.
Continuous integration (CI) checks must pass.
