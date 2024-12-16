from flask import Blueprint, render_template, request, jsonify
import scrap.scraping as scrap
import json, os

# create a Blueprint
bp = Blueprint('main', __name__)

# Path to the JSON file where data will be stored
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, 'data/homework_data.json')

@bp.route('/')
def index():
    return render_template('index.html', title="Home")

@bp.route('/sync', methods=['POST'])
def sync_homeworks():
    """
    Save homework data from client to server (overwrite the file).
    """
    try:
        # Get JSON data from the POST request
        data = request.get_json()

        # Ensure the directory exists
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

        # Save the data to a JSON file
        with open(DATA_FILE, 'w') as file:
            json.dump(data, file, indent=4)

        return jsonify({"status": "success", "message": "Data synced to server successfully."}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@bp.route('/load', methods=['GET'])
def load_homeworks():
    """
    Load homework data from the server to the client.
    """
    try:
        if not os.path.exists(DATA_FILE):
            return jsonify({}), 200  # Return an empty object if no file exists

        with open(DATA_FILE, 'r') as file:
            data = json.load(file)

        return jsonify(data), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@bp.route('/plg')
def plg():
    plg_data = get_plg_data()
    return render_template('plg.html', plg_data=plg_data, title="Planning")

def get_plg_data():
    plg_data = scrap.main()[0]
    for day, day_data in plg_data.items():
        jour= ""
        nom = ""
        h1  = ""
        h2  = ""
        for data in day_data[:-1]:
            jour= day[0:3].lower()
            nom = simplifier_nom(data['nom'])
            hp  = data['heure_plate'].split(' - ')
            h1  = hp[0]
            h2  = hp[1]

            data['infos_supp'] = {'abrvt_jour': jour, 'abrvt_nom': nom, 'heure_debut': h1, 'heure_fin': h2}
    return plg_data


def simplifier_nom(nom):
    nom = nom.lower().replace(" ", "_").replace(".", "")
    mots_clefs = {
        "web":      "web",
        "math":     "math",
        "dev":      "dev",
        "archi":    "archi",
        "systemes": "systemes",
        "economie": "eco",
        "gestion":  "gestion",
        "bd":       "bd",
        "ppp":      "ppp",
        "sae":      "sae",
        "comm":     "comm",
        "anglais":  "anglais",
        "tutorat":  "tutorat",
        "soutien":  "soutien"
    }

    for cle, raccourci in mots_clefs.items():
        if cle in nom:
            return raccourci
    return "default"

# add more routes for homework, test, note, ....
