from flask import Blueprint, render_template, request, jsonify
import scrap.scraping as scrap
import json, os

# create a Blueprint
bp = Blueprint('main', __name__)

base_dir = os.path.dirname(os.path.abspath(__file__))
json_file_path = os.path.join(base_dir, 'list_data.json')

@bp.route('/')
def index():
    return render_template('index.html', title="Home")

@bp.route('/plg')
def plg():
    plg_data = get_plg_data()
    return render_template('plg.html', plg_data=plg_data, title="Planning")

@bp.route('/saveList', methods=['POST'])
def save_list():
    data = request.get_json()

    my_list = data.get('list', [])

    try:
        with open(json_file_path, 'w') as f:
            json.dump(my_list, f, indent=4)
        return jsonify({"message": "List successfully saved!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/getList', methods=['GET'])
def get_list():
    try:
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r') as f:
                homeworksList = json.load(f)
            return jsonify({"list": homeworksList}), 200
        else:
            return jsonify({"message": "No list found."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

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
