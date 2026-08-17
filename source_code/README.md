# Agriculture Process Management System

A submission-ready academic Django project for managing farm records, crops, cultivation activities, expenses, harvests, sales, and reports. The application uses Django 5.2 LTS, Bootstrap, and SQLite for development. It is organized with secure authentication, farmer-owned records, CRUD screens, search, pagination, report summaries, migrations, tests, demo data, deployment files, diagrams, and academic documentation.

## Quick Start

```powershell
cd source_code
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

Open http://127.0.0.1:8000 and log in with `demo_farmer` / `DemoPass123`.

## Main Modules

- Authentication Module
- Farm Management Module
- Crop Management Module
- Activity Management Module
- Expense Management Module
- Harvest Management Module
- Reports Management Module

The documentation folder contains the full academic report, setup guide, deployment guide, project guide, troubleshooting guide, and test report.
