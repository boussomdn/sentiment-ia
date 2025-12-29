from flask import Flask, render_template, request, jsonify 
from transformers import pipeline 
app = Flask(__name__) 
# Charger le modèle de sentiment 
print("Chargement du modèle...") 
sentiment_analyzer = pipeline( 
"sentiment-analysis", 
model="nlptown/bert-base-multilingual-uncased-sentiment" 
) 
print("Modèle prêt !") 
@app.route('/') 
def index(): 
    return render_template('sentiment.html') 
@app.route('/analyze', methods=['POST']) 
def analyze(): 
    data = request.get_json() 
    text = data.get('text', '') if data else '' 
 
    if not text.strip(): 
        return jsonify({"error": "Texte vide"}), 400 
 
    try: 
        result = sentiment_analyzer(text[:512])[0] 
 
        stars = int(result['label'].split()[0]) 
 
        sentiment_map = { 
            1: {"text": "Très négatif", "emoji": "😡", "color": "#d32f2f"}, 
            2: {"text": "Négatif", "emoji": "😕", "color": "#f57c00"}, 
            3: {"text": "Neutre", "emoji": "😐", "color": "#fbc02d"}, 
            4: {"text": "Positif", "emoji": "😊", "color": "#7cb342"}, 
            5: {"text": "Très positif", "emoji": "😍", "color": "#388e3c"} 
        } 
 
        sentiment_info = sentiment_map.get(stars, sentiment_map[3]) 
 
        return jsonify({ 
            "stars": stars, 
            "confidence": round(result['score'] * 100, 2), 
            "sentiment": sentiment_info["text"], 
            "emoji": sentiment_info["emoji"], 
            "color": sentiment_info["color"] 
        }) 
 
    except Exception as e: 
        return jsonify({"error": str(e)}), 500 
 
if __name__ == '__main__': 
    app.run(host='0.0.0.0', port=5000, debug=True) 