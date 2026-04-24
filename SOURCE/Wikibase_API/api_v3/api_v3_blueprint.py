from flask import Blueprint, jsonify, request
from .qudt_service import search_qudt

api_v3 = Blueprint("api_v3", __name__)

@api_v3.route("/info")
def info():
    return jsonify({"name": "Meine API", "version": "1.0"})

@api_v3.route("/search", methods=["GET"])
def search():
    search_term = request.args.get("search", "")
    lang = request.args.get("lang", "en")
    types = request.args.get("types", "unit").split(",")

    result = search_qudt(search=search_term, lang=lang, types=types)
    return jsonify(result)  

# ---------------------------------------------
# Wenn die Suche komplexer wird:
# ---------------------------------------------
# @api_v3.route("/search", methods=["POST"])
# def search_route():
#     data = request.get_json(force=True)
#     search = data.get("search", "")
#     lang = data.get("lang", "en")
#     types = data.get("types", ["unit"])

#     result = search_qudt(search=search, lang=lang, types=types)
#     return jsonify(result)    


# ---------------------------------------------
# Dann muss das folgende für die Integration in das Frontend:
# ---------------------------------------------
# fetch("/api/v3/search", {
#   method: "POST",
#   headers: { "Content-Type": "application/json" },
#   body: JSON.stringify({
#     search: "Volt",
#     lang: "en",
#     types: ["unit"]
#   })
# });