from flask import Blueprint, render_template
import scrap.scraping as scrap

# create a Blueprint
bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    header_title = "Welcome to Plancton"
    header_desc = "Your personal planning assistant. Stay organized, track your tasks, and manage your schedule effortlessly. Let's get started!"
    return render_template('index.html', header_title=header_title, header_desc=header_desc)

@bp.route('/plg')
def plg():
    header_title = "Get Started with Plancton"
    header_desc = "Organize your tasks and stay on top of your schedule with Plancton. Start now and take control of your day!"
    plg_data = get_plg_data()
    return render_template('plg.html', plg_data=plg_data, header_title=header_title, header_desc=header_desc)


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
    print("plg_data: \n\n\n", plg_data)
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