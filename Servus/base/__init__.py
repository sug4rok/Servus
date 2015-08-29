# coding=utf-8
from base.settings import EXTENDED_APPS

# If in the database there is a table fill the table base_application
from django.db.utils import OperationalError, ProgrammingError
try:
    from base.models import Application
    for ext_app in EXTENDED_APPS:
        app, created = Application.objects.get_or_create(name=ext_app)
        if app.name == 'home':
            app.is_tab = True
        if app.tab_name == '':
            app.tab_name = ext_app.capitalize()
        app.save()
except (OperationalError, ProgrammingError):
    pass