from flask import Blueprint, render_template, request, jsonify
import scrap.scraping as scrap
from scrap.scraping import getDay
import json, os

# create a Blueprint
bp = Blueprint('main', __name__)

semester    = "SM1"
group       = "S1"
group_week  = "A"

# Path to the JSON file where data will be stored
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HOMEWORK_FILE = os.path.join(BASE_DIR, f'data/homework_data_{semester}_{group}_{group_week}.json')
PLANNING_FILE = os.path.join(BASE_DIR, f'data/planning_data_SM1_S1_A.json')


def load_plg_data(PLG_DATA_FILE):
    if os.path.exists(PLG_DATA_FILE):
        with open(PLG_DATA_FILE, "r") as f:
            return json.load(f)
    return [{}, {}]

def save_plg_data(data, PLG_DATA_FILE):
    with open(PLG_DATA_FILE, "w") as f:
        json.dump(data, f)

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
        os.makedirs(os.path.dirname(HOMEWORK_FILE), exist_ok=True)

        # Save the data to a JSON file
        with open(HOMEWORK_FILE, 'w') as file:
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
        if not os.path.exists(HOMEWORK_FILE):
            return jsonify({}), 200  # Return an empty object if no file exists

        with open(HOMEWORK_FILE, 'r') as file:
            data = json.load(file)

        return jsonify(data), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@bp.route('/plg', methods=['GET', 'POST'])
def plg():
    global PLANNING_FILE
    global HOMEWORK_FILE
    global semester
    global group
    global group_week
    plg_data = load_plg_data(PLANNING_FILE)

    if request.method == 'POST':
        semester = request.form.get('semester', 'SM1')
        group = request.form.get('group', 'S1')
        group_week = request.form.get('group_week', 'A')

        PLANNING_FILE = os.path.join(BASE_DIR, f'data/planning_data_{semester}_{group}_{group_week}.json')
        plg_data = get_plg_data(SM=semester, grp=group, grpWeek=group_week)
        save_plg_data(plg_data, PLANNING_FILE)

    HOMEWORK_FILE = os.path.join(BASE_DIR, f'data/homework_data_{semester}_{group}_{group_week}.json')
    
    return render_template('plg.html', plg_data=plg_data[0], title="Planning")

def get_plg_data(SM, grp, grpWeek):
    if os.path.exists(PLANNING_FILE) and os.path.getsize(PLANNING_FILE) > 0:
        with open(PLANNING_FILE, "r") as file:
            json_data = json.load(file)
        if json_data[1][-1]['jour'] == getDay():
            planning_data = json_data
    else:
        planning_data = scrap.main(SM, grp, grpWeek)

    for day, day_data in planning_data[0].items():
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

    print(planning_data)
    return planning_data


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
