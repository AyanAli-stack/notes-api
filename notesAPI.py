from flask import Flask, jsonify, request
import jwt
import psycopg2
from dotenv import load_dotenv
import os
import bcrypt
app = Flask(__name__)
load_dotenv()
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")



conn = psycopg2.connect(
    dbname="notes_db",
    user="ayanali123",
    password="123456",
    host="postgres-db"
)





@app.route("/")
def home():
    return "Simple Notes API Running"

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    if not data or "username" not in data or not data["username"] or "password" not in data or not data["password"]:
        return jsonify({"error": "username and password fields are required"}), 400
    cur = conn.cursor()
    hashed_password = bcrypt.hashpw(data["password"].encode("utf-8"),
        bcrypt.gensalt())                            
    cur.execute(
        "INSERT INTO users (username, password) VALUES (%s, %s)", (data["username"], hashed_password.decode("utf-8"))
    )
    conn.commit()
    return jsonify({"message": "User created successfully"}),201

@app.route("/login", methods =["POST"])
def login():
    data = request.json

    if not data or "username" not in data or not data["username"] or "password" not in data or not data["password"]:
        return jsonify({"error": "username and password required"}), 400
    cur = conn.cursor()

    cur.execute(
        "SELECT id, password FROM users WHERE username = %s",
        (data["username"],)
    )
    user = cur.fetchone()

    if not user:
        return jsonify({"error": "Invalid username or passsword"}), 401
    
    user_id, stored_password = user

    
    if not bcrypt.checkpw(
        data["password"].encode("utf-8"),
        stored_password.encode("utf-8")
    ):
        return jsonify({"error": "Invalid username or password"}), 401

    
    token = jwt.encode(
    {
        "user_id": user_id
    },
    app.config["SECRET_KEY"],
    algorithm="HS256"
)

    return jsonify({
    "message": "Login successful",
    "token": token
}), 200
   


@app.route("/notes", methods=["GET"])
def get_notes():
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return jsonify({"error": "Token missing"}),401
    token = auth_header.split(" ")[1]
    decoded = jwt.decode(token, app.config["SECRET_KEY"],algorithms=["HS256"])
    user_id = int(decoded["user_id"])
    print("USER ID FROM TOKEN:", user_id)

    cur = conn.cursor()
    user_id = int(decoded["user_id"])
    page = request.args.get("page")
    limit = request.args.get("limit") 
    
    if page and limit:
        page = int(page)
        limit = int(limit)
        offset = (page -1) *limit
        cur.execute(
        "SELECT * FROM notes WHERE user_id = %s LIMIT %s OFFSET %s",
        (user_id, limit, offset)
        )
    else:
        print("USER ID USED IN QUERY:", user_id)
        cur.execute("SELECT * FROM notes WHERE user_id = %s",(user_id,))
    rows = cur.fetchall()
    notes = []
    for row in rows:
        notes.append({
            "id": row[0],
            "content": row[1]
        })

    return jsonify(notes)
    

@app.route("/notes", methods=["POST"])
def create_note():
    cur = conn.cursor()
    data = request.json
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return jsonify({"error": "Token missing"}), 401

    parts = auth_header.split(" ")
    if len(parts) != 2 or parts[0] != "Bearer":
        return jsonify({"error": "Invalid token format"}), 401

    token = parts[1]

    decoded = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
    user_id = int(decoded["user_id"])

    if not data or "content" not in data or not data["content"]:
        return jsonify({"error": "content field is required"}), 400

    cur.execute(
        "INSERT INTO notes (content, user_id) VALUES (%s, %s) RETURNING id",
        (data["content"],user_id)
    )

    new_id = cur.fetchone()[0]
    conn.commit()

    return jsonify({
        "id": new_id,
        "content": data["content"]
    }), 201


@app.route("/notes/<int:note_id>", methods=["PUT"])
def update_notes(note_id):
    cur = conn.cursor()
    data = request.json

    
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return jsonify({"error": "Token missing"}), 401

    parts = auth_header.split(" ")
    if len(parts) != 2 or parts[0] != "Bearer":
        return jsonify({"error": "Invalid token format"}), 401

    token = parts[1]
    decoded = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
    user_id = int(decoded["user_id"])

    
    if not data or "content" not in data or not data["content"]:
        return jsonify({"error": "content field is required"}), 400

    
    cur.execute(
        "UPDATE notes SET content=%s WHERE id=%s AND user_id=%s RETURNING id",
        (data["content"], note_id, user_id)
    )

    result = cur.fetchone()

    if not result:
        return jsonify({"error": "Note not found or not yours"}), 404

    conn.commit()

    return jsonify({
        "id": note_id,
        "content": data["content"]
    }), 200


@app.route("/notes/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):
    cur = conn.cursor()

    
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return jsonify({"error": "Token missing"}), 401

    parts = auth_header.split(" ")
    if len(parts) != 2 or parts[0] != "Bearer":
        return jsonify({"error": "Invalid token format"}), 401

    token = parts[1]
    decoded = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
    user_id = int(decoded["user_id"])

    
    cur.execute(
        "DELETE FROM notes WHERE id=%s AND user_id=%s RETURNING id",
        (note_id, user_id)
    )

    result = cur.fetchone()

    if not result:
        return jsonify({"error": "Note not found or not yours"}), 404

    conn.commit()

    return jsonify({"message": "Note deleted successfully!"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000, debug=True)



