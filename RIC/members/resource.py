from import_export import resources
from .models import Bio,WorkshopBio

class BioResource(resources.ModelResource):
    class Meta:
        model = Bio