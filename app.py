from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

users = {}
likes = {}
matches = []

@app.route('/register_user', methods=['POST'])
def register_user():
    data = request.json
    name = data.get('name')
    age = data.get('age')
    interests = data.get('interests', '')

    if not name or not age:
        return jsonify({'error': 'Имя и возраст обязательны'}), 400

    user_id = str(uuid.uuid4())
    users[user_id] = {
        'id': user_id,
        'name': name,
        'age': age,
        'interests': interests
    }
    likes[user_id] = set()

    return jsonify({'user_id': user_id})

@app.route('/get_profiles')
def get_profiles():
    user_id = request.args.get('user_id')
    if not user_id or user_id not in users:
        return jsonify([])

    profiles = [u for uid, u in users.items() if uid != user_id]
    return jsonify(profiles)

@app.route('/like_profile', methods=['POST'])
def like_profile():
    data = request.json
    user_id = data.get('user_id')
    profile_id = data.get('profile_id')

    if not user_id or not profile_id:
        return jsonify({'error': 'user_id и profile_id обязательны'}), 400
    if user_id not in users or profile_id not in users:
        return jsonify({'error': 'Пользователь не найден'}), 404

    likes[user_id].add(profile_id)

    if user_id in likes[profile_id]:
        place = "Кафе на Воробьевых горах"
        time = "Сегодня в 18:00"
        matches.append({'user1': user_id, 'user2': profile_id, 'place': place, 'time': time})
        return jsonify({'match': True, 'place': place, 'time': time})

    return jsonify({'match': False})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
