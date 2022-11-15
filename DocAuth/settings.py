"""
Django settings for DocAuth project.

Generated by 'django-admin startproject' using Django 4.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-gp-&h)w(21)$%1z=sc1765#o@bz7aut1n#=*iuv=f0uw6j*uff"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# 允许访问的主机ip，可以用通配符*
ALLOWED_HOSTS = []


# Application definition

# 用来注册App 前6个是django自带的应用
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "App.apps.TheAppConfig",
]

# 中间件 ,需要加载的中间件。比如在请求前和响应后根据规则去执行某些代码的方法
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# 指定URL列表文件 父级URL配置
# 当网站的一个接口被请求的时候，Django会找到ROOT_URLCONF设置的模块中名为urlpatterns的变量，然后按照顺序匹配这个变量中的每个URL模式，直到找到匹配的模式为止。
ROOT_URLCONF = "DocAuth.urls"

# 加载网页模板路径
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# WSGI的配置文件路径
WSGI_APPLICATION = "DocAuth.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# 数据库配置 默认的数据库为sqlite
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "OPTIONS": {
            "read_default_file": str(BASE_DIR / "confs/my.cnf"),
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators
# 相关密码验证
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/
# 语言设置 默认英语， 中文是zh-hans
LANGUAGE_CODE = "en-us"
# 时区设置，中国的是：Asia/Shanghai
TIME_ZONE = "UTC"
# i18n字符集是否支持
USE_I18N = True
# 是否使用timezone
# 保证存储到数据库中的是 UTC 时间；
# 在函数之间传递时间参数时，确保时间已经转换成 UTC 时间；
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/
# 静态文件路径
STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Rest framework settings
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly"
    ]
}
