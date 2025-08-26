from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Ollama API configuration
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:1b"

def analyze_with_ollama(review_text):
    """
    Send the review to Ollama for emotion analysis
    """
    prompt = f"""
    Analyze the following movie review and determine the emotional sentiment.
    Focus on identifying emotions like joy, sadness, anger, surprise, fear, etc.
    Provide a JSON response with:
    - overall_sentiment (positive, negative, neutral, mixed)
    - primary_emotion (the strongest emotion detected)
    - emotion_intensity (low, medium, high)
    - key_emotions (array of detected emotions)
    - brief_explanation (short explanation of the analysis)

    Review: {review_text}
    """
    
    try:
        payload = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }
        
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        
        # Extract the response from Ollama
        result = response.json()
        analysis_text = result.get('response', '')
        
        # In a real implementation, you would parse the AI response
        # For this example, we'll return a simulated response
        return {
            "overall_sentiment": "positive",
            "primary_emotion": "joy",
            "emotion_intensity": "high",
            "key_emotions": ["joy", "excitement", "satisfaction"],
            "brief_explanation": "The review expresses strong positive emotions with words like 'masterpiece' and 'superb' indicating high satisfaction."
        }
        
    except requests.exceptions.RequestException as e:
        print(f"Error calling Ollama API: {e}")
        return None

@app.route('/analyze', methods=['POST'])
def analyze_review():
    """
    Endpoint to analyze movie reviews
    """
    data = request.get_json()
    
    if not data or 'review' not in data:
        return jsonify({"error": "No review provided"}), 400
    
    review_text = data['review']
    
    # Call Ollama for analysis
    analysis_result = analyze_with_ollama(review_text)
    
    if analysis_result:
        return jsonify(analysis_result)
    else:
        return jsonify({"error": "Analysis failed"}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    """
    return jsonify({"status": "OK", "model": MODEL_NAME})

if __name__ == '__main__':
    app.run(debug=True, port=5000)