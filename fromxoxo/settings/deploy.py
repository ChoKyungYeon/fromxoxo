from .base import *

def read_secret(secret_name):
    file = open('/run/secrets/' + secret_name)
    secret =file.read()
    secret = secret.rstrip().lstrip()
    file.close()
    return secret

env = environ.Env(
    DEBUG=(bool, False)
)


environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


SECRET_KEY = read_secret('DJANGO_SECRET_KEY') # secretkey 수정
SENS_ACCESS_KEY= read_secret('SENS_ACCESS_KEY')
SENS_SECRET_KEY= read_secret('SENS_SECRET_KEY')
SENS_SERVICE_KEY= read_secret('SENS_SERVICE_KEY')
DEBUG = False #deploy check ,

ALLOWED_HOSTS = ['*'] #모든 호스트를 허용

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'fromxoxo_db', # yml 파일과 이름 맞춰주기
        'USER': 'fromxoxo_admin', # yml 파일과 이름 맞춰주기
        'PASSWORD': read_secret('MYSQL_PASSWORD'),  # maridb 비밀번호 수정
        'HOST': 'mariadb',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
            'use_unicode': True,
        },
    }
}
