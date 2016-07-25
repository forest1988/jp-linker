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
            'KEYWORD': {
                # --- sample table for 'KEYWORD' ---
                # 'NAME' : table name
                # columns[0] : column for keywords
                # columns[1] : column for urls
                # columns[2] : column for enable (0 or 1 )
                # You may make other columns for the table, but please set 3 items for this program as below.
                'NAME' : 'linker_keyword',
                'COLUMNS' : ('keyword_text', 'url', 'enable')
                },
            'TARGET': {
                # --- sample table for 'TARGET' ---
                # 'NAME' : table name
                # columns[0] : column for file paths
                # columns[1] : column for enable ( 0 or 1 )
                # You may make other columns for the table, but please set 2 items for this program as below.
                'NAME' : 'linker_target',
                'COLUMNS' : ('path', 'enable')
            }
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
