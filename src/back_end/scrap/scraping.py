import datetime, os, re, asyncio, nest_asyncio; nest_asyncio.apply()
from playwright.async_api import async_playwright, Playwright

URL_A = "https://proseconsult.umontpellier.fr/direct/?data=5ac561a2326f3677ab1a9118f59438fd4f51f7d91eb3648604d628113e82760dbed8d89011b8db3f565a6eba3fb421d313f6c63370d69630c73e5d47e7b4caa205b671755e2e313accf1c0ae7bea9fe2ffaaa69cbd14fea5a6d0111bfaa17a823cc1c3b4302fc5dd2762be0aa3a53986aa46015363b2752612a410752d15eaafd211eeb7936734e0cd7fd38213cedc0eec845302a004ead06829e11b88069c0470ffb5ed45df960ede2292b82b30eb71d41a159a6dca32169d785b1c27d7c5e2,1"
URL_B = "https://proseconsult.umontpellier.fr/direct/?data=5ac561a2326f3677ab1a9118f59438fd4f51f7d91eb3648604d628113e82760dbed8d89011b8db3f565a6eba3fb421d313f6c63370d69630c73e5d47e7b4caa205b671755e2e313accf1c0ae7bea9fe2ffaaa69cbd14fea5a6d0111bfaa17a823cc1c3b4302fc5dd2762be0aa3a53986aa46015363b2752612a410752d15eaafd211eeb7936734e0cd7fd38213cedc0eec845302a004ead06829e11b88069c0470ffb5ed45df960ede2292b82b30eb713c31274445b36b718cbc128f95bf301d,1"
XML_PATH = '//*[@id="Planning"]/div'
DATE = datetime.datetime.now().strftime('%D')
DAYS = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']

file_dir = os.path.dirname(os.path.abspath(__file__))
events_file = os.path.join(file_dir, "cache_files/events.txt")
oscillator_file = os.path.join(file_dir, "cache_files/oscillator.txt")

# Table de relation pour traduire de EN à FR.
Wtable = {'Monday': 'Lundi',
          'Tuesday': 'Mardi',
          'Wednesday': 'Mercredi',
          'Thursday': 'Jeudi',
          'Friday': 'Vendredi',
          'Saturday': 'Samedi',
          'Sunday': 'Dimanche'}


def delSpace(char:str) -> str:
    return " ".join(char.split())


def howManyClassesWeek(d:dict) -> int:
    sum = 0
    for day in DAYS:
        sum += len(d[day])
    return sum - 5


def howManyHours(all_class:list) -> str:
    total = 0
    for classes in all_class:
        hour = classes['heure']
        
        if hour[0][1] < hour[1][1]:
            h1 = hour[0][0]+hour[0][1]
            h2 = hour[1][0]+hour[1][1]
        # min. start > min. end (e.g. start at 14h15 and end at 15h);
        else:
            h1 = hour[0][0]+hour[1][1]
            h2 = hour[1][0]+hour[0][1]
        total += int(h2)-int(h1)
    total = str(total)
    
    return total[:2] + 'h' + total[2:] if len(total) > 3 else total[0] + 'h' + total[1:]

def howManyHoursWeek(d:dict):
    h1, h2 = 0, 0
    for event in d:
        h = d[event][-1]['total_heures'].split('h')
        if h[1] == "":
            h[1] = '00'
        h1 += int(h[0])
        h2 += int(h[1])
    sup_min = h2%60
    sup_hour = h2//60
    hours = h1 + sup_hour
    minutes = sup_min
    return f'{hours}h{minutes}'


def getDay():
    return Wtable[datetime.datetime.now().strftime('%A')]


def getSmoothHour(l:list):
    hours = f"{l[0][0]}h{l[0][1]} - {l[1][0]}h{l[1][1]}"
    return hours


def isItWeekA(date:str):
    file = open(oscillator_file, "r")
    data = eval(file.read())
    file.close()

    print(data)

    if date in data:
        return data[date]
    
    data[date] = int(not data[list(data)[-1]])

    return data[date]
    

async def scrap(pw: Playwright):
    file = open(events_file, "r")
    data = eval(file.read())
    file.close()

    if data is not None and data[1][-1]['jour'] == getDay():
        return data

    chromium = pw.chromium
    browser = await chromium.launch()

    context = await browser.new_context(viewport={"width": 1920, "height": 1080})
    page = await context.new_page()

    if isItWeekA(DATE):
        await page.goto(URL_A)
    else:
        await page.goto(URL_B)
    await page.wait_for_timeout(5000)

    parsed = []
    event_boxes = page.locator(XML_PATH)

    for box in await event_boxes.element_handles():
        data = await box.query_selector(".eventText")
        data = await data.get_attribute("aria-label")

        id = await box.get_attribute("style")

        pattern_data = 'null'
        regex_data = re.split(pattern_data, data)

        pattern_id = r"\d{1,}px"
        regex_id = re.findall(pattern_id, id)[0][:-2]

        list_hour = [None, None]
        hours = regex_data[-1].split('h')
        hours[1] = hours[1].split(' - ')
        list_hour[0], list_hour[1] = (hours[0][1:], hours[1][0]), (hours[1][1], hours[2])

        classroom = delSpace(regex_data[1]) if delSpace(regex_data[1]) != 'Cours en ligne (CEL) IUTMS' else 'Cours en ligne'

        parsed.append({
            "id":int(regex_id),
            "nom":delSpace(regex_data[0]),
            "salle":classroom,
            "heure":list_hour,
            "heure_plate":getSmoothHour(list_hour)
        })

    id_selector = [-1, -1, -1, -1, -1, -1, -1]
    j = 0
    for event in parsed:
        id = event["id"]
        if id not in id_selector:
            id_selector[j] = id
            j += 1

    Rtable = {}
    for i, ids in enumerate(id_selector):
        if ids == -1:
            break
        Rtable[ids] = DAYS[i]
        
    dict_event = {'Lundi': [],
                    'Mardi': [],
                    'Mercredi': [],
                    'Jeudi': [],
                    'Vendredi': [],
                    'Samedi': [],
                    'Dimanche': []}
    
    for event in parsed:
        id = event["id"]
        dict_event[Rtable[id]].append(event)
        
    for day in dict_event:
        dict_event[day].append({'jour': day, 'total_classes': len(dict_event[day]), 'total_heures': howManyHours(dict_event[day])})

    today = getDay()
    today_classes = dict_event[today]
    
    tup = (dict_event, today_classes)
    file = open(events_file, "w")
    file.write(str(tup))
    file.close()

    await browser.close()
    return tup
    

async def run():
    async with async_playwright() as playwright:
        return await scrap(playwright)
    

def main():
    return asyncio.run(run())



if __name__ == "__main__":
    main = main()
    
    de = main[0]
    tc = main[1]

    print(de)
    print("\n\n")
    print(tc)
    print("\n\n")

    print(howManyHoursWeek(de))