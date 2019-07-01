import pyttsx3
from tipo_rabotaet.comands import *
from fuzzywuzzy import fuzz
engine = pyttsx3.init()
F = {
    "objs" : {
        "apple": ("яблоко", "яблоки", "яблочки", "яблочко", "яблока"),
        "bottle": ("бутылку", "бутылки"),
        "banana": ("банан", "бананы"),
        "toy": ("игрушки", "игрушку", "игрухи"),
        "money": ("деньги", "банкноты"),
        "bag": ("пакет", "пакеты", "пакета"),
        "glass bottle": ("стеклянная бутылка", "стеклянные бутылки"),
        "plastic bottle": ("пластиковая бутылка", "пластиковые бутылки")
              },
    "cmds" : {
        "get": ("собери", "принеси", "неси"),
        "add": ("добавить", "присоединить", "добавь")
    },
    "num":
        {
            "1": ("один", "одну", "1"),
            "2": ("два", "две", "2"),
            "3": ("три", "3"),
            "4": ("четрыре", "4"),
            "5": ("пять", "5"),
            "6": ("шесть", "6"),
            "7": ("семь", "7"),
            "8": ("восемь", "8"),
            "all": ("все")
        }
}
def recognize_obj(obj):
    RC = {"object": '', "percent": 0}
    for c, v in F["objs"].items():
        for x in v:
            vrt = fuzz.ratio(obj,x)
            if vrt > RC["percent"]:
                RC["percent"] = vrt
                RC["object"] = c
    return RC

def recognize_col(num):
    RC = {"num": 0, "percent": 0}
    for c,v in F["num"].items():
        for x in v:
            vrt = fuzz.ratio(num,x)
            if vrt > RC["percent"]:
                RC["percent"] = vrt
                RC["num"] = c
    return RC

def recognize_cmd(cmd):
    RC = {"cmd": '', "percent" : 0}
    for c, v in F["cmds"].items():
        for x in v:
            vrt = fuzz.ratio(cmd,x)
            if vrt > RC["percent"]:
                RC["percent"] = vrt
                RC["cmd"] = c
    return RC



import speech_recognition as sr
r = sr.Recognizer()
with sr.Microphone(device_index=1) as source:
    print("Слухаю")
    audio = r.listen(source,phrase_time_limit=5)

print("распознаю")
query = r.recognize_google(audio, language="ru-RU")
task = query.lower()
print(task)
F["objs"] = get_obj()
if len(task.split()) >= 3:
    com, num, obj = task.split(maxsplit = 2)
    print(recognize_obj(obj))
    print(recognize_col(num))
elif len(task.split()) == 2:
    num, obj = task.split()
    print(obj)
elif len(task.split()) == 1:
    com = task
    r = recognize_cmd(com)
    if (r["cmd"] == "add") and (r["percent"] > 50):
        add_obj()

