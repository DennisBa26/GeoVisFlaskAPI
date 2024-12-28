from models import PLZ_PVModel
class PLZService:
    def __init__(self):
        self.model = PLZ_PVModel()

    def create(self, plz,pv):
        return self.model.create(plz,pv)