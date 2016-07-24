# --- DataBase settings ---

# --- Default setting (overwritten by 'args' called when you run 'linker.py')
# ------ If you want to change default setting, please rewrite values of default_set.
# ------ Please DO NOT change the keys of default_set.

default_set = {
    'DATABASESYSTEM' : 'sqlite',
    'DATABASE' : 'sample',
}

# --- sqlite sample

DATABASES = {
    'sample' : {
        'ENGINE': 'django.db.backends.sqlite3',
        'DBPATH': '/Users/shadetree/workspace/django_test/mysite/db.sqlite3',
        'TABLES': {
            'KEYWORD': 'polls_keyword',
            'HTML': '',
        }
    },
    'mysqltemplate': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'template1',
        'USER': 'DB_USER_NAME',
        'PASSWORD': 'DB_USER_PASSWORD',
        'HOST': 'DB_HOST',
        'PORT': int('5432'),
        'TABLES': {
            'keyword': 'polls_keyword',
            'html': '',
        }
    }
}
