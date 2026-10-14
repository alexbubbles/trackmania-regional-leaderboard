from flask import Flask, render_template, request, jsonify
import requests
import time

app = Flask(__name__)

# Dizionario completo con tutti i paesi europei e i principali mondiali
FLAGS = {
    "Italy": "🇮🇹", "France": "🇫🇷", "Germany": "🇩🇪", "Spain": "🇪🇸",
    "United Kingdom": "🇬🇧", "England": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "Scotland": "🏴󠁧󠁢󠁳󠁣󠁴󠁿", "Wales": "🏴󠁧󠁢󠁷󠁬󠁳󠁿",
    "Ireland": "🇮🇪", "Portugal": "🇵🇹", "Andorra": "🇦🇩", "San Marino": "🇸🇲", 
    "Vatican City": "🇻🇦", "Monaco": "🇲🇨", "Malta": "🇲🇹", "Greece": "🇬🇷",
    "Cyprus": "🇨🇾", "Switzerland": "🇨🇭", "Austria": "🇦🇹", "Liechtenstein": "🇱🇮", 
    "Netherlands": "🇳🇱", "Belgium": "🇧🇪", "Luxembourg": "🇱🇺",
    "Poland": "🇵🇱", "Czechia": "🇨🇿", "Slovakia": "🇸🇰", "Hungary": "🇭🇺",
    "Sweden": "🇸🇪", "Norway": "🇳🇴", "Finland": "🇫🇮", "Denmark": "🇩🇰", 
    "Iceland": "🇮🇸", "Estonia": "🇪🇪", "Latvia": "🇱🇻", "Lithuania": "🇱🇹",
    "Russia": "🇷🇺", "Ukraine": "🇺🇦", "Belarus": "🇧🇾", "Moldova": "🇲🇩",
    "Romania": "🇷🇴", "Bulgaria": "🇧🇬", "Croatia": "🇭🇷", "Serbia": "🇷🇸",
    "Slovenia": "🇸🇮", "Bosnia and Herzegovina": "🇧🇦", "Montenegro": "🇲🇪",
    "North Macedonia": "🇲🇰", "Albania": "🇦🇱", "Kosovo": "🇽🇰", 
    "Turkey": "🇹🇷", "Georgia": "🇬🇪", "Armenia": "🇦🇲", "Azerbaijan": "🇦🇿",
    "United States": "🇺🇸", "Canada": "🇨🇦", "Brazil": "🇧🇷", "Argentina": "🇦🇷", 
    "Mexico": "🇲🇽", "Chile": "🇨🇱", "Colombia": "🇨🇴", "Uruguay": "🇺🇾",
    "Australia": "🇦🇺", "New Zealand": "🇳🇿", "Japan": "🇯🇵", "South Korea": "🇰🇷",
    "China": "🇨🇳", "India": "🇮🇳", "South Africa": "🇿🇦", "Egypt": "🇪🇬", "Morocco": "🇲🇦"
}

def get_country_from_zone(zone_info):
    """Estrae la nazione dalla struttura a matrioska delle zone di Trackmania"""
    names = []
    current = zone_info
    
    while current and isinstance(current, dict):
        if 'name' in current:
            names.append(current['name'])
        current = current.get('parent')
        
    continenti = ["World", "Europe", "Asia", "North America", "South America", "Africa", "Oceania"]
    for name in reversed(names):
        if name not in continenti:
            return name
    return "Unknown"

def get_regional_campaign_leaderboard(campaign_uid, target_region, pages_to_scan):
    base_url = f"https://trackmania.io/api/leaderboard/{campaign_uid}"
    headers = {"User-Agent": "TM_Seasonal_Tracker_Web"}
    
    regional_players = []
    offset = 0
    length = 100 
    
    for page in range(pages_to_scan):
        url = f"{base_url}?offset={offset}&length={length}"
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            tops = data.get('tops', [])
            if not tops:
                break
                
            for record in tops:
                player = record.get('player', {})
                zone_info = player.get('zone', {})
                
                if target_region.lower() in str(zone_info).lower():
                    points = record.get('points', record.get('score', 0))
                    
                    country_name = get_country_from_zone(zone_info)
                    flag_emoji = FLAGS.get(country_name, "🌍") 
                    
                    regional_players.append({
                        "global_position": record.get('position', 0),
                        "name": player.get('name', 'Unknown'),
                        "points": points,
                        "country": country_name,
                        "flag": flag_emoji
                    })
            
            offset += length
            if page < pages_to_scan - 1:
                time.sleep(1.5)
                
        except Exception as e:
            print(f"Errore API: {e}")
            break

    return regional_players

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/search', methods=['POST'])
def search_leaderboard():
    dati_ricevuti = request.json
    uid = dati_ricevuti.get('uid')
    region = dati_ricevuti.get('region', 'World')
    
    # SICUREZZA: Previene valori malevoli per evitare blocchi del server
    try:
        pages = int(dati_ricevuti.get('pages', 1))
        pages = max(1, min(pages, 100)) # Forza tra 1 e 100
    except (ValueError, TypeError):
        pages = 1
    
    risultati = get_regional_campaign_leaderboard(uid, region, pages)
    risultati.sort(key=lambda x: x['points'], reverse=True)
    return jsonify(risultati)

if __name__ == '__main__':
    # Debug disattivato per sicurezza in vista della pubblicazione
    app.run(debug=False)