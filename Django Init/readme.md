# Django Project Auto Setup (Windows)

This script automatically creates and configures a Django project on **Windows**, saving you from repetitive setup tasks.

## 🚀 What It Does
- Creates a virtual environment
- Installs Django & Pillow
- Creates a Django project and multiple apps
- Registers apps in `INSTALLED_APPS`
- Configures **static** and **media** files
- Sets up app-level `urls.py` and project routing
- Runs migrations
- Creates a Django superuser (non-interactive)
- Initializes Git and makes the first commit
- Generates `.gitignore` and `requirements.txt`
- Opens the project in VS Code

## 🧰 Requirements
- Python 3.10+
- Git
- VS Code (optional, but recommended)
- Windows OS

## ▶️ How to Use
1. Save the script as `setup.py`
2. Open Command Prompt or PowerShell
3. Run:
   ```bash
   python start_django.py
```

## 📌 Notes

1. Superuser email is auto-generated as username@example.com

2. Static and media folders are created automatically

3. Safe file edits prevent duplicate settings