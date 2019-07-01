from fuzzywuzzy import fuzz
def add_obj():
    obj = input("Enter object class: ")
    keys = input("Enter oject names(at least 2): ").split()
    with open("objects.txt", "a") as f:
        f.write(obj+" ")
        for i in keys:
            f.write(i+" ")
        f.write("\n")
def get_obj():
    with open("objects.txt", "r") as f:
        objs = {}
        k = f.read().splitlines()
        for i in k:
            x = i.split()
            objs[x[0]] = (x[1::])
    return objs
