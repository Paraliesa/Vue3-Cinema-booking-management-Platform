# custom_backend.py
from django.db.backends.mysql import base

class DatabaseWrapper(base.DatabaseWrapper):
    def get_connection_params(self):
        params = super().get_connection_params()
        params['sql_mode'] = 'ANSI'
        return params