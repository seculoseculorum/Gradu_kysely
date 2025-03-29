from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from init_db import init_db
import sqlite3
import uuid
import os, random

app = Flask(__name__)
app.secret_key = "some-secret-string"  # Required to use sessions

@app.route('/')
def home():
    # Redirect users to the consent form as soon as they hit the root URL.
    return redirect(url_for('welcome'))

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/consent', methods=['GET', 'POST'])
def consent():
    """
    Displays a consent form. If the user agrees (checkbox ticked),
    they can proceed to the background questionnaire.
    Otherwise, stay on the page with an error.
    """
    if request.method == 'POST':
        if request.form.get('consent_check') == 'on':
            # Generate a new user_id and store in session.
            user_id = str(uuid.uuid4())
            session['user_id'] = user_id
            
            # (Optional) Store consent in the database.
            conn = sqlite3.connect('kysely.db')
            c = conn.cursor()
            c.execute('''
                INSERT INTO consent_responses (user_id, consent)
                VALUES (?, ?)
            ''', (user_id, 1))  # 1 for True
            conn.commit()
            conn.close()

            # Proceed to background questionnaire.
            return redirect(url_for('background'))
        else:
            error = "You must agree to the consent form before continuing."
            return render_template('consent.html', error=error)
    else:
        return render_template('consent.html')

@app.route('/background', methods=['GET', 'POST'])
def background():
    """
    Displays the background questionnaire form (GET)
    and processes the submitted data (POST).
    After submission, the user is redirected to the Task 1 instruction page.
    """
    if request.method == 'POST':
        user_id = session.get('user_id', None)
        if not user_id:
            return redirect(url_for('consent'))

        # Retrieve form data.
        age = int(request.form.get('age', '0'))
        gender = request.form.get('gender', '')
        education = request.form.get('education', '')
        investment_experience = int(request.form.get('investment_experience', '0'))
        fin_mark_engagement = request.form.get('fin_mark_engagement', '')
        ai_engagement = request.form.get('ai_engagement', '')
        risk_tolerance = int(request.form.get('risk_tolerance', '0'))
        familiarity_ai = int(request.form.get('familiarity_ai', '0'))
        knowledge_gen_ai = int(request.form.get('knowledge_gen_ai', '0'))
        ai_trust = int(request.form.get('ai_trust', '0'))
        decision_confidence = int(request.form.get('decision_confidence', '0'))

        # Insert background data into the database.
        conn = sqlite3.connect('kysely.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO background_responses
            (
                user_id,
                Age,
                Gender,
                Education,
                InvestmentExperience,
                FinMarkEngagement,
                AiEngagement,
                RiskTolerance,
                FamiliarityAI,
                KnowledgeGenAI,
                AITrust,
                DecisionConfidence
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_id,
            age,
            gender,
            education,
            investment_experience,
            fin_mark_engagement,
            ai_engagement,
            risk_tolerance,
            familiarity_ai,
            knowledge_gen_ai,
            ai_trust,
            decision_confidence
        ))
        conn.commit()
        conn.close()

        # After background is submitted, redirect to the Task 1 instruction page.
        return redirect(url_for('task1info'))
    else:
        return render_template('background.html')

@app.route('/task1info')
def task1info():
    """
    Renders the Task 1 instructions page.
    """
    return render_template('Task1Info.html', user_id=session.get('user_id'))

@app.route('/survey')
def survey():
    """
    Renders the Task 1 questionnaire.
    Uses images from the 'images' folder.
    """
    images_path = os.path.join(app.static_folder, 'images')
    file_list = [f for f in os.listdir(images_path) if f.lower().endswith('.svg')]
    random.shuffle(file_list)

    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())

    return render_template(
        'Task1.html',  # Task1 questionnaire template.
        candlestick_images=file_list,
        user_id=session['user_id']
    )

@app.route('/submit', methods=['POST'])
def submit():
    """
    Handles submission for Task 1.
    Expects JSON in the format:
    {
      "user_id": "...",
      "image": "candlestick1.svg",
      "expectedValue": 103.45
    }
    Inserts the response into the task1responses table.
    """
    data = request.json
    user_id = data.get('user_id')
    image_name = data.get('image')
    user_value = data.get('expectedValue')
    
    conn = sqlite3.connect('kysely.db')
    c = conn.cursor()
    c.execute("""
    INSERT INTO task1responses (user_id, image_name, user_estimate)
    VALUES (?, ?, ?)
    """, (user_id, image_name, user_value))
    conn.commit()
    conn.close()

    return jsonify({"status": "ok", "message": "Response saved."})

@app.route('/task2info')
def task2info():
    """
    Renders the Task 2 instructions page.
    """
    return render_template('Task2Info.html', user_id=session.get('user_id'))

@app.route('/task2')
def task2():
    """
    Renders the Task 2 questionnaire.
    Uses images from the 'Clean_Images' folder.
    """
    images_path = os.path.join(app.static_folder, 'Clean_Images')
    file_list = [f for f in os.listdir(images_path) if f.lower().endswith('.svg')]
    random.shuffle(file_list)

    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())

    return render_template(
        'Task2.html',
        candlestick_images=file_list,
        user_id=session['user_id']
    )

@app.route('/submitTask2', methods=['POST'])
def submitTask2():
    """
    Handles submission for Task 2.
    Expects JSON in the format:
    {
      "user_id": "...",
      "image": "candlestick1.svg",
      "expectedValue": 103.45
    }
    Inserts the response into the task2responses table.
    """
    data = request.json
    user_id = data.get('user_id')
    image_name = data.get('image')
    user_value = data.get('expectedValue')
    
    conn = sqlite3.connect('kysely.db')
    c = conn.cursor()
    c.execute("""
        INSERT INTO task2responses (user_id, image_name, user_estimate)
        VALUES (?, ?, ?)
    """, (user_id, image_name, user_value))
    conn.commit()
    conn.close()

    return jsonify({"status": "ok", "message": "Task2 response saved."})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
