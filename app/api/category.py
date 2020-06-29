from flask import request, current_app as app
from app.models import Models
from app.utils.json import JSONParser

def CategoryRoute(app):

    @app.route("/api/categories", methods=['GET'])
    def api_categories():
        return CategoryAPI().CtrlGetAll(request.args)

    pass

class CategoryAPI:
    def __init__(self):
        model = Models()
        self.categories = model.categories
    
    def CtrlGetAll(self, parameters):
        rows = self.categories.find()

        sort = parameters.get("sort")
        if sort:
            if sort[0] == "-":
                rows.sort({ sort.strip("-"): -1 })
            else:
                rows.sort({ sort: 1 })

        skip = parameters.get("skip")
        if not skip:
            skip = 0
        rows.skip(int(skip))

        limit = parameters.get("limit")
        if not limit:
            limit = app.config["PAGE_SIZE_DEFAULT"]
        rows.limit(int(limit))

        return JSONParser(list(rows))
