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

app = Flask(__name__)

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')  # Connect to MongoDB
db = client['LLM']  # Database name
users_collection = db['user credentials']  # Collection name

# Voiceflow API setup
VOICEFLOW_API_KEY = "VF.DM.67489a6eb2be2df9d1167f85.zfH7geHXdzgQQ7HV"
VERSION_ID = "674892085b353a1561fe4b0f"
USER_ID = "674892085b353a1561fe4b0e"

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
    "Show me a graph for vehicle sales by type": [
        {"Car Type": "Sedan", "Count": 2000},
        {"Car Type": "SUV", "Count": 1500},
        {"Car Type": "Hatchback", "Count": 1800}
    ],
    "Show me a bar chart of rainfall by city for this year": [
        {"City": "Mumbai", "Rainfall (mm)": 200},
        {"City": "Bangalore", "Rainfall (mm)": 150},
        {"City": "Delhi", "Rainfall (mm)": 100},
        {"City": "Chennai", "Rainfall (mm)": 120}
    ],
    "Plot graph of car sales over the years": [
        {"State": "Maharashtra", "GDP Contribution": 800},
        {"State": "Delhi", "GDP Contribution": 600},
        {"State": "Tamil Nadu", "GDP Contribution": 700},
        {"State": "Karnataka", "GDP Contribution": 500}
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
        if users_collection.find_one({'username': username}):
            error = "Username already exists. Please try a different one."
            return render_template('signup.html', error=error)
        else:
            users_collection.insert_one({'username': username, 'password': password})
            return redirect(url_for('home'))
    return render_template('signup.html')

@app.route('/description')
def description():
    return render_template('description.html')

@app.route('/predict_graph', methods=['POST'])
def predict_graph():
    try:
        # Step 1: Get the query from the user input
        new_query = request.form.get('query')

        # Log the received query
        print(f"Received query: {new_query}")

        if not new_query:
            return jsonify({"error": "Query is empty"}), 400
        result = classifier(new_query, candidate_labels=graph_types)
        predicted_graph_type = result['labels'][0]
        print(f"Predicted graph type: {predicted_graph_type}")
        sample_data = sample_data_dict.get(new_query, None)
        if sample_data is None:
            print(f"No sample data found for query: {new_query}")
            return jsonify({"error": "No data found for the query."}), 400
        graph_path = "static/generated_graph.png"
        print(f"Graph path: {graph_path}")
        if predicted_graph_type == "Bar chart" and sample_data:
            # Generate Bar Chart
            df_sample = pd.DataFrame(sample_data)
            df_sample.plot(kind='bar', x=df_sample.columns[0], y=df_sample.columns[1], legend=False)
            plt.title("Bar Chart")
            plt.savefig(graph_path)
            plt.close()
            return jsonify({"prediction": predicted_graph_type, "graph_path": graph_path})

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
            print(f"Unsupported graph type or no data found for query: {new_query}")
            return jsonify({"error": "Unsupported graph type or no data found."}), 400

    except Exception as e:
        print(f"Error in /predict_graph: {e}")
        return jsonify({"error": f"Internal server error: {e}"}), 500


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





