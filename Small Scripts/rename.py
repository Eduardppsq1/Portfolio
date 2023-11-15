import os

path = r"C:\Users\Example\Desktop\Director_rename"
os.chdir(path)
fisiere = os.listdir(path)
for fisier in fisiere:
    nume_nou = ""
    for i in range(len(fisier.split())):
        if i == 2:
            nume_nou += fisier.split()[i][1:] + " "
        else:
            nume_nou += fisier.split()[i] + " "
    os.rename(fisier, nume_nou)
