from flask import Flask, request, jsonify
import random
from datetime import datetime, timedelta

app = Flask(__name__)

users = {}  # user_id: {profile}
likes = {}  # user_id: set(liked_user_ids)
matches = []  # список матчей

meeting_places = [
    "Кофейня Salut в Шуваловском",
    "Лавочки у фонтана МГУ",
    "Библиотека в ДК",
    "Смотровая на Воробьевых горах",
    "Коворкинг на 4 этаже Шуваловки"
]

def generate_meeting():
    place = random.choice(meeting_places)
    day_offset = random.randint(1, 3)
    time = datetime.now() + timedelta(days=day_offset)
    return {
        "place": place,
        "date": time.strftime("%d.%m.%Y"),
        "time": time.strftime("%H:%M")
    }

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    user_id = data["user_id"]
    users[user_id] = {
        "name": data["name"],
        "faculty": data["faculty"],
        "gender": data["gender"],
        "interests": data.get("interests", []),
        "photo_url": data.get("photo_url", "")
    }
    likes[user_id] = set()
    return jsonify({"status": "registered"})

@app.route("/get_profiles", methods=["GET"])
def get_profiles():
    current_user = request.args.get("user_id")
    profiles = []
    for uid, profile in users.items():
        if uid != current_user and uid not in likes.get(current_user, set()):
            profiles.append({**profile, "user_id": uid})
    return jsonify(profiles)

@app.route("/like", methods=["POST"])
def like():
    data = request.json
    user_id = data["user_id"]
    liked_id = data["liked_user_id"]

    likes[user_id].add(liked_id)

    if liked_id in likes and user_id in likes[liked_id]:
        meeting = generate_meeting()
        match_info = {
            "user1": users[user_id]["name"],
            "user2": users[liked_id]["name"],
            "meeting": meeting
        }
        matches.append(match_info)
        return jsonify({"match": True, "meeting": meeting})
    return jsonify({"match": False})

@app.route("/matches", methods=["GET"])
def get_matches():
    return jsonify(matches)

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
