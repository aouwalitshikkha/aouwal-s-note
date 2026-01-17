import os
import subprocess
import sys

def run(cmd):
    print("\n" + "=" * 60)
    print(f"RUNNING: {cmd}")
    print("=" * 60 + "\n")
    subprocess.run(cmd, shell=True)



print("=== Django Project Auto Setup (Windows) ===")

# 1. Inputs
project_name = input("Enter Django project name: ").strip()
apps_input = input("Enter app names (comma separated): ").strip()
apps = [app.strip() for app in apps_input.split(",") if app.strip()]
superuser_name = input("Enter superuser username: ").strip()
superuser_password = input("Enter superuser password: ").strip()

if not superuser_name or not superuser_password:
    print("Superuser username and password are required.")
    sys.exit(1)





if not project_name or not apps:
    print("Project name and at least one app are required.")
    sys.exit(1)

# 2. Create virtual environment
print("Creating virtual environment...")
run("python -m venv venv")

# 3. Activate venv (Windows)
activate_cmd = r"venv\Scripts\activate"
pip_cmd = r"venv\Scripts\pip"
python_cmd = r"venv\Scripts\python"

# 4. Install Django
print("Installing Django...")
run(f"{pip_cmd} install django Pillow")

# 5. Start Django project
print("Creating Django project...")
run(f"{python_cmd} -m django startproject {project_name} .")

# 6. Create apps
for app in apps:
    print(f"Creating app: {app}")
    run(f"{python_cmd} manage.py startapp {app}")

# 7. Add apps to INSTALLED_APPS (SAFE METHOD)
settings_path = os.path.join(project_name, "settings.py")

with open(settings_path, "r", encoding="utf-8") as f:
    lines = f.readlines()


new_lines = []
inside_installed_apps = False

for line in lines:
    new_lines.append(line)

    if line.strip().startswith("INSTALLED_APPS = ["):
        inside_installed_apps = True
        continue

    if inside_installed_apps and line.strip().startswith("]"):
        for app in apps:
            new_lines.insert(
                len(new_lines) - 1,
                f"    '{app}',\n"
            )
        inside_installed_apps = False

with open(settings_path, "w", encoding="utf-8") as f:
    f.writelines(new_lines)


# 7.1 Add static & media settings (NO DUPLICATES)
settings_path = os.path.join(project_name, "settings.py")

with open(settings_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
has_static_root = False
has_media_root = False

for line in lines:
    new_lines.append(line)

    if line.strip().startswith("STATIC_ROOT"):
        has_static_root = True
    if line.strip().startswith("MEDIA_ROOT"):
        has_media_root = True

    # Insert after STATIC_URL if missing
    if line.strip().startswith("STATIC_URL") and not has_static_root:
        new_lines.append("STATIC_ROOT = BASE_DIR / 'staticfiles'\n")
        new_lines.append("STATICFILES_DIRS = [BASE_DIR / 'static']\n\n")
        has_static_root = True

# Append media settings at end if missing
if not has_media_root:
    new_lines.append("\nMEDIA_URL = '/media/'\n")
    new_lines.append("MEDIA_ROOT = BASE_DIR / 'media'\n")

with open(settings_path, "w", encoding="utf-8") as f:
    f.writelines(new_lines)

# Create folders
os.makedirs("static", exist_ok=True)
os.makedirs("media", exist_ok=True)


# 8. Create urls.py in apps
for app in apps:
    urls_path = os.path.join(app, "urls.py")
    with open(urls_path, "w", encoding="utf-8") as f:
        f.write(
            "from django.urls import path\n\n"
            "urlpatterns = [\n"
            "]\n"
        )

# 9. Update project urls.py (SAFE)
project_urls_path = os.path.join(project_name, "urls.py")

with open(project_urls_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
has_include = False
has_admin = False

for line in lines:
    if "include" in line:
        has_include = True
    if "admin.site.urls" in line:
        has_admin = True
    new_lines.append(line)

# Fix import
for i, line in enumerate(new_lines):
    if line.startswith("from django.urls import"):
        if "include" not in line:
            new_lines[i] = line.replace("path", "path, include")

# Fix urlpatterns
for i, line in enumerate(new_lines):
    if line.strip() == "urlpatterns = [":
        insert_index = i + 1
        for app in apps:
            new_lines.insert(
                insert_index,
                f"    path('{app}/', include('{app}.urls')),\n"
            )
            insert_index += 1
        break

with open(project_urls_path, "w", encoding="utf-8") as f:
    f.writelines(new_lines)

# Add static & media url patterns (SAFE)
project_urls_path = os.path.join(project_name, "urls.py")

with open(project_urls_path, "r", encoding="utf-8") as f:
    urls = f.read()

if "static(" not in urls:
    if "from django.conf import settings" not in urls:
        urls = urls.replace(
            "from django.contrib import admin",
            "from django.contrib import admin\nfrom django.conf import settings"
        )

    if "from django.conf.urls.static import static" not in urls:
        urls = urls.replace(
            "from django.conf import settings",
            "from django.conf import settings\nfrom django.conf.urls.static import static"
        )

    urls += """

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
"""

with open(project_urls_path, "w", encoding="utf-8") as f:
    f.write(urls)



# 10. Create .gitignore
gitignore_content = """
# Python
__pycache__/
*.py[cod]
*.sqlite3
*.log

# Virtual Environment
venv/

# Django
*.env
media/
staticfiles/

# VS Code
.vscode/

# OS
.DS_Store
"""

with open(".gitignore", "w", encoding="utf-8") as f:
    f.write(gitignore_content.strip())

# 11. Create requirements.txt
print("Creating requirements.txt...")
run(f"{pip_cmd} freeze > requirements.txt")

# 12. Git init & first commit
print("Initializing Git repository...")
run("git init")
run("git add .")
run('git commit -m "first commit"')


# 13. Running Migrations
print("Running migrations...")
run(f"{python_cmd} manage.py migrate")

# 14 Creating Super User
print("Creating superuser...")

env = os.environ.copy()
env["DJANGO_SUPERUSER_USERNAME"] = superuser_name
env["DJANGO_SUPERUSER_PASSWORD"] = superuser_password
env["DJANGO_SUPERUSER_EMAIL"] = f"{superuser_name}@example.com"

subprocess.check_call(
    f"{python_cmd} manage.py createsuperuser --noinput",
    shell=True,
    env=env
)


# 13. Open VS Code
print("Opening project in VS Code...")
run("code .")

print("\n✅ Django project setup complete!")
print("👉 Activate venv manually with:")
print("   venv\\Scripts\\activate")
