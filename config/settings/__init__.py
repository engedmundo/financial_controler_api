from .database import DATABASES
from .default_auto_field import DEFAULT_AUTO_FIELD
from .i18n import LANGUAGE_CODE, TIME_ZONE, USE_I18N, USE_TZ
from .installed_apps import INSTALLED_APPS
from .login_logout import LOGIN_REDIRECT_URL, LOGIN_URL
from .middleware import MIDDLEWARE
from .rest_framework import REST_FRAMEWORK
from .security import (
    ALLOWED_HOSTS,
    AUTH_PASSWORD_VALIDATORS,
    CORS_ALLOWED_ORIGINS,
    DEBUG,
    SECRET_KEY,
)
from .simple_jwt import SIMPLE_JWT
from .static import (
    BASE_DIR,
    STATIC_ROOT,
    STATIC_URL,
    STATICFILES_DIRS,
    TEMPLATES,
)
from .urls import ROOT_URLCONF
from .wsgi_config import WSGI_APPLICATION
