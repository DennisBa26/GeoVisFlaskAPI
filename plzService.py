from models import PLZ_PVModel
import json
class PLZService:
    def __init__(self):
        self.model = PLZ_PVModel()

    def create(self, request):
        for plz in request["plzs"]:
            self.model.create(plz["PLZ"], plz["PV"])
        return "OK"

    def get_all(self):
        return self.model.get_all()