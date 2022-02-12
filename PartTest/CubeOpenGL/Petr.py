hodnoty = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
TYP = ["C", "S", "D", "H"]

def cardGen():
    karty = dict()
    for typ in TYP:
        for hodnota in hodnoty:
            karty[typ+hodnota] = [hodnota, "Images/"+typ+hodnota+".jpg"]
    
    return karty
    

for key, val in cardGen().items():
    print(key, "-", val)