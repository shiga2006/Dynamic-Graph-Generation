from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import joblib  # For saving and loading the model
import io
import base64
import requests
import json
import os
app = Flask(__name__)

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')  # Connect to MongoDB
db = client['LLM']  # Database name
users_collection = db['user credentials']  # Collection name
GRAPH_DIR = 'static/graphs'

# Ensure the directory exists
if not os.path.exists(GRAPH_DIR):
    os.makedirs(GRAPH_DIR)
# Voiceflow API setup
VOICEFLOW_API_KEY = ""
VERSION_ID = ""
USER_ID = ""

# Load Dataset and Train Model
file_path = "C:/Users/DELL-7420/LLM/LLM/graphdata.csv"
df = pd.read_csv(file_path, encoding='ISO-8859-1')

tfidf_vectorizer = TfidfVectorizer()
X = tfidf_vectorizer.fit_transform(df['Query'])  # Use the 'Query' column for input
y = df['Graph Type']  # Target column

# Split and train the model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier()
model.fit(X_train, y_train)
print("Model Accuracy:", model.score(X_test, y_test))

# Sample data for graph generation
sample_data_dict = {
    "Show me a bar graph for vehicle sales by type": [
        {"Car Type": "Sedan", "Count": 2000},
        {"Car Type": "SUV", "Count": 1500},
        {"Car Type": "Hatchback", "Count": 1800}
    ],
    "Plot a line graph of car sales over the years": [
        {"Year": 2020, "Sales": 5000},
        {"Year": 2021, "Sales": 5500},
        {"Year": 2022, "Sales": 6000},
        {"Year": 2023, "Sales": 6500}
    ],
    "Give me a graph of vehicle sales vs region": [
        {"Region": "North", "Sales": 1500},
        {"Region": "South", "Sales": 1800},
        {"Region": "East", "Sales": 1200},
        {"Region": "West", "Sales": 1600}
    ],
    "Create a pie chart for the distribution of vehicle sales by brand": [
        {"Car Brand": "Toyota", "Sales": 2500},
        {"Car Brand": "Honda", "Sales": 2000},
        {"Car Brand": "Ford", "Sales": 1500},
        {"Car Brand": "BMW", "Sales": 1000}
    ],
    "Generate a bar chart of the sales of vehicles in 2023 by state": [
        {"State": "Maharashtra", "GDP Contribution": 800},
        {"State": "Delhi", "GDP Contribution": 600},
        {"State": "Tamil Nadu", "GDP Contribution": 700},
        {"State": "Karnataka", "GDP Contribution": 500}
    ],
    "Plot a line graph of temperature variations over the past month": [
        {"Day": 1, "Temperature (°C)": 32},
        {"Day": 2, "Temperature (°C)": 34},
        {"Day": 3, "Temperature (°C)": 33},
        {"Day": 4, "Temperature (°C)": 31},
        {"Day": 5, "Temperature (°C)": 30}
    ],
    "Show me a bar chart of rainfall by city for this year": [
        {"City": "Mumbai", "Rainfall (mm)": 200},
        {"City": "Bangalore", "Rainfall (mm)": 150},
        {"City": "Delhi", "Rainfall (mm)": 100},
        {"City": "Chennai", "Rainfall (mm)": 120}
    ],
    "Give me a scatter plot of humidity vs temperature": [
        {"Temperature (°C)": 30, "Humidity (%)": 70},
        {"Temperature (°C)": 32, "Humidity (%)": 75},
        {"Temperature (°C)": 33, "Humidity (%)": 80}
    ],
    "Plot a pie chart of the most used SIM providers by speed": [
       {"Provider": "Airtel", "Market Share (%)": 30},
       {"Provider": "Jio", "Market Share (%)": 35},
       {"Provider": "Vodafone", "Market Share (%)": 25},
       {"Provider": "BSNL", "Market Share (%)": 10}
    ],
    "Plot a line graph showing the average internet speed for each mobile network" : [
       {"Provider": "Airtel", "Speed (Mbps)": 45},
       {"Provider": "Jio", "Speed (Mbps)": 50},
       {"Provider": "Vodafone", "Speed (Mbps)": 40},
       {"Provider": "BSNL", "Speed (Mbps)": 30}
    ],
    "Give me a bar chart for India's GDP by sector in 2023": [
       {"Sector": "Agriculture", "Contribution (%)": 18},
       {"Sector": "Services", "Contribution (%)": 55},
       {"Sector": "Industry", "Contribution (%)": 27}
    ]     
   
    
}

@app.route('/')
def home():
    return render_template('home.html')  # Main page with chatbot and graph generator links

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users_collection.find_one({'username': username, 'password': password})
        if user:
            return redirect(url_for('description'))
        else:
            error = "Invalid username or password."
            return render_template('login.html', error=error)
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if the username already exists
        if users_collection.find_one({'username': username}):
            error = "Username already exists. Please try a different one."
            return render_template('signup.html', error=error)
        else:
            # Insert the new user's credentials into the database
            users_collection.insert_one({'username': username, 'password': password})
            
            # Redirect to the graph maker page after signup
            return redirect(url_for('graph_maker'))
    
    # Render the signup page for GET requests
    return render_template('signup.html')

@app.route('/graph_maker')
def graph_maker():
    return render_template('graph_maker.html')


@app.route('/description')
def description():
    return render_template('description.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/send_mail', methods=['POST'])
def send_mail():
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        # EmailJS API configuration
        emailjs_service_id = ""  # Replace with your EmailJS service ID
        emailjs_template_id = ""  # Replace with your EmailJS template ID
        emailjs_user_id = ""  # Replace with your EmailJS public key

        # Data to send to EmailJS
        payload = {
            "service_id": emailjs_service_id,
            "template_id": emailjs_template_id,
            "user_id": emailjs_user_id,
            "template_params": {
                "from_name": name,
                "from_email": email,
                "message": message
            }
        }

        # Make a POST request to EmailJS API
        response = requests.post(
            "https://api.emailjs.com/api/v1.0/email/send",
            json=payload
        )

        # Check the response status
        if response.status_code == 200:
            return jsonify({'status': 'success', 'message': 'Your message has been sent successfully!'})
        else:
            return jsonify({'status': 'error', 'message': 'Failed to send the message. Please try again.'})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        user_query = data.get('query')

        if not user_query:
            return jsonify({"error": "No query provided"}), 400

        # Vectorize the query and predict
        new_query_vectorized = tfidf_vectorizer.transform([user_query])
        prediction = model.predict(new_query_vectorized)
        predicted_graph_type = prediction[0]

        # Sample data for graphing
        sample_data = sample_data_dict.get(user_query, [])
        graph_path = "static/generated_graph.png"

        if predicted_graph_type == "Bar chart" and sample_data:
            # Generate Bar Chart
            df_sample = pd.DataFrame(sample_data)
            df_sample.plot(kind='bar', x=df_sample.columns[0], y=df_sample.columns[1], legend=False)
            plt.title("Bar Chart")
            plt.savefig(graph_path)
            plt.close()
            return jsonify({"prediction": predicted_graph_type, "graph_path": graph_path})
        elif prediction[0] == "Pie chart" and sample_data:
            df_sample = pd.DataFrame(sample_data)
            graph_path = "static/pie_chart.png"
            df_sample.set_index(df_sample.columns[0], inplace=True)
            df_sample.plot(kind='pie', y=df_sample.columns[0], autopct='%1.1f%%')
            plt.title("Pie Chart")
            plt.savefig(graph_path)
            plt.close()
            return jsonify({"graph_type": prediction[0], "graph_path": graph_path})
        elif predicted_graph_type == "Scatter plot" and sample_data:
            # Generate Scatter Plot
            df_sample = pd.DataFrame(sample_data)
            plt.scatter(df_sample.iloc[:, 0], df_sample.iloc[:, 1], c='blue', marker='o')
            plt.title("Scatter Plot")
            plt.xlabel(df_sample.columns[0])
            plt.ylabel(df_sample.columns[1])
            plt.savefig(graph_path)
            plt.close()
            return jsonify({"prediction": predicted_graph_type, "graph_path": graph_path})

        elif predicted_graph_type == "Line graph" and sample_data:
            # Generate Line Graph
            df_sample = pd.DataFrame(sample_data)
            plt.plot(df_sample.iloc[:, 0], df_sample.iloc[:, 1], marker='o', linestyle='-')
            plt.title("Line Graph")
            plt.xlabel(df_sample.columns[0])
            plt.ylabel(df_sample.columns[1])
            plt.savefig(graph_path)
            plt.close()
            return jsonify({"prediction": predicted_graph_type, "graph_path": graph_path})

        else:
            return jsonify({"error": "Unsupported graph type or no data found."}), 400

    except Exception as e:
        print(f"Error in /predict: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    voiceflow_url = f"https://general-runtime.voiceflow.com/state/{VERSION_ID}/user/{USER_ID}/interact"
    payload = {"request": {"type": "text", "payload": user_message}}
    headers = {"Authorization": VOICEFLOW_API_KEY, "Content-Type": "application/json"}

    try:
        response = requests.post(voiceflow_url, json=payload, headers=headers)
        response_data = response.json()
        if response.status_code == 200 and "responses" in response_data:
            bot_responses = response_data["responses"]
            bot_message = "\n".join([resp.get("text", "") for resp in bot_responses])
            return jsonify({"response": bot_message})
        else:
            return jsonify({"error": "Failed to get response from chatbot"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)





