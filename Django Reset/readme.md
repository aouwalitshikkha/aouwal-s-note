# Django One-Shot Reset Script

This script **completely resets a Django project** and brings it back to a clean, runnable state in one command.  
It is designed for **local development only** and is intentionally destructive.

If you’re tired of manually deleting virtual environments, databases, and migrations every time something breaks — this script does it for you.

---

## What This Script Does (Exactly)

When you run the script, it performs the following steps **in order**:

1. **Deletes the existing virtual environment**
   - Removes the `env/` folder entirely

2. **Deletes the SQLite database**
   - Removes `db.sqlite3` (fails safely if the file is in use)

3. **Deletes Django migration files**
   - Removes all migration `.py` files **except** `__init__.py`

4. **Creates a fresh virtual environment**
   - Uses `python -m venv env`

5. **Installs dependencies**
   - If `requirements.txt` exists → installs from it  
   - Otherwise installs:
     - `django`

6. **Rebuilds the database**
   - Runs `makemigrations`
   - Runs `migrate`

7. **Creates a Django superuser**
   - Uses the credentials you define in the script
   - Skips creation if the user already exists

---

## Requirements

- Python **3.9+**
- Django project with:
  - `manage.py` in the same directory
- Windows (uses `env/Scripts/` paths)

> ⚠️ This script is **not tested for macOS/Linux** without path changes.

---

## Setup (Important)

Before running the script, open it and update these values:

```python
USERNAME = "admin"
PASSWORD = "admin123"
EMAIL = "admin@example.com"
```
⚠️ Do not use real production credentials.

## How to Run

From your Django project root:
```
python reset_django.py
```
Sit back and let it finish.
If something fails, the script stops immediately and prints the error.