from flask import Flask, request, jsonify, abort
from datetime import datetime
import uuid

app = Flask(__name__)

# Хранилище для объявлений
ads = {}


# Функция для создания нового объявления
def create_ad(title, description, owner):
    ad_id = str(uuid.uuid4())
    ad = {
        "id": ad_id,
        "title": title,
        "description": description,
        "created_at": datetime.now().isoformat(),
        "owner": owner
    }
    ads[ad_id] = ad
    return ad


# Маршрут для создания нового объявления
@app.route('/ads', methods=['POST'])
def create_ad_route():
    data = request.json
    if not data or not all(k in data for k in ("title", "description", "owner")):
        return jsonify({"error": "Invalid request"}), 400

    ad = create_ad(data['title'], data['description'], data['owner'])
    return jsonify(ad), 201


# Маршрут для получения объявления по ID
@app.route('/ads/<ad_id>', methods=['GET'])
def get_ad_route(ad_id):
    ad = ads.get(ad_id)
    if not ad:
        return jsonify({"error": "Ad not found"}), 404

    return jsonify(ad), 200


# Маршрут для удаления объявления по ID
@app.route('/ads/<ad_id>', methods=['DELETE'])
def delete_ad_route(ad_id):
    ad = ads.pop(ad_id, None)
    if not ad:
        return jsonify({"error": "Ad not found"}), 404

    return jsonify({"message": "Ad deleted"}), 200


# Запуск сервера
if __name__ == '__main__':
    app.run(debug=True)
