from playwright.async_api import async_playwright, Playwright
import datetime, os, re, asyncio, nest_asyncio, json

nest_asyncio.apply()

BASE_URL = "https://proseconsult.umontpellier.fr/direct/?data=5ac561a2326f3677ab1a9118f59438fd4f51f7d91eb3648604d628113e82760dbed8d89011b8db3f565a6eba3fb421d313f6c63370d69630c73e5d47e7b4caa205b671755e2e313accf1c0ae7bea9fe2ffaaa69cbd14fea5a6d0111bfaa17a823cc1c3b4302fc5dd2762be0aa3a53986aa46015363b2752612a410752d15eaafd211eeb7936734e0cd7fd38213cedc0eec845302a004ead06829e11b88069c0470ffb5ed45df960ede2292b82b30eb71"

grp_class = {

    'SM1': {
        'S1': {
            'URL_A': '6ce7222fa637bcfa9672911335cef256,1',
            'URL_B': 'f428fc2c109066826a02cf2bb87d17f5,1',
        },
        'S2': {
            'URL_A': 'd41a159a6dca32169d785b1c27d7c5e2,1',
            'URL_B': '3c31274445b36b718cbc128f95bf301d,1',
        },
        'S3': {
            'URL_A': 'fe98c3241d4aadae2ffa65e7f92005a7,1',
            'URL_B': 'd4721bd8a135a30ded28d9a1f102ffed,1',
        },
        'S4': {
            'URL_A': 'f2eb3dd0e46aea6dc414b934302928fb,1',
            'URL_B': 'c32362317deadf5ad45cc155e328f16f,1',
        },
        'S5': {
            'URL_A': '0b1cbde941298ca18c26bdcad1eb8745,1',
            'URL_B': 'a93503033ca02a65db59d56e9b816deb,1',
        }
    },
    'SM2': {
        'S1': {
            'URL_A': '4f36dde892fa4493d29d62c8bf6b04c0,1',
            'URL_B': '55ce413688b6cf5296dc5bbf404082ff,1',
        },
        'S2': {
            'URL_A': '47b6f1e1d8ac94a7bbbde8d1f61bd15a,1',
            'URL_B': '83221260d6469a64728eddb5f59f20bf,1',
        },
        'S3': {
            'URL_A': '95d55e4dda5b17a5184169aedf339b01,1',
            'URL_B': 'f5d5c6f674d2d5e0f0d705c67bbf6746,1',
        },
        'S4': {
            'URL_A': '85a2c351285429ef122463d00bb33d8c,1',
            'URL_B': '91d9a81f1cb6fffcd4670b792118e2ec,1',
        },
        'S5': {
            'URL_A': '86120ffec4b32abcd7251f55bac011f1,1',
            'URL_B': '268feb9c5b619d37ba21cf9e1012a700,1',
        }
    },
    'SM3': {
        'Q1': {
            'URL_A': 'bc492639e450e01015fbc0a41c37395d,1',
            'URL_B': '17d40dca3e8d16f2ddc04478ecd9d05d,1',
        },
        'Q2': {
            'URL_A': 'c59629fc2244712c157ebbf910d125b1,1',
            'URL_B': '8d8808d658f1e7cd4a958e3b9cf053cf,1',
        },
        'Q3': {
            'URL_A': '209a75b5b0f7d98c9b8b5034ddf4ecd7,1',
            'URL_B': '8f8e3e4456fa9c8f7d93005cf66cb004,1',
        },
        'Q4': {
            'URL_A': 'a4de5be01cc4261869752713a6cfb5ca,1',
            'URL_B': 'c80e41f211be0a161de4d5c7fd57c9ed,1',
        }
    },
    'SM4': {
        'Q1': {
            'URL': 'ec07272fc6fa8eaec86e9aa3adb440dc,1'
        },
        'Q2': {
            'URL': '9b39e42545ac0e2601a857f2e856cf11,1'
        },
        'Q3': {
            'URL': '544070c862197a6bd7263e4fc64531b9,1'
        },
        'Q4': {
            'URL': 'beddb424634146ffdb01d12611b63a1a,1'
        }
    },
    'SM5': {
        'G1': {
            'URL': 'b7f958b6a4e187951a5297938fe7ccb2,1'
        },
        'G2': {
            'URL': 'f5f63c64469f19d3ae90f017019dad1d,1'
        },
        'G3': {
            'URL': '99f8b54bea24fd5de7a1ccda46944f09,1'
        },
        'G4': {
            'URL': 'a726124b015519875892de640d85723e,1'
        }
    },
    'SM6': {
        'G1': {
            'URL': '9befe9af9f9e74132a9796390ffa92a4,1'
        },
        'G2': {
            'URL': '00cc99c655eef57eb33b38b094b2a672,1'
        },
        'G3': {
            'URL': 'df348820256a73c13c906aa75494d1b6,1'
        },
        'G4': {
            'URL': '1fce8a4bd8fcde1e419c14fdc907aaad,1'
        }
    }
}

XML_PATH = '//*[@id="Planning"]/div'
DATE = datetime.datetime.now()
DAYS = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']

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

async def scrap(pw: Playwright, SM: str, grp: str, grpWeek: str):

    chromium = pw.chromium
    browser = await chromium.launch()
    context = await browser.new_context(viewport={"width": 1920, "height": 1080})
    page = await context.new_page()

    if isItWeekA(DATE.date()):
        if len(grp_class[SM][grp]) == 1:
            pg = grp_class[SM][grp]['URL']
        else:
            pg = grp_class[SM][grp]['URL_A'] if grpWeek == 'A' else grp_class[SM][grp]['URL_B']
        await page.goto(BASE_URL + pg)
    else:
        if len(grp_class[SM][grp]) == 1:
            pg = grp_class[SM][grp]['URL']
        else:
            pg = grp_class[SM][grp]['URL_B'] if grpWeek == 'B' else grp_class[SM][grp]['URL_A']
        await page.goto(BASE_URL + pg)
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

    await browser.close()
    return dict_course, today_classes

async def run(SM: str, grp: str, grpWeek: str):
    async with async_playwright() as playwright:
        return await scrap(playwright, SM, grp, grpWeek)

def main(SM: str='SM1', grp: str='S2', grpWeek: str='A'):
    return asyncio.run(run(SM, grp, grpWeek))

if __name__ == "__main__":
    main_data = main()
    de = main_data[0]
    tc = main_data[1]

    print(de, "\n\n\n", tc, "\n\n\n")

    # print(json.dumps(de, indent=4, ensure_ascii=False))
    # print("\n\n")
    # print(json.dumps(tc, indent=4, ensure_ascii=False))
