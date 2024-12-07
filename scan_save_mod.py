import os
import re
import requests
from bs4 import BeautifulSoup

# Путь к папке с модами
mods_path = r"C:\Games\cvka\Sid Meiers Civilization VI v1.0.12.58 by Pioneer\Sid Meiers Civilization VI\DLC"
output_file = "mod_states.txt"

def extract_mod_id(filename):
    # Проверяем, начинается ли имя файла с цифры
    if filename[0].isdigit():
        # Извлечение чисел до "_"
        match = re.match(r"(\d+)", filename)
        return match.group(1) if match else None
    return None

def fetch_mod_details(mod_id):
    url = f"https://steamcommunity.com/sharedfiles/filedetails/?id={mod_id}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        # Находим все элементы с классом `detailsStatRight`
        date_divs = soup.find_all("div", class_="detailsStatRight")
        elements = [div.text.strip() for div in date_divs]  # Сохраняем текст всех элементов
        return elements
    return []

def save_mod_states():
    with open(output_file, "w", encoding="utf-8") as file:
        for mod_file in os.listdir(mods_path):
            mod_id = extract_mod_id(mod_file)  # Извлекаем ID мода, если он начинается с цифры
            if mod_id:
                details = fetch_mod_details(mod_id)  # Получаем все элементы
                file.write(f"Mod ID {mod_id}:\n")
                for idx, detail in enumerate(details, start=1):
                    file.write(f"Element {idx}: {detail}\n")
                file.write("\n")  # Пустая строка между модами
                print(f"Saved Mod ID {mod_id}")

if __name__ == "__main__":
    save_mod_states()
