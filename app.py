from flask import Flask, jsonify, request, Response

app = Flask(__name__)
users = {}
next_user_id = 1

@app.route("/users", methods=['GET'])
def get_users():
    return jsonify(list(users.values())), 200

@app.route("/users/<int:user_id>", methods=['GET'])
def get_user(user_id):
    user = users.get(user_id)
    if user:
        return jsonify(user), 200
    return jsonify({"error": "User not found"}), 404

@app.route("/users", methods=['POST'])
def create_user():
    global next_user_id
    if not request.json or 'name' not in request.json or 'lastname' not in request.json:
        return Response(status=400)
    data = {'id': next_user_id, 'name': request.json['name'], 'lastname': request.json['lastname']}
    users[next_user_id] = data
    next_user_id += 1
    return jsonify(data), 201

@app.route("/users/<int:user_id>", methods=['PATCH'])
def update_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404
    if not request.json:
        return Response(status=400)
    
    valid_keys = {'name', 'lastname'}
    if not all(key in valid_keys for key in request.json.keys()):
        return jsonify({"error": "Invalid fields"}), 400

    user = users[user_id]
    user.update({k: request.json[k] for k in request.json if k in valid_keys})
    return Response(status=204)

@app.route("/users/<int:user_id>", methods=['PUT'])
def replace_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404
    if not request.json or 'name' not in request.json or 'lastname' not in request.json:
        return Response(status=400)
    users[user_id] = {'id': user_id, 'name': request.json['name'], 'lastname': request.json['lastname']}
    return Response(status=204)

@app.route("/users/<int:user_id>", methods=['DELETE'])
def delete_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404
    del users[user_id]
    return Response(status=204)

if __name__ == "__main__":
    app.run(debug=True)
