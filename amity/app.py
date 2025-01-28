# from flask import Flask, render_template, request, redirect, url_for, session
# app = Flask(__name__)
# app.secret_key = 'your_secret_key'  # Required for session handling

# # Dummy user data storage
# users = {}

# @app.route('/')
# def home():
#     # Check if a user is logged in
#     if 'email' in session:
#         email = session['email']
#         user = users.get(email)
#         return render_template('home.html', user=user)
#     else:
#         return redirect(url_for('login'))


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']
#         if email in users and users[email]['password'] == password:
#             session['email'] = email  # Store email in session
#             return redirect(url_for('home'))
#         else:
#             return "Invalid credentials, please try again."



#     return render_template('login.html')

# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if request.method == 'POST':
#         name = request.form['name']
#         location = request.form['location']
#         email = request.form['email']
#         password = request.form['password']
#         # Storing user data
#         users[email] = {'name': name, 'location': location, 'password': password}
#         return redirect(url_for('login'))

#     return render_template('signup.html')

# @app.route('/logout')
# def logout():
#     session.pop('email', None)  # Remove email from session
#     return redirect(url_for('login'))

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, render_template, request, redirect, url_for, session
from flask import Flask, jsonify, request

from pymongo import MongoClient
import math

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB connection string
db = client['myDatabase']  # Replace with your database name
users_collection = db['users']  # Replace with your collection name

@app.route('/')
def home():
    if 'email' in session:
        user = users_collection.find_one({'email': session['email']})
        if user:
            return render_template('home.html', user=user)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = users_collection.find_one({'email': email, 'password': password})
        if user:
            session['email'] = email
            return redirect(url_for('home'))
        return 'Invalid credentials', 401
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        password = request.form['password']
        location = request.form['location']
        if users_collection.find_one({'email': email}):
            return 'Email already registered', 400
        users_collection.insert_one({'email': email, 'name': name, 'password': password, 'location': location})
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('login'))



# @app.route('/rewards', methods=['GET', 'POST'])
# def rewards():
#     if request.method == 'POST':
#         bio_waste = float(request.form['bio_waste'])
#         nonbio_waste = float(request.form['nonbio_waste'])

#         # Save waste data to session
#         session['bio_waste'] = bio_waste
#         session['nonbio_waste'] = nonbio_waste

#         # Reward logic
#         if bio_waste > nonbio_waste:
#             reward_message = f"Great job! You earned {int(bio_waste * 10)} stars for managing {bio_waste} kg of biodegradable waste!"
#         else:
#             reward_message = "Try to generate more biodegradable waste to earn rewards!"

#         return render_template('rewards.html', reward_message=reward_message)
#     return render_template('rewards.html')



# @app.route('/tips', methods=['GET'])
# def tips():
#     # Retrieve waste data from session
#     bio_waste = session.get('bio_waste', 0)
#     nonbio_waste = session.get('nonbio_waste', 0)

#     # Tips logic
#     if bio_waste > nonbio_waste:
#         tips = [
#             "Compost biodegradable waste to create natural fertilizer.",
#             "Use biodegradable waste to produce biogas.",
#             "Avoid mixing biodegradable waste with plastics."
             
#         ]
#     else:
#         tips = [
#             "Reduce non-biodegradable waste by reusing items.",
#             "Recycle plastics and e-waste at nearby centers.",
#             "Switch to biodegradable alternatives for daily use."
#         ]

#     return render_template('tips.html', tips=tips)





# @app.route('/rewards', methods=['GET', 'POST'])
# def rewards():
#     if request.method == 'POST':
#         bio_waste = int(request.form['bio_waste'])
#         non_bio_waste = int(request.form['non_bio_waste'])

#         if 'email' in session:
#             user_email = session['email']
#             users_collection.update_one(
#                 {'email': user_email},
#                 {'$set': {'bio_waste': bio_waste, 'non_bio_waste': non_bio_waste}}
#             )


#         # Redirect to the rewards page with updated data
#         return redirect(url_for('rewards'))

#     if 'email' in session:
#         user = users_collection.find_one({'email': session['email']})
#         return render_template('rewards.html', user=user)
#     return redirect(url_for('login'))


@app.route('/rewards', methods=['GET', 'POST'])
def rewards():
    if request.method == 'POST':
        bio_waste = int(request.form['bio_waste'])
        non_bio_waste = int(request.form['non_bio_waste'])

        # Check if the user is logged in
        if 'email' in session:
            user_email = session['email']

            # Save bio_waste and non_bio_waste in the user's record
            users_collection.update_one(
                {'email': user_email},
                {'$set': {'bio_waste': bio_waste, 'non_bio_waste': non_bio_waste}}
            )

        # Redirect to reload rewards page with updated data
        return redirect(url_for('rewards'))

    if 'email' in session:
        user = users_collection.find_one({'email': session['email']})

        # Fetch bio_waste and non_bio_waste from user's data
        bio_waste = user.get('bio_waste', 0)
        non_bio_waste = user.get('non_bio_waste', 0)

        # Rewards logic
        if bio_waste > non_bio_waste:
            reward_message = f"Great job! You earned {int(bio_waste * 10)} stars for managing {bio_waste} kg of biodegradable waste!"
        else:
            reward_message = f"You generated more non-biodegradable waste ({non_bio_waste} kg). Try to reduce it to earn more stars!"

        return render_template('rewards.html', reward_message=reward_message, bio_waste=bio_waste, non_bio_waste=non_bio_waste)

    return redirect(url_for('login'))


@app.route('/tips')
def tips():
    if 'email' in session:
        user = users_collection.find_one({'email': session['email']})
        if user:
            bio_waste = user.get('bio_waste', 0)
            non_bio_waste = user.get('non_bio_waste', 0)

            # Determine which waste is higher
            if bio_waste > non_bio_waste:
                message = f"Since your biodegradable waste ({bio_waste} kg) is more, here are some tips to manage it efficiently."
                tips = [
                    "Compost biodegradable waste to create organic fertilizer.",
                    "Use food scraps for vermiculture or biogas production.",
                    "Avoid throwing biodegradable waste in non-biodegradable bins."
                ]
            else:
                message = f"Since your non-biodegradable waste ({non_bio_waste} kg) is more, here are some tips to manage it efficiently."
                tips = [
                    "Recycle plastic, glass, and paper waste whenever possible.",
                    "Segregate electronic waste and take it to e-waste collection centers.",
                    "Avoid using single-use plastics; switch to reusable alternatives."
                ]

            return render_template('tips.html', message=message, tips=tips)
    return redirect(url_for('login'))



centers = [
    {
        "name": "Green Earth Recycling Center",
        "address": "123 Green St, Springfield",
        "latitude": 37.7749,
        "longitude": -122.4194,
        "opening_hours": "9:00 AM - 5:00 PM",
        "waste_types": ["Plastic", "Glass", "Metal"]
    },
    {
        "name": "Eco Waste Management",
        "address": "456 Eco Rd, Springfield",
        "latitude": 37.8049,
        "longitude": -122.4294,
        "opening_hours": "8:00 AM - 6:00 PM",
        "waste_types": ["Organic", "Paper", "E-waste"]
    },
    {
        "name": "Urban Waste Solutions",
        "address": "789 Urban Ave, Springfield",
        "latitude": 37.7849,
        "longitude": -122.4094,
        "opening_hours": "7:00 AM - 7:00 PM",
        "waste_types": ["Plastic", "Metal", "E-waste"]
    }
]

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in kilometers
    d_lat =math. radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = math.sin(d_lat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(d_lon / 2) ** 2
    c = 2 *math. atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

@app.route('/centers', methods=['POST'])
def centers_view():
    # Get latitude and longitude from the request
    data = request.get_json()
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    if latitude and longitude:
        # Example: Fetch nearby centers based on lat/lon
        nearby_centers = [
            {
                "name": "Green Earth Center",
                "type": "Biodegradable",
                "location": "Downtown, City",
                "contact": "123-456-7890",
            },
            {
                "name": "Recycle Hub",
                "type": "Non-biodegradable",
                "location": "Uptown, City",
                "contact": "987-654-3210",
            },
        ]
        return jsonify(nearby_centers)

    return jsonify({"error": "Location data is missing!"}), 400@app.route('/centers', methods=['POST'])
def centers_view():
    # Get latitude and longitude from the request
    data = request.get_json()
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    if latitude and longitude:
        # Example: Fetch nearby centers based on lat/lon
        nearby_centers = [
            {
                "name": "Green Earth Center",
                "type": "Biodegradable",
                "location": "Downtown, City",
                "contact": "123-456-7890",
            },
            {
                "name": "Recycle Hub",
                "type": "Non-biodegradable",
                "location": "Uptown, City",
                "contact": "987-654-3210",
            },
        ]
        return jsonify(nearby_centers)

    return jsonify({"error": "Location data is missing!"}), 400



if __name__ == '__main__':
    app.run(debug=True)
