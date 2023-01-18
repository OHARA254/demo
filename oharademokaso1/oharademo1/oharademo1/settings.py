"""
Django settings for oharademo1 project.

Generated by 'django-admin startproject' using Django 4.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-7lw8ca6wk9-5hg+mtgsz_$p1%lg9n7@$d-)o^eg^v7^%+81s$$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['7934-223-29-13-138.jp.ngrok.io']#127.0.0.1
ALLOWED_HOSTS = ['127.0.0.1']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'maintenance_mode',
    'app.apps.AppConfig',
    'accounts.apps.AccountsConfig',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'django.contrib.sites',
    'django_bootstrap5',    
    'widget_tweaks',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'maintenance_mode.middleware.MaintenanceModeMiddleware'
]

ROOT_URLCONF = 'oharademo1.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'app/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'oharademo1.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS=(
    os.path.join(BASE_DIR,'static'),
    )

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


AUTH_USER_MODEL='accounts.CustomUser'

#django-allauthで利用するdjango.contrib.sitesを使うためにサイト識別用IDを設定
SITE_ID=1

AUTHENTICATION_BACKENDS=(
    'allauth.account.auth_backends.AuthenticationBackend',
    #一般ユーザー用メールアドレス
    'django.contrib.auth.backends.ModelBackend',
    #管理サイト用メールアドレス
)

ACCOUNT_FORMS = {
'signup': 'accounts.forms.CustomSignupForm',
}

#signupformからの情報をcustomusermodelに保存するのに必要
ACCOUNT_ADAPTER = 'accounts.adapter.AccountAdapter'


#サインアップにメールアドレス確認をはさむように設定
ACCOUNT_EMAIL_VERIFICATION='mandatory'
ACCOUNT_EMAIL_REQUIRED=True

#ログイン、ログアウト後の設定
LOGIN_REDIRECT_URL='app:index'
ACCOUNT_LOGOUT_REDIRECT_URL='app:index'

#ログアウトリンクのクリック一発でログアウトする設定
ACCOUNT_LOGOUT_ON_GET=False

#django-allauthが送信するメールの件名に自動付与される接頭辞をブランクする設定
ACCOUNT_EMAIL_SUBJECT_PREFIX=''

#デフォルトのメール送信先を設定
DEFOULT_FROM_EMAIL=os.environ.get('FROM_EMAIL')

#メールアドレス認証に変更する設定
ACCOUNT_AUTHENTICATION_METHOD='email'
ACCOUNT_USERNAME_REQUIRED=False


LOGGING={
    'version':1, #1固定
    'disable_existing_loggers':False,

    #ロガーの設定
    'loggers':{
        #Djamgoが利用するロガー
        'django':{
            'hanbdlers':['console'],
            'level':'INFO',
        },
        #diaryアプリケーションが利用するロガー
        'app':{
            'handlers':['console'],
            'level':'DEBUG',
        },
    },
    'handlers':{
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter':'dev'
        },
    },

    #フォーマッタの設定
    'formatters':{
        'dev':{
            'format':'\t'.join([
                '%(asctime)s',
                '[%(levelname)s]',
                '%(pathname)s(lineno)d)',
                '%(message)s'
            ])
        },
    }
}

EMAIL_BACKEND='django.core.mail.backends.console.EmailBackend'

# 画像追加
MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MAINTENANCE_MODE_IGNORE_ADMIN_SITE = True

MAINTENANCE_MODE_IGNORE_SUPERUSER = True