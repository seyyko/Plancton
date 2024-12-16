from playwright.async_api import async_playwright, Playwright
import datetime, os, re, asyncio, nest_asyncio, json

nest_asyncio.apply()

URL_A = "https://proseconsult.umontpellier.fr/direct/?data=5ac561a2326f3677ab1a9118f59438fd4f51f7d91eb3648604d628113e82760dbed8d89011b8db3f565a6eba3fb421d313f6c63370d69630c73e5d47e7b4caa205b671755e2e313accf1c0ae7bea9fe2ffaaa69cbd14fea5a6d0111bfaa17a823cc1c3b4302fc5dd2762be0aa3a53986aa46015363b2752612a410752d15eaafd211eeb7936734e0cd7fd38213cedc0eec845302a004ead06829e11b88069c0470ffb5ed45df960ede2292b82b30eb71d41a159a6dca32169d785b1c27d7c5e2,1"
URL_B = "https://proseconsult.umontpellier.fr/direct/?data=5ac561a2326f3677ab1a9118f59438fd4f51f7d91eb3648604d628113e82760dbed8d89011b8db3f565a6eba3fb421d313f6c63370d69630c73e5d47e7b4caa205b671755e2e313accf1c0ae7bea9fe2ffaaa69cbd14fea5a6d0111bfaa17a823cc1c3b4302fc5dd2762be0aa3a53986aa46015363b2752612a410752d15eaafd211eeb7936734e0cd7fd38213cedc0eec845302a004ead06829e11b88069c0470ffb5ed45df960ede2292b82b30eb713c31274445b36b718cbc128f95bf301d,1"
XML_PATH = '//*[@id="Planning"]/div'
DATE = datetime.datetime.now()
DAYS = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']

file_dir = os.path.dirname(os.path.abspath(__file__))
courses_file = os.path.join(file_dir, "cache_files/courses.json")

Wtable = {
    'Monday': 'Lundi',
    'Tuesday': 'Mardi',
    'Wednesday': 'Mercredi',
    'Thursday': 'Jeudi',
    'Friday': 'Vendredi',
    'Saturday': 'Samedi',
    'Sunday': 'Dimanche'
}

def delSpace(char: str) -> str:
    return " ".join(char.split())

def howManyHours(all_class: list) -> str:
    total = 0
    for classes in all_class:
        hour = classes['heure']
        h1 = int(hour[0][0]) * 60 + int(hour[0][1])
        h2 = int(hour[1][0]) * 60 + int(hour[1][1])
        total += h2 - h1
    
    hours = total // 60
    minutes = total % 60
    return f"{hours}h{minutes:02d}"

def getDay():
    return Wtable[datetime.datetime.now().strftime('%A')]

def getSmoothHour(l: list):
    return f"{l[0][0]}h{l[0][1]} - {l[1][0]}h{l[1][1]}"

def isItWeekA(date: datetime.date) -> bool:
    date_ref = datetime.date(2024, 6, 12)
    weeks_difference = (date - date_ref).days // 7
    print(weeks_difference % 2 == 0)
    return weeks_difference % 2 == 0

async def scrap(pw: Playwright):
    if os.path.exists(courses_file) and os.path.getsize(courses_file) > 0:
        with open(courses_file, "r") as file:
            data = json.load(file)
        if data[1][-1]['jour'] == getDay():
            return data


    chromium = pw.chromium
    browser = await chromium.launch()
    context = await browser.new_context(viewport={"width": 1920, "height": 1080})
    page = await context.new_page()

    if isItWeekA(DATE.date()):
        await page.goto(URL_A)
    else:
        await page.goto(URL_B)
    await page.wait_for_timeout(5000)

    parsed = []
    course_boxes = page.locator(XML_PATH)

    for box in await course_boxes.element_handles():
        data = await box.query_selector(".eventText")
        data = await data.get_attribute("aria-label")

        id = await box.get_attribute("style")
        
        pattern_id = r"\d{1,}px"
        regex_id = re.findall(pattern_id, id)[0][:-2]

        pattern_data = 'null'
        regex_data = re.split(pattern_data, data)

        hours = regex_data[-1].split('h')
        hours[1] = hours[1].split(' - ')
        list_hour = [(hours[0][1:], hours[1][0]), (hours[1][1], hours[2])]

        classroom = delSpace(regex_data[1]) if delSpace(regex_data[1]) != 'Cours en ligne (CEL) IUTMS' else 'Cours en ligne'

        parsed.append({
            "id": int(regex_id),
            "nom": delSpace(regex_data[0]),
            "salle": classroom,
            "heure": list_hour,
            "heure_plate": getSmoothHour(list_hour)
        })

    id_selector = [-1, -1, -1, -1, -1, -1, -1]
    j = 0
    for course in parsed:
        id = course["id"]
        if id not in id_selector:
            id_selector[j] = id
            j += 1

    Rtable = {id_selector[i]: DAYS[i] for i in range(len(id_selector)) if id_selector[i] != -1}
    dict_course = {day: [] for day in DAYS}

    for course in parsed:
        id = course["id"]
        dict_course[Rtable[id]].append(course)

    for day in dict_course:
        dict_course[day].append({
            'jour': day,
            'total_classes': len(dict_course[day]),
            'total_heures': howManyHours(dict_course[day])
        })

    today = getDay()
    today_classes = dict_course[today]

    tup = (dict_course, today_classes)
    
    with open(courses_file, "w") as file:
        json.dump(tup, file, indent=4, ensure_ascii=False)

    await browser.close()
    return tup

async def run():
    async with async_playwright() as playwright:
        return await scrap(playwright)

def main():
    return asyncio.run(run())

if __name__ == "__main__":
    main_data = main()
    de = main_data[0]
    tc = main_data[1]

    print(de, "\n\n\n", tc, "\n\n\n")

    # print(json.dumps(de, indent=4, ensure_ascii=False))
    # print("\n\n")
    # print(json.dumps(tc, indent=4, ensure_ascii=False))
