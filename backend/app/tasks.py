import re
from datetime import datetime

from email import message_from_file
from email.utils import parsedate_to_datetime
from locale import setlocale, LC_TIME

from huey import crontab
from huey.contrib.djhuey import periodic_task
from os import path

from app.models import Menu, FirstCourse, SecondCourse, SideCourse, ContentMenu

DATE_REGEX = r"menu' del giorno ([0-9]{1,2} (gennaio|febbraio|marzo|aprile|maggio|giugno|luglio|agosto|settembre|ottobre|novembre|dicembre){1} [0-9]{4})"
PRICE_REGEX = r"^([0-9]\.*[0-9]*) euro$"

setlocale(LC_TIME, 'it_IT')

def normalize_words(word):
    word = word.strip()
    if ((len(re.findall(r"( )", word)) * 100) / len(word)) > 40:
        word = re.sub(r"( )", "", word)
    return word


def elaborate_email(message):
    text = message.get_payload()[0].get_payload(decode=True).decode('utf-8').lower()

    date = None
    dish_type = None
    price = None
    temperature = None
    cooking = None
    first_dish_type = None
    second_dish_type = None

    menu = None

    for word in re.findall(r"“(.*)”", text):
        text = text.replace("“%s”" % word, "%s" % normalize_words(word))
    text = re.sub(re.compile(r"^> ", re.MULTILINE), "", text)
    text = re.sub(r"[\n]{2,}", "\n", text)
    text = re.sub(r"[ ]{2,}", " ", text)
    text = re.sub(r">", "\n", text)
    text = re.sub(r"insalatona (\w*)\n(\(.*\))", "insalatona\n\g<1> \g<2>", text)

    for line in text.split("\n"):
        line = line.strip()
        if len(re.findall(DATE_REGEX, line)) == 1:
            date = datetime.strptime(re.findall(DATE_REGEX, line)[0][0].title(), "%d %B %Y")
            menu = Menu.objects.create(consumeDate=date,
                                       sendDate=parsedate_to_datetime(message.get('Date')))
        elif len(re.findall(PRICE_REGEX, line)) == 1:
            price = float(re.findall(PRICE_REGEX, line)[0])
        elif "compreso contorno" in line:
            continue
        elif line == "primi piatti di terra":
            dish_type = FirstCourse
            temperature = 'C'
            first_dish_type = 'T'
        elif line == "piatto freddo":
            temperature = 'F'
        elif line == "primi piatti di mare":
            dish_type = FirstCourse
            temperature = 'C'
            first_dish_type = 'M'
        elif line == "secondi piatti di terra":
            dish_type = SecondCourse
            second_dish_type = 'T'
        elif "insalatona" in line:
            dish_type = SecondCourse
            second_dish_type = 'I'
        elif line == "contorni":
            dish_type = SideCourse
            cooking = 'N'
        elif line == "al vapore":
            cooking = 'V'
        elif line == "al forno":
            cooking = 'F'
        elif "menù n°" in line:
            break
        elif dish_type:
            dish = None
            if dish_type is FirstCourse:
                dish = dish_type.objects.get_or_create(name=line, contentType=first_dish_type, cookingType=temperature)
                ContentMenu.objects.create(course=dish[0], menu=menu, price=price)
            elif dish_type is SecondCourse:
                notes = None
                if re.findall(r"\((.*)\)", line):
                    notes = re.findall(r"\((.*)\)", line)[0][0]
                line = re.sub(r"\((.*)\)", '', line)
                dish = dish_type.objects.get_or_create(name=line, contentType=second_dish_type, notes=notes)
                ContentMenu.objects.create(course=dish[0], menu=menu, price=price)
            elif dish_type is SideCourse:
                for name_dish in re.split(r"[‐‑‒–−𐆑\-]", line):
                    dish = dish_type.objects.get_or_create(name=name_dish.strip(), cookingType=cooking)
                    ContentMenu.objects.create(course=dish[0], menu=menu, price=price)


@periodic_task(crontab(minute="*"))
def receive_email():
    message = message_from_file(open(path.join("..", "fake_data", "MENU_8.8P.eml")))
    #if not Menu.objects.filter(sendDate=parsedate_to_datetime(message.get('Date'))):
    elaborate_email(message)
