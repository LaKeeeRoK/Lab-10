import requests
import json
import pyttsx3
import speech_recognition as sr
from datetime import datetime

# Функция для выполнения команды "перечислить" - вывести названия праздников
def list_holidays():
    response = requests.get('https://date.nager.at/api/v2/publicholidays/2020/GB')
    if response.status_code == 200:
        holidays = [holiday['localName'] for holiday in response.json()]
        print("Названия праздников:")
        for holiday in holidays:
            print(holiday)
        return holidays
    else:
        print("Ошибка получения данных")

# Функция для выполнения команды "сохранить" - сохранить названия праздников в файл
def save_names(filename, holidays):
    with open(filename, 'w') as file:
        for holiday in holidays:
            file.write(holiday + '\n')
    print(f"Названия праздников сохранены в файл {filename}")

# Функция для выполнения команды "даты" - сохранить даты и названия праздников в файл
def save_dates(filename):
    response = requests.get('https://date.nager.at/api/v2/publicholidays/2020/GB')
    if response.status_code == 200:
        holidays = response.json()
        with open(filename, 'w') as file:
            for holiday in holidays:
                file.write(f"{holiday['date']} - {holiday['localName']}\n")
        print(f"Даты и названия праздников сохранены в файл {filename}")
    else:
        print("Ошибка получения данных")

# Функция для выполнения команды "ближайший" - найти ближайший праздник к текущей дате
def nearest_holiday():
    response = requests.get('https://date.nager.at/api/v2/publicholidays/2020/GB')
    if response.status_code == 200:
        holidays = response.json()
        today = datetime.now().date()
        nearest = min(holidays, key=lambda x: abs(datetime.strptime(x['date'], '%Y-%m-%d').date() - today))
        print("Ближайший праздник:")
        print(nearest['localName'], nearest['date'])
        return nearest['localName']
    else:
        print("Ошибка получения данных")

# Функция для выполнения команды "количество" - вывести количество праздников
def count_holidays():
    response = requests.get('https://date.nager.at/api/v2/publicholidays/2020/GB')
    if response.status_code == 200:
        holidays = response.json()
        count = len(holidays)
        print(f"Количество праздников: {count}")
        return count
    else:
        print("Ошибка получения данных")

# Функция для распознавания команды и выполнения соответствующего действия
def process_command(command):
    if "перечислить" in command:
        list_holidays()
    elif "сохранить" in command:
        save_names("holidays.txt", list_holidays())
    elif "даты" in command:
        save_dates("holidays_dates.txt")
    elif "ближайший" in command:
        nearest_holiday()
    elif "количество" in command:
        count_holidays()
    else:
        print("Команда не распознана")

# Функция для распознавания голоса
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Скажите команду:")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio, language="ru-RU").lower()
        print("Вы сказали:", command)
        return command
    except sr.UnknownValueError:
        print("Голос не распознан")
        return ""
    except sr.RequestError:
        print("Ошибка запроса к сервису распознавания")
        return ""

# Функция для озвучивания текста
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Основной цикл работы ассистента
def main():
    while True:
        command = recognize_speech()
        if command:
            process_command(command)
            speak("Готово")

if __name__ == "__main__":
    main()