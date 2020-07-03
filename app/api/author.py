from flask import request, current_app as app
from app.models import Models
from app.utils.json import JSONParser

def AuthorRoute(app):

    @app.route("/api/authors", methods=['GET'])
    def api_authors():
        return AuthorAPI().CtrlGetAll(request.args)

    pass

class AuthorAPI:
    def __init__(self):
        model = Models()
        self.authors = model.authors
    
    def CtrlGetAll(self, parameters):
        rows = self.authors.find()

        total = self.authors.count()

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

        return JSONParser({
            "list": list(rows),
            "total": total,
            "skip": int(skip),
            "limit": int(limit)
        })
