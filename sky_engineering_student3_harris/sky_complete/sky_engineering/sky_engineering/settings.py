"""
Django settings for the Sky Engineering Portal coursework project.

This file controls the project-wide configuration: installed apps, middleware,
database, templates, static files and login redirects.  The comments are written
for coursework marking so the purpose of each important setting is clear.
"""

from pathlib import Path

# BASE_DIR points to the outer project folder that contains manage.py.
# Using BASE_DIR avoids absolute file paths, so the project can run on another
# computer after being downloaded by a tutor or teammate.
BASE_DIR = Path(__file__).resolve().parent.parent

# Coursework/development key.  In a real deployed application this should be kept
# outside source code, for example in an environment variable.
SECRET_KEY = 'django-insecure-sky-engineering-cwk2-change-in-production-xyz123'

# DEBUG=True is acceptable for local coursework development because it shows
# helpful error pages.  It should be False in production.
DEBUG = True

# Allow all hosts so the project runs locally without host configuration issues.
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    # Built-in Django apps used for admin, authentication, sessions and static files.
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Coursework apps.  accounts handles registration/profile features and
    # messaging is the Student 3 individual element.
    'accounts',
    'messaging',

    # Other group apps can be added here, for example teams, organisation,
    # schedule or reports.  Keeping apps separate helps with group integration.
]

MIDDLEWARE = [
    # SecurityMiddleware adds basic security headers.
    'django.middleware.security.SecurityMiddleware',

    # Sessions and authentication allow Django to remember logged-in users.
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',

    # CSRF protection is important for forms such as login, registration and compose.
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',

    # Enables Django's temporary flash messages shown after actions like send/delete.
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Main URL file for the project.
ROOT_URLCONF = 'sky_engineering.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        # Project-level templates folder contains shared base templates and auth pages.
        'DIRS': [BASE_DIR / 'templates'],

        # APP_DIRS=True lets Django find app templates such as messaging/inbox.html.
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Standard Django processors used by templates.
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                # Adds unread_count to every page so the navbar can display it.
                'messaging.context_processors.unread_count',
            ],
        },
    },
]

# WSGI entry point used by Django's runserver and deployment servers.
WSGI_APPLICATION = 'sky_engineering.wsgi.application'

# SQLite is used because the coursework brief requires a DBMS suitable for the
# local Django project.  The database file is stored inside the project folder.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Django password validators support safer local account registration.
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/London'
USE_I18N = True
USE_TZ = True

# Static files are used for images such as the Sky logo and auth background.
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Default primary key type for new models.
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Login flow for the coursework application.
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/messaging/inbox/'
LOGOUT_REDIRECT_URL = '/accounts/login/'
