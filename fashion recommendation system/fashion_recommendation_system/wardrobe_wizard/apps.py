from django.apps import AppConfig


class WardrobeWizardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'wardrobe_wizard'

    def ready(self):
        import wardrobe_wizard.signals

