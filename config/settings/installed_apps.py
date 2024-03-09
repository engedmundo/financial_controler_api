INSTALLED_APPS = [
    # django admin custom
    "jazzmin",
    # django default apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 3rd apps
    "rangefilter",
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
    # project apps
    "apps.core",
    "apps.family_manager",
    "apps.account_manager",
    "apps.financial_manager",
]
