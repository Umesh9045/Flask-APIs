from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# In-memory user database
users_db = {}

@app.route('/')
def home():
    return "Welcome to the Flask SignUp/SignIn API!"

# Serve Signup page
@app.route('/signup')
def signup_page():
    return render_template('signup.html')

# Serve Signin page
@app.route('/signin')
def signin_page():
    return render_template('signin.html')


# Sign-Up API to register a new user
@app.route('/signup', methods=['POST'])
def signup():
    #DATA INPUT
    data = request.get_json()  # Get JSON data from the request
    username = data.get('username')
    password = data.get('password')
    dob = data.get('dob')
    emailid = data.get('emailid')

    # Validations
    if not username or not password or not dob or not emailid:
        return jsonify({'message': 'All fields are required!'}), 400

    if username in users_db:
        return jsonify({'message': 'User already exists!'}), 400

    # Insert Data
    users_db[username] = {
        "password": password,
        "dob": dob,
        "emailid": emailid
    }

    # Return response
    return jsonify({'message': 'User created successfully!'}), 201


# Sign-In API to authenticate an existing user
@app.route('/signin', methods=['POST'])
def signin():
    #DATA INPUT
    data = request.get_json()  # Get JSON data from the request
    username = data.get('username')
    password = data.get('password')

    # VALIDATION
    if not username or not password:
        return jsonify({'message': 'Username and password are required!'}), 400

    # Read data from db
    user_data = users_db.get(username)

    if not user_data:
        return jsonify({'message': 'User not found!'}), 404

    stored_password = user_data["password"]

    if stored_password != password:
        return jsonify({'message': 'Invalid credentials!'}), 401

    return jsonify({'message': 'Sign-in successful!'}), 200


if __name__ == '__main__':
    app.run(debug=True)
