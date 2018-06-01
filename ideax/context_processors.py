from decouple import config
from django.conf import settings

def export_vars(request):
    return {"PIWIK_URL" : config("PIWIK_URL", default=""),
            "PIWIK_ID" : config("PIWIK_ID", default=""),
            "DIALOGFLOW_ID" : config("DIALOGFLOW_ID", default=""),
            "PERMISSIONS" : settings.PERMISSIONS,}
