from flask import Flask, request, jsonify

app = Flask(__name__)

# in-memory storage for registration data
registered_users = []

@app.route('/register', methods=['POST'])
def register():
    data = request.json

    #extract from data
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    username = data.get('username')
    email = data.get('email')
    repeat_email = data.get('repeat_email')
    password = data.get('password')
    repeat_password = data.get('repeat_password')

    # validate form input
    if not all([first_name, last_name, username, email, repeat_email, password, repeat_password]):
        return jsonify({'error': 'All fields are required'}), 400
    if email != repeat_email:
        return jsonify({'error': 'Emails do not match'}), 400
    if password != repeat_password:
        return jsonify({'error': 'Passwords do not match'}), 400
    
    # check if user already exists
    for user in registered_users:
        if user['username'] == username:
            return jsonify({'error': 'Username already exists'}), 400
        if user['email'] == email:
            return jsonify({'error': 'Email already exists'}), 400
        
        # add new user
        new_user = {
            'first_name': first_name,
            'last_name': last_name,
            'username': username,
            'email': email,
            'password': password
        }
        registered_users.append(new_user)
        return jsonify({'message': 'Registration successful'}), 201
    
    @app.route('/users', methods=['GET'])
    def get_users():
        return jsonify(registered_users)
    
    @app.route('/login', methods=['POST'])
def login():
    data = request.json
    
    username = data.get('username')
    password = data.get('password')
    
    # Validate form inputs
    if not all([username, password]):
        return jsonify({"error": "Username and password are required"}), 400
    
    # Check credentials
    for user in registered_users:
        if user['username'] == username and user['password'] == password:
            return jsonify({"message": "Login successful"}), 200
    
    return jsonify({"error": "Invalid username or password"}), 401

if __name__ == '__main__':
        app.run(debug=True)
