# automacoes

Project to manage and automate an office hardware inventory (computers and related equipment).

> A small Python project to track, manage and automate workflows around the office's computer hardware stock. Designed to work with PostgreSQL in typical deployments.

Badges
- License: MIT
- Language: Python
- Topics: postgresql, python

Table of Contents
- [About](#about)
- [Features](#features)
- [Tech stack](#tech-stack)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Database setup](#database-setup)
- [Usage](#usage)
- [Development](#development)
- [Tests](#tests)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

About
-----
This repository contains tools and automation for creating and maintaining an office hardware inventory. Typical responsibilities:
- Add / remove equipment (computers, monitors, peripherals) (remove equipment not working for now, bcse idnt create this feature yet)
- works for now only for the windows SO

Features
--------
- Inventory CRUD operations for hardware items
- PostgreSQL-backed storage

Tech stack
----------
- Python (project language)
- PostgreSQL (primary persistence)

Requirements
------------
- Python 3.9+ (adjust as needed)
- pip
- PostgreSQL server
- (Recommended) virtualenv or venv for development

Installation
------------
1. Clone the repository:
   git clone https://github.com/Renaolol/automacoes.git
   cd automacoes

2. Create a virtual environment and activate it:
   python -m venv .venv
   .venv\Scripts\activate      # Windows (PowerShell)

3. Install dependencies:
   pip install -r requirements.txt

If the project does not include a requirements file yet, install the packages you need (for example, psycopg[binary], SQLAlchemy, click, etc.) and add them to requirements.txt.

Configuration
-------------
The project expects configuration for the database and other environment-specific settings. Use a `.env` file or environment variables.

Example `.env` (template)
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=automacoes_db
DB_USER=automacoes_user
DB_PASS=supersecret
# Optional
LOG_LEVEL=INFO
```

How your application reads config may vary (example: python-dotenv or another config loader). Adapt the variables to your code.

Database setup
--------------
Example steps to create a PostgreSQL role and database:

1. As a PostgreSQL superuser:
   sudo -u postgres psql

2. Then execute:
   CREATE USER automacoes_user WITH PASSWORD 'supersecret';
   CREATE DATABASE automacoes_db OWNER automacoes_user;
   \q

3. Run your migrations or initialization scripts (if present):
   # Example (replace with project's migration command)
   alembic upgrade head
   # or
   python scripts/init_db.py

Usage
-----
How to run the main script or CLI will depend on the project layout. Here are typical examples:

- Run a script:
  python main.py

- Run as a module:
  python -m automacoes

- Use CLI commands (example for a Click-based CLI):
  python -m automacoes list
  python -m automacoes add --name "Workstation-01" --serial "SN12345" --assigned-to "Alice"

- Export inventory to CSV:
  python -m automacoes export --format csv --output inventory.csv

Replace the commands above with the actual entry points and subcommands implemented in the repository.

Development
-----------
Recommended workflow for contributors:
1. Create a feature branch:
   git checkout -b feat/your-feature

2. Implement changes, add tests, update docs.

3. Run linter and tests locally:
   flake8 .
   black --check .
   pytest

4. Commit and open a PR against `main`.

Tests
-----
If the repository includes tests, run them with:
pytest

Add tests for new features and maintain test coverage. If there are no tests yet, consider adding a basic test suite that verifies core inventory operations.

Contributing
------------
Contributions are welcome. Suggestions:
- Open an issue to discuss larger changes.
- Provide small, focused pull requests.
- Include tests and update documentation for new features.
- Follow the repository's code style (add linter/format config if not present).

License
-------
This project is licensed under the MIT License. See LICENSE for details.

Contact
-------
Repo owner: [Renaolol](https://github.com/Renaolol)

Acknowledgements / Next steps
----------------------------
- Consider adding: a requirements.txt, example .env file, migration scripts, and a minimal example dataset to help new users try the project quickly.
- If you'd like, I can create and commit this README.md to the repository or tailor the README to reflect exact commands/entrypoints found in the codebase—tell me if you want me to add it as a commit/PR or to adapt the content after I inspect the repo structure in more detail.
