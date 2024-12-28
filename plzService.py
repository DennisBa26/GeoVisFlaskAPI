from models import PLZ_PVModel
class PLZService:
    def __init__(self):
        self.model = PLZ_PVModel()

    def create(self, request):
        return self.model.create(request["PLZ"], request["PV"])

    def get_all(self):
        return self.model.get_all()