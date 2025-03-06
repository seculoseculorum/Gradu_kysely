from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from init_db import init_db
import sqlite3
import uuid

app = Flask(__name__)
app.secret_key = "some-secret-string"  # Required to use sessions

@app.route('/')
def home():
    # Redirect users to the consent form as soon as they hit the root URL
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
        # Check if the user ticked the checkbox named 'consent_check'
        if request.form.get('consent_check') == 'on':
            # Generate or retrieve a user_id, store in session
            user_id = str(uuid.uuid4())
            session['user_id'] = user_id
            
            # (Optional) Store consent in database
            conn = sqlite3.connect('kysely.db')
            c = conn.cursor()
            c.execute('''
                INSERT INTO consent_responses (user_id, consent)
                VALUES (?, ?)
            ''', (user_id, 1))  # 1 for True
            conn.commit()
            conn.close()

            # Proceed to background questionnaire
            return redirect(url_for('background'))
        else:
            # If not ticked, re-render the page with an error
            error = "You must agree to the consent form before continuing."
            return render_template('consent.html', error=error)
    else:
        return render_template('consent.html')

@app.route('/background', methods=['GET', 'POST'])
def background():
    """
    Displays the background questionnaire form (GET)
    and processes the submitted data (POST).
    After this, it redirects to the main survey page.
    """
    if request.method == 'POST':
        # Retrieve user_id from session (assuming it was stored after consent)
        user_id = session.get('user_id', None)

        # If for some reason there's no user_id, you might handle that
        if not user_id:
            # Redirect or handle error
            return redirect(url_for('consent'))

        # Get form data, convert to the appropriate types
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

        # Insert background data into the database
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

        # After background is submitted, go to the survey
        return redirect(url_for('survey'))
    else:
        # GET request: show the background form
        return render_template('background.html')

@app.route('/survey')
def survey():
    import os, random
    
    # Gather .svg images from static/images
    images_path = os.path.join(app.static_folder, 'images')
    file_list = [f for f in os.listdir(images_path) if f.lower().endswith('.svg')]

    # Shuffle them
    random.shuffle(file_list)

    # Optionally generate a unique user_id if not in session
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())

    return render_template(
        'index.html',
        candlestick_images=file_list,
        user_id=session['user_id']
    )
@app.route('/submit', methods=['POST'])
def submit():
    """
    Expects JSON like:
    {
      "user_id": "...",
      "image": "candlestick1.svg",
      "expectedValue": 103.45,
      "confidence": "4",
      "analysisSupport": "Yes",
      "visualClarity": "5"
    }
    """
    data = request.json

    user_id = data.get('user_id')
    image_name = data.get('image')
    expected_value = data.get('expectedValue')
    confidence = data.get('confidence')
    analysis_support = data.get('analysisSupport')
    visual_clarity = data.get('visualClarity')

    # Insert into DB
    conn = sqlite3.connect('kysely.db')
    c = conn.cursor()
    c.execute("""
        INSERT INTO responses
        (user_id, image_name, expected_value, confidence, analysis_support, visual_clarity)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        image_name,
        expected_value,
        confidence,
        analysis_support,
        visual_clarity
    ))
    conn.commit()
    conn.close()

    return jsonify({"status": "ok", "message": "Response saved."})



if __name__ == '__main__':
    init_db()
    app.run(debug=True)
