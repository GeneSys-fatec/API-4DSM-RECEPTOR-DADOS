from flask import request
from flask_restx import Namespace, Resource

from config import get_db_collection

receptor = Namespace(
    "receptor",
    description="Recebe leituras dos sensores e persiste no MongoDB.",
    path="/receptor",
)

collection = get_db_collection()


@receptor.route("")
class ReceptorResourcePost(Resource):
    @receptor.doc("post")
    def post(self):
        data = request.get_json(silent=True)

        if not data:
            return {"error": "JSON inválido"}, 400

        result = collection.insert_one(data)

        return {"status": "salvo", "db_id": str(result.inserted_id)}, 201