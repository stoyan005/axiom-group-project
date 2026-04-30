# Sky Engineering Portal – Messaging Module
## 5COSC021W Coursework | Group Axiom | Student: Harris Bourou (w2046023)

### Stack
- Python 3.10+
- Django 4.2
- SQLite (db.sqlite3 — auto-created on first migrate)
- Bootstrap 5.3 + Bootstrap Icons (CDN)
- DM Sans font (Google Fonts CDN)

### Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create database and run migrations
python manage.py migrate

# 3. (Optional) Create a superuser for admin panel
python manage.py createsuperuser
## Admin Panel

The Django admin panel can be accessed at:

http://127.0.0.1:8000/admin/

To create an admin/superuser account, run:

python manage.py createsuperuser

# 4. Run the development server
python manage.py runserver
```

Then open http://127.0.0.1:8000 in your browser.

### URL Structure
| URL | View |
|-----|------|
| / | Redirects to /messaging/inbox/ |
| /accounts/login/ | Login |
| /accounts/register/ | Self-registration |
| /accounts/profile/ | User profile |
| /accounts/change-password/ | Change password |
| /messaging/inbox/ | Inbox |
| /messaging/sent/ | Sent messages |
| /messaging/drafts/ | Drafts |
| /messaging/compose/ | New message |
| /messaging/view/<id>/ | View a message |
| /messaging/draft/<id>/ | Edit a draft |
| /messaging/delete/<id>/ | Delete a message |
| /messaging/toggle/<id>/ | Toggle read/unread |
| /messaging/api/unread-count/ | JSON unread badge API |
| /admin/ | Django admin panel |

### Apps
- **accounts** — User registration, login, profile, password change
- **messaging** — Inbox, sent, drafts, compose, view, delete, read-status

### UI Update
- Added a moon/sun theme toggle in the top navigation.
- The selected theme is saved in `localStorage` as `sky-theme`, so the portal remembers the user's light/dark preference across pages.
- Shared CSS variables in `templates/base/base.html` now support both light mode and dark mode across authentication, messaging, profile, and password pages.
