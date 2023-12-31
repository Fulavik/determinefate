import asyncio, requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


chrome_options = Options()
# chrome_options.add_argument("headless")

async def get_partizans(surname: str, name: str, middlename: str, year_of_birth: int, rank: str):
    print(surname, name, middlename, year_of_birth, rank)
    service = Service(executable_path="chromedriver.exe")
    browser = webdriver.Chrome(options=chrome_options, service=service)

    link = f"https://obd-memorial.ru/html/search.htm?f={surname}&n={name}&s={middlename}&y={year_of_birth}&r={rank}"
    print(link)

    browser.get(link.replace("None", "").replace("0", ""))

    await asyncio.sleep(1.5)

    div_elements = browser.find_elements('tag name', 'div')

    results = {}

    for div in div_elements:
        if div.get_attribute('id'):
            id = div.get_attribute('id')

            if id.isdigit():
                full_name = div.find_element("css selector", "div:nth-child(3) > div:nth-child(1) > div:nth-child(1)").text
                date_of_birth = div.find_element("css selector", "div:nth-child(3) > div:nth-child(1) > div:nth-child(2)").text
                date_of_die = div.find_element("css selector", "div:nth-child(3) > div:nth-child(1) > div:nth-child(3)").text

                results.update({
                    f"{id}": {
                        "full_name": full_name,
                        "date_of_birth": date_of_birth,
                        "date_of_die": date_of_die
                    }
                })

    if len(results) == 0:
        return None

    return results

async def get_partizan_by_id(id: int):
    r = requests.get(f"https://obd-memorial.ru/html/info.htm?id={id}")

    if r.status_code == 404:
        return None

    soup = BeautifulSoup(r.text, 'lxml')

    surname = soup.find('span', {'class': 'card_param-title'}, text='Фамилия').find_next_sibling('span').text
    name = soup.find('span', {'class': 'card_param-title'}, text='Имя').find_next_sibling('span').text
    middlename = soup.find('span', {'class': 'card_param-title'}, text='Отчество').find_next_sibling('span').text
    try:
        date_of_bitrh = soup.find('span', {'class': 'card_param-title'}, text='Дата рождения/Возраст').find_next_sibling('span').text
    except:
        date_of_bitrh = "Не указано."
    try:
        place_of_birth = soup.find('span', {'class': 'card_param-title'}, text='Место рождения').find_next_sibling('span').text
    except:
        place_of_birth = "Не указано."
    try:
        call_place = soup.find('span', {'class': 'card_param-title'}, text='Дата и место призыва').find_next_sibling('span').text
    except:
        call_place = "Не указано."
    try:
        last_call_place = soup.find('span', {'class': 'card_param-title'}, text='Последнее место службы').find_next_sibling('span').text
    except:
        last_call_place = "Не указано."
    try:
        rank = soup.find('span', {'class': 'card_param-title'}, text='Воинское звание').find_next_sibling('span').text
    except:
        rank = "Не указано."
    try:
        reason_of_leave = soup.find('span', {'class': 'card_param-title'}, text='Причина выбытия').find_next_sibling('span').text
    except:
        reason_of_leave = "Не указано."
    try:
        date_of_leave = soup.find('span', {'class': 'card_param-title'}, text='Дата выбытия').find_next_sibling('span').text
    except:
        date_of_leave = "Не указано."
    try:
        place_of_leave = soup.find('span', {'class': 'card_param-title'}, text='Место выбытия').find_next_sibling('span').text
    except:
        place_of_leave = "Не указано."
    try:
        issue = soup.find('span', {'class': 'card_param-title'}, text='Название источника донесения').find_next_sibling('span').text
    except:
        issue = "Не указано."

    info = {
        "name": name, 
        "surname": surname,
        "middlename": middlename,
        "date_of_bitrh": date_of_bitrh, 
        "place_of_birth": place_of_birth, 
        "call_place": call_place,
        "last_call_place": last_call_place,
        "rank": rank,
        "reason_of_leave": reason_of_leave,
        "date_of_leave": date_of_leave, 
        "place_of_leave": place_of_leave,
        "issue": issue
    }

    return info
