from PIL import Image, ImageDraw, ImageFont
import os, scraping

longueur = 220
largeur = 950
background = (54,57,62)
text_color = "white"

fontsize = 10
file_dir = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(file_dir, "img/agenda_day.jpeg")
font = ImageFont.truetype(os.path.join(file_dir, "fonts/CamingoCode-Bold.ttf"), fontsize)


def draw_text(nom_img, txt, x, y):
    img = Image.open(nom_img)
    draw = ImageDraw.Draw(img)
    draw.text((x,y), txt, text_color, font=font)
    img.save(nom_img, quality=100)
    return img


def createAgenda(start:int, agenda:dict):
    new_im = Image.new('RGB', (longueur, largeur), background)
    new_im.save(src, quality=100)
    
    while start <= 1930:
        if str(start)[-2:] == "60":
            h = str(int(str(start)[:-2]) + 1)
            m = "00"
            start = int(h+m)
            continue
        if len(str(start)) > 3:
            agenda[str(start)[:-2]+'h'+str(start)[-2:]] = [] 
        else: agenda["0"+str(start)[:-2]+'h'+str(start)[-2:]] = []
        start += 15


def getNextTick(time:str):
    return time[:3] + str(int(time[3:]) + 15) if int(time[3:]) != 45 else str(int(time[:2]) + 1) + "h" + "00"


def setEvent(time:list, name:str, classroom:str, agenda:dict):
    # [('08', '00'), ('08', '45')]
    # "Gestion proj. orga."
    # "Cours en ligne (CEL) IUTMS"
    start = time[0][0]+"h"+time[0][1]
    header_name = getNextTick(start)
    header_classroom = getNextTick(header_name)
    end = time[1][0]+"h"+time[1][1]

    agenda[start].append("$"+"#"*24)
    agenda[header_name].append(name)
    agenda[header_classroom].append(classroom)
    agenda[end].append("#"*24+"€")


def completeAgenda(tdy_classes:list, agenda:dict):
    for classes in tdy_classes[:-1]:
        setEvent(classes['heure'], classes['nom'], classes['salle'], agenda)


def getAgenda(agenda:dict):
    l = []
    for i, time in enumerate(agenda):
        e = "".join(agenda[time]).center(25)
        if e[0] == "$" and e[-1] == "#":
            l.append((50, (i+.5)*20 + 5))
        elif e[0] == "#" and e[-1] == "€":
            l.append((192, (i+.5)*20 + 10))
        txt = "".join((time if time[0] != "0" else time[1:].center(5), "-", e, "\n"))

        if len(l) == 2:
            img = Image.open(src)
            rect = ImageDraw.Draw(img)
            rect.rectangle(l, fill=	(114,137,218))
            img.save(src, quality=100)
            l = []

    for i, time in enumerate(agenda):
        e = "".join(agenda[time]).center(25)
        if e[0] == "$" and e[-1] == "#" or e[0] == "#" and e[-1] == "€":
            e=""
        txt = "".join((time if time[0] != "0" else time[1:].center(5), "-", e, "\n"))
        draw_text(src, txt, 10, (i+.5)*20)


def main(tdy_classes):
    start = 800
    agenda = dict()

    createAgenda(start, agenda)
    completeAgenda(tdy_classes, agenda)
    getAgenda(agenda)

    return agenda

if __name__ == "__main__":

    # today_classes = [
    #     {'id': 0, 'nom': 'Initiation au dev.', 'salle': 'Cours en ligne', 'heure': [('08', '00'), ('09', '00')], 'heure plate': '08h00 - 09h00'},
    #     {'id': 0, 'nom': 'Intro. systèmes', 'salle': 'Cours en ligne', 'heure': [('09', '15'), ('10', '15')], 'heure plate': '09h15 - 10h15'},
    #     {'id': 0, 'nom': 'Gestion proj. orga.', 'salle': 'Cours en ligne', 'heure': [('10', '30'), ('11', '45')], 'heure plate': '10h30 - 11h45'},
    #     {'id': 0, 'nom': 'Initiation au dev.', 'salle': 'Salle 52', 'heure': [('14', '30'), ('16', '30')], 'heure plate': '14h30 - 16h30'},
    #     {'id': 0, 'nom': 'PPP', 'salle': 'TD1.10', 'heure': [('16', '45'), ('18', '15')], 'heure plate': '16h45 - 18h15'},
    #     {'jour': 'Lundi', 'total_classes': 5, 'total_heures': '7h45'}]

    today_classes = scraping.main()[1]

    print(main(today_classes))