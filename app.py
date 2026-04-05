from flask import Flask, request, jsonify, render_template, redirect, url_for
import pandas as pd
import requests

app = Flask(__name__)

# Load datasets
df = pd.read_csv("dataset.csv")
precautions_df = pd.read_csv("symptom_precaution.csv")

GOOGLE_MAPS_API_KEY = "YOUR_GOOGLE_MAPS_API_KEY_HERE"

# ---------------- ROUTES ---------------- #

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect(url_for('patient'))
    return render_template("login.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        return redirect(url_for('patient'))
    return render_template("signup.html")

@app.route('/patient')
def patient():
    return render_template("patient.html")

@app.route('/predict_page')
def predict_page():
    return render_template("index.html")

@app.route('/location')
def location():
    return render_template("location.html")

# ---------------- PREDICT API ---------------- #

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    user_input = data["symptoms"]

    user_symptoms = [s.strip().lower().replace(" ", "_") for s in user_input.split(",")]

    best_match = None
    max_count = 0

    for index, row in df.iterrows():
        disease = row["Disease"]
        symptoms = [str(s).strip().lower().replace(" ", "_")
                    for s in row[1:] if str(s) != 'nan']

        match_count = len(set(user_symptoms) & set(symptoms))

        if match_count > max_count:
            max_count = match_count
            best_match = disease

    if best_match is None:
        best_match = "No matching disease found"

    precautions = []
    if best_match != "No matching disease found":
        row = precautions_df[precautions_df["Disease"] == best_match]
        if not row.empty:
            precautions = row.iloc[0, 1:].dropna().tolist()

    return jsonify({
        "disease": best_match,
        "precautions": precautions
    })

# ---------------- RUN ---------------- #

if __name__ == "__main__":
    app.run(debug=True)