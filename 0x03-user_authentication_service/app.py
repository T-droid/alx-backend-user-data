#!/usr/bin/env python3
"""a simple flask app"""
from flask import Flask, jsonify, request, abort, make_response, redirect
from auth import Auth

AUTH = Auth()
app = Flask(__name__)

@app.route("/")
def home():
    """home route"""
    return jsonify({"message": "Bienvenue"})

@app.route("/users", methods=['POST'])
def users():
    """gets user credentials"""
    email = request.form["email"]
    password = request.form["password"]
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    
@app.route("/sessions", methods=['POST'])
def session():
    """create new session for user"""
    email = request.form["email"]
    password = request.form["password"]
    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    response = make_response(jsonify({"email": email, "message": "logged in"}))
    response.set_cookie('session_id', session_id)
    return response

@app.route('/sessions', methods=['DELETE'])
def logout():
    """logs out a user"""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect('/')
    abort(403)

@app.route("/profile", methods=['GET'])
def profile() -> str:
    """responds with user profile"""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email})
    abort(403)

    


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000", debug=True)
