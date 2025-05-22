import os

from config.components.base import BASE_DIR, DEBUG

ROOT_URLCONF = "urls"

# 模板页面配置
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": (os.path.join(BASE_DIR, "templates"),),
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "config.context_processors.web_env.custom_settings",
            ],
        },
    }
]

INSTALLED_APPS = (
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "unfold.contrib.inlines",
    "unfold.contrib.import_export",
    "apps.base",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "rest_framework",
    "rest_framework.authtoken",
    "django_minio_backend",
    "django_filters",
    "mptt",
    "django_comment_migrate",
    "import_export",
    "django_select2",
    "apps.core",
    "nats_client",
    "allauth.socialaccount.providers.weixin",
)

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

AUTHENTICATION_BACKENDS = (
    "apps.core.backends.AuthBackend",  # this is default
    "apps.core.backends.APISecretAuthBackend",
    "django.contrib.auth.backends.ModelBackend",
    "apps.core.backends.SocialBackends",
)

AUTH_USER_MODEL = "base.User"

MIDDLEWARE = (
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    # "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    # 跨域检测中间件， 默认关闭
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # django国际化中间件
    "django.middleware.locale.LocaleMiddleware",
    "apps.core.middlewares.app_exception_middleware.AppExceptionMiddleware",
    "apps.core.middlewares.drf_middleware.DisableCSRFMiddleware",
    "apps.core.middlewares.api_middleware.APISecretMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "apps.core.middlewares.auth_middleware.AuthMiddleware",
)
SOCIALACCOUNT_PROVIDERS = {
    "weixin": {
        "AUTHORIZE_URL": "https://open.weixin.qq.com/connect/qrconnect",  # for media platform
        "SCOPE": ["snsapi_login"],
    }
}

LOGIN_REDIRECT_URL = os.getenv("LOGIN_REDIRECT_URL", "/")
if DEBUG:
    INSTALLED_APPS += (
        "corsheaders",
        "drf_yasg",
        "debug_toolbar",
    )  # noqa
    # 该跨域中间件需要放在前面
    MIDDLEWARE = (
        "corsheaders.middleware.CorsMiddleware",
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ) + MIDDLEWARE  # noqa
    CORS_ORIGIN_ALLOW_ALL = True
    CORS_ALLOW_CREDENTIALS = True
    CORS_ALLOW_HEADERS = [
        "accept",
        "authorization",
        "content-type",
        "user-agent",
        "x-csrftoken",
        "x-requested-with",
        "api-authorization",
        "debug",
    ]

# 获取 apps 目录下的所有子目录名称
APPS_DIR = os.path.join(BASE_DIR, "apps")
if os.path.exists(APPS_DIR):
    install_apps = os.getenv("INSTALL_APPS", "").split(",")
    app_folders = [
        name for name in os.listdir(APPS_DIR) if os.path.isdir(os.path.join(APPS_DIR, name)) and name in install_apps
    ]
else:
    app_folders = []
INSTALLED_APPS += tuple(f"apps.{app}" for app in app_folders)
