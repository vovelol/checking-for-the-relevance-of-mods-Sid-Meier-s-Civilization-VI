import requests
from bs4 import BeautifulSoup

input_file = "mod_states.txt"

def fetch_mod_details(mod_id):
    url = f"https://steamcommunity.com/sharedfiles/filedetails/?id={mod_id}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        # Находим все элементы с классом `detailsStatRight`
        date_divs = soup.find_all("div", class_="detailsStatRight")
        return [div.text.strip() for div in date_divs]  # Возвращаем список текстов элементов
    return []

def read_saved_states():
    """Читает сохранённые состояния модов из файла."""
    mod_states = {}
    with open(input_file, "r", encoding="utf-8") as file:
        current_mod = None
        for line in file:
            line = line.strip()
            if line.startswith("Mod ID"):
                current_mod = line.split(" ")[-1].strip(":")
                mod_states[current_mod] = []
            elif line.startswith("Element"):
                mod_states[current_mod].append(line.split(": ", 1)[1])
    return mod_states

def compare_mod_states():
    """Сравнивает сохранённые состояния с текущими."""
    saved_states = read_saved_states()
    for mod_id, saved_elements in saved_states.items():
        current_elements = fetch_mod_details(mod_id)
        if current_elements != saved_elements:
            print(f"Mismatch found for Mod ID {mod_id}")


if __name__ == "__main__":
    compare_mod_states()
