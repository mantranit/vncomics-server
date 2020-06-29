from app.models import Models
from app.utils.json import JSONParser

def CategoriesRoute(app):

    @app.route("/api/categories", methods=['GET'])
    def api_categories():
        return CategoriesAPI().CtrlGetAll()

    pass

class CategoriesAPI:
    def __init__(self):
        model = Models()
        self.categories = model.categories
    
    def CtrlGetAll(self):
        rows = self.categories.find()
        return JSONParser(list(rows))
