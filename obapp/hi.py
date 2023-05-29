from django.apps import apps
app_models = apps.get_models()
print(app_models)