from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import secrets
app = Flask(__name__)
CORS(app)
DATA_FILE = os.path.join(
    os.path.dirname(__file__),
    "admin_translations.json"
)


def load_translations():
    if not os.path.exists(DATA_FILE):
        return {}

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_translations(data):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=2
        )

@app.post("/api/admin/login")
def admin_login():

    data = request.get_json() or {}

    password = str(
        data.get("password", "")
    )

    admin_password = os.environ.get(
        "ADMIN_PASSWORD",
        ""
    )

    if (
    admin_password
    and secrets.compare_digest(
        password.encode("utf-8"),
        admin_password.encode("utf-8")
    )
):
        return jsonify({
            "success": True,
            "message": "Admin login successful."
        })

    return jsonify({
        "success": False,
        "message": "Invalid password."
    }), 401
@app.get("/api/translations")
def get_translations():
    return jsonify(load_translations())


@app.post("/api/translations")
def update_translation():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "No data received."
        }), 400

    surah = str(data.get("surah", "")).strip()
    ayah = str(data.get("ayah", "")).strip()
    translation = str(data.get("translation", "")).strip()

    if not surah or not ayah:
        return jsonify({
            "success": False,
            "message": "Surah and ayah are required."
        }), 400

    if not translation:
        return jsonify({
            "success": False,
            "message": "Translation cannot be empty."
        }), 400

    translations = load_translations()

    if surah not in translations:
        translations[surah] = {}

    translations[surah][ayah] = translation

    save_translations(translations)

    return jsonify({
        "success": True,
        "message": "Translation saved."
    })


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )