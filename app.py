from flask import Flask, render_template, request, jsonify
import os
import random
import sqlite3
import uuid

app = Flask(__name__)

@app.route('/')
def index():
    """
    1. Generate a random "user_id" for the new user session if needed.
       In reality, you'd likely set this in a session or user login. 
       For demonstration, let's generate a UUID and pass it to the template.
    """
    user_id = str(uuid.uuid4())

    # 2. List all .svg files in static/images
    images_path = os.path.join(app.static_folder, 'images')
    file_list = [f for f in os.listdir(images_path) if f.lower().endswith('.svg')]

    # 3. Shuffle them
    random.shuffle(file_list)

    # 4. Render the template, passing the user_id and the list of images
    return render_template('index.html', candlestick_images=file_list, user_id=user_id)

@app.route('/submit', methods=['POST'])
def submit():
    """
    Receives user responses from the front end in JSON form:
    {
        "user_id": "some-random-uuid",
        "image": "candlestick1.svg",
        "expectedValue": 103.45
    }
    Stores them in the SQLite DB.
    """
    data = request.json
    user_id = data.get('user_id')
    image_name = data.get('image')
    expected_value = data.get('expectedValue')

    # Insert into the DB
    conn = sqlite3.connect('kysely.db')
    c = conn.cursor()
    c.execute("""
        INSERT INTO responses (user_id, image_name, expected_value)
        VALUES (?, ?, ?)
    """, (user_id, image_name, expected_value))
    conn.commit()
    conn.close()

    # Respond with a success message (JSON)
    return jsonify({"status": "ok", "message": "Response saved."})

if __name__ == '__main__':
    # Make sure the DB is created before we run
    # (Or manually run init_db.py once)
    app.run(debug=True)
