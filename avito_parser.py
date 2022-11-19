import sqlite3
import time
from datetime import datetime, timedelta

from bs4 import BeautifulSoup

import requests

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


options = webdriver.ChromeOptions()
options.add_argument("--disable-gpu")
options.add_argument("--headless")
options.add_argument(
    "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 " +
    "(KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
)
options.add_argument("Accept=image/avif,image/webp,*/*")


def insert_into_database(info: dict) -> None:
    """
    Функция проверяет, есть ли в базе данных строка с таким же id.
    Если нет, то добавляет это объявление в базу.

    :param info: Словарь с параметрами квартиры.
    """
    sqlite_connection = sqlite3.connect("realty.db")
    cursor = sqlite_connection.cursor()
    cursor.execute("""select id FROM avito WHERE id = (?)""", (info["id"],))
    result = cursor.fetchone()

    if (result is None) and (info["id"] is not None):
        cursor.execute(
            """INSERT INTO avito
            (id, Цена, Адрес, Ближайшее_метро, Дата_публикации,
            Количество_комнат, Общая_площадь, Жилая_площадь, Этаж,
            Балкон_или_лоджия, Тип_комнат, Высота_потолков, Санузел,
            Окна, Ремонт, Мебель, Тёплый_пол, Отделка, Техника,
            Способ_продажи, Вид_сделки, Тип_дома, Год_постройки,
            Этажей_в_доме, Пассажирский_лифт, Парковка, В_доме,
            Двор, Грузовой_лифт, Название_новостройки, Корпус_строение,
            Официальный_застройщик, Тип_участия, Срок_сдачи, Ссылка)
            VALUES
            (:id, :Цена, :Адрес, :Ближайшее_метро, :Дата_публикации,
            :Количество_комнат, :Общая_площадь, :Жилая_площадь, :Этаж,
            :Балкон_или_лоджия, :Тип_комнат, :Высота_потолков, :Санузел,
            :Окна, :Ремонт, :Мебель, :Тёплый_пол, :Отделка, :Техника,
            :Способ_продажи, :Вид_сделки, :Тип_дома,:Год_постройки,
            :Этажей_в_доме, :Пассажирский_лифт, :Парковка, :В_доме, :Двор,
            :Грузовой_лифт, :Название_новостройки, :Корпус_строение,
            :Официальный_застройщик, :Тип_участия, :Срок_сдачи, :Ссылка)""",
            info,
        )
        cursor.execute(
            """INSERT INTO description (id, Описание) VALUES (:id, :Описание)""", info
        )
        sqlite_connection.commit()
        cursor.close()

        print(f'Квартира {info["id"]} добавлена в базу')


URL = "https://www.avito.ru/sankt-peterburg/kvartiry/prodam-ASgBAgICAUSSA8YQ?s=104"


def get_links(url=URL) -> list:
    """
    Функция собирает ссылки на все объявления с данной страницы.

    :param url: Ссылка на страницу, где находятся объявления.
    :return: Список с ссылками на объявления.
    """
    links = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    items = soup.find_all("a", {"data-marker": "item-title"})
    for item in items:
        links.append(f'https://avito.ru/{item["href"]}')
    return links


def get_info():
    """
    Функция проходит по всем собранным объявлениям.
    Для каждого объявления формирует словарь с параметрами о квартире.
    Посылает запрос на добавление информации в базу данных.
    """
    links = get_links()
    with webdriver.Chrome(options=options) as browser:
        for link in links:
            time.sleep(10)
            browser.get(url=link)
            info = {
                "id": None,
                "Цена": None,
                "Адрес": None,
                "Ближайшее_метро": None,
                "Дата_публикации": None,
                "Количество_комнат": None,
                "Общая_площадь": None,
                "Площадь_кухни": None,
                "Жилая_площадь": None,
                "Этаж": None,
                "Балкон_или_лоджия": None,
                "Тип_комнат": None,
                "Высота_потолков": None,
                "Санузел": None,
                "Окна": None,
                "Ремонт": None,
                "Мебель": None,
                "Тёплый_пол": None,
                "Отделка": None,
                "Техника": None,
                "Способ_продажи": None,
                "Вид_сделки": None,
                "Тип_дома": None,
                "Год_постройки": None,
                "Этажей_в_доме": None,
                "Пассажирский_лифт": None,
                "Парковка": None,
                "В_доме": None,
                "Двор": None,
                "Грузовой_лифт": None,
                "Название_новостройки": None,
                "Корпус_строение": None,
                "Официальный_застройщик": None,
                "Тип_участия": None,
                "Срок_сдачи": None,
                "Ссылка": link,
                "Описание": None,
            }

            # Находим цену квартиры
            try:
                info["Цена"] = int(
                    browser.find_element(By.XPATH, '//span[@itemprop="price"]')
                    .get_attribute("content")
                    .strip()
                )
            except NoSuchElementException:
                pass

            # Находим адрес квартиры
            try:
                info["Адрес"] = (
                    browser.find_element(By.XPATH, '//div[@itemprop="address"]')
                    .find_element(By.TAG_NAME, "span")
                    .text.strip()
                )
            except NoSuchElementException:
                pass

            # Находим дату объявления и преобразуем ее в нормальный вид
            try:
                date = browser.find_element(
                    By.XPATH, '//span[@data-marker="item-view/item-date"]'
                ).text.lstrip("· ")
                if "сегодня" in date:
                    date = date.replace(
                        "сегодня", (datetime.today()).strftime("%d.%m.%Y")
                    )
                elif "вчера" in date:
                    date = date.replace(
                        "вчера",
                        (datetime.today() - timedelta(days=1)).strftime("%d.%m.%Y"),
                    )
                info["Дата_публикации"] = date
            except NoSuchElementException:
                pass

            # Находим id объявления
            try:
                info["id"] = int(
                    browser.find_element(
                        By.XPATH, '//span[@data-marker="item-view/item-id"]'
                    ).text.split()[1]
                )
            except NoSuchElementException:
                pass

            # Находим параметры квартиры
            try:
                parameters_apartments = browser.find_element(
                    By.XPATH, "//div[@data-marker='item-view/item-params']"
                ).find_elements(By.TAG_NAME, "li")
                for point in parameters_apartments:
                    info[
                        point.text.split(":")[0].replace(" ", "_").replace(",", "")
                    ] = point.text.split(":")[1].strip()
            except NoSuchElementException:
                pass

            # Находим параметры дома
            try:
                parameters_house = (
                    browser.find_element(By.XPATH, '//div[text()="О доме"]')
                    .find_element(By.XPATH, "..")
                    .find_elements(By.TAG_NAME, "li")
                )
                for point in parameters_house:
                    info[
                        point.text.split(":")[0].replace(" ", "_").replace(",", "")
                    ] = point.text.split(":")[1].strip()
            except NoSuchElementException:
                pass

            # Находим ближайшее метро
            try:
                metro = browser.find_elements(
                    By.XPATH,
                    '//span[@class="style-item-address-georeferences-item-TZsrp"]',
                )
                info["Ближайшее_метро"] = "".join([x.text for x in metro])
            except NoSuchElementException:
                pass

            # Находим описание квартиры
            try:
                info["Описание"] = "".join(
                    [
                        x.strip()
                        for x in browser.find_element(
                            By.XPATH, '//div[@data-marker="item-view/item-description"]'
                        ).text.split("\n")
                    ]
                )
            except NoSuchElementException:
                pass

            insert_into_database(info)


def main():
    while True:
        print(f"Время {datetime.now()}")
        get_info()
        print("Новые квартиры на странице закончились\n")
        time.sleep(600)


if __name__ == "__main__":
    main()
