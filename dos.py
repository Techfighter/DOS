import copy
import os.path
import glob
from datetime import datetime
from time import localtime
import random
import re

# BUG: Aucun connue
run = 1

"""
AMELIORATION DU SCRIPTE:
1) Vous pouvez choisir l'emplacement de départ sur l'ordinateur.
   Il début par default sur la clé USB répertoir python si vous faite enter.
2) Tout les fichiers apparaisent et un inventaire des type de fichier en plus.
   Les fichier sont classable horizontalement ou verticalement page par page.
3) Vous ouvrez le fichier en écrivant son nom et en sortez avec .close
   Le contenu des fichiers sont révélé ligne par ligne avec numérotation.
4) Vous avez le choix d'ajouté ou effacé une ligne ou vous voulez et sauvegardé.
   Taper .#(num ligne) pour inserér une ligne ou ..#(num ligne) pour effacé.
   Taper .##(num ligne) pour remplacé une ligne par une autre a l'emplacement.
   Taper .. pour effacé la derniere ligne du fichier ou >(text) pour y écrir.
5) Les commandes spécial sont précédé d'un (.) Ex: .AIDE, .QUIT .RETURN .DEL
"""

def remove_EOF():
    global sourcefile, testline, test, file, line
    testline = 0
    file = open(Rep + sourcefile, "r")
    for line in file: #mesure le nombre de ligne
        testline = testline + 1
    file.close()
    if (testline > 1):
        test = 0
        file = open(Rep + sourcefile, "r")
        for line in file:
            if (test < (testline - 1)): #reecrit tout le fichier moins la derniere ligne
                file = open(Rep + sourcefile + ".tmp", "a")
                file.write(line[:-1] + "\n")
                file.close()
            test = test + 1
        file.close()
        #kill fichier origine
        os.remove(Rep + sourcefile)
        file = open(Rep + sourcefile + ".tmp", "r")
        for line in file:
            #reecrit tout le fichier tmp dans le fichier d'origine
            file = open(Rep + sourcefile, "a")
            file.write(line[:-1] + "\n")
            file.close()
        file.close()
        #kill fichier tmp
        os.remove(Rep + sourcefile + ".tmp")
    else:
        #kill fichier origine
        os.remove(Rep + sourcefile)
        #Recré nouveau fichier vide au même nom
        file = open(Rep + sourcefile, "a")
        file.close()
            
#Scr 22x80
tabulation = "                          "
repertoir = []
Rep = input("File Locat >")
edit = 0
if (Rep == "" or Rep == "?"):
    Rep = 'E:/PERSONNEL/python_2/python/'
    repertoir = os.listdir(Rep)
while(run == 1):
    #repertoir = os.listdir(Rep)
    while (os.path.exists(Rep) == True):
        directory = 0
        inventaire = 0
        edit = 0
        rep = 0
        exe = 0
        docx = 0
        txt = 0
        pdf = 0
        jpg = 0
        png = 0
        gif = 0
        py = 0
        mix = 0
        msi = 0
        fld = 0
        print(Rep)
        for x in repertoir:
            rep = rep + 1
            #Verrfie Extension
            for i in range(len(repertoir[rep - 1])):
                if (repertoir[rep - 1][i - 1].upper() == "."):
                    #Identification fichier
                    if (repertoir[rep - 1][i:].upper() == "EXE"):
                        exe = exe + 1
                    if (repertoir[rep - 1][i:].upper() == "DOCX"):
                        docx = docx + 1
                    if (repertoir[rep - 1][i:].upper() == "TXT"):
                        txt = txt + 1
                    if (repertoir[rep - 1][i:].upper() == "PDF"):
                        pdf = pdf + 1
                    if (repertoir[rep - 1][i:].upper() == "JPG"):
                        jpg = jpg + 1
                    if (repertoir[rep - 1][i:].upper() == "PNG"):
                        png = png + 1
                    if (repertoir[rep - 1][i:].upper() == "GIF"):
                        gif = gif + 1
                    if (repertoir[rep - 1][i:].upper() == "PY"):
                        py = py + 1
                    if (repertoir[rep - 1][i:].upper() == "MIX"):
                        mix = mix + 1
                    if (repertoir[rep - 1][i:].upper() == "MSI"):
                        msi = msi + 1
                fld = rep - (exe + docx + txt + pdf + jpg + png + gif + py + msi + mix)
            if (directory == 1):
                print(repertoir[rep - 1].upper())
                if ((rep / 22) == int(rep / 22)):
                    key = input("   (ENTER SUITE.)")
        if (directory == 0):
            for x in range(int(rep / 2.9)):
                y = 3 * x
                if ((rep - y) > 2):
                    print(repertoir[y - 2][0:26],tabulation[0:26 - len(repertoir[y - 2][0:26])],repertoir[y - 1][0:26],tabulation[0:26 - len(repertoir[y - 1][0:26])],repertoir[y][0:26])
                else:
                    if (int(3 * ((rep / 3) - int(rep / 3))) == 2):
                        print(repertoir[y - 2][0:26],tabulation[0:26 - len(repertoir[y - 2][0:26])],repertoir[y - 1][0:26])
                    if (int(3 * ((rep / 3) - int(rep / 3))) == 1):
                        print(repertoir[y - 2][0:26])

        print(rep, "element trouve.")
        if (inventaire == 1):
            print("fld(",fld,"),exe(",exe,"),docx(",docx,"),txt(",txt,"),pdf(",pdf,"),jpg(",jpg,"),png(",png,"),gif(",gif,"),py(",py,"),msi(",msi,"),mix(",mix,")")
        sourcefile = input("Ouvrir >")
        if (sourcefile == ""):
            sourcefile = "TEXT" #Ouvre ou Créer un TEXT a cette emplacement
        #Quit
        if (sourcefile[0:5].upper() == ".QUIT" or sourcefile[0:7].upper() == ".SORTIE" or sourcefile[0:8].upper() == ".QUITTER" or sourcefile[0:8].upper() == ".EXIT"):
            edit = 0
            rep = 0
            run = 0
            break
            exit()
        #kill fichier
        if (sourcefile[0:4].upper() == ".DEL" or sourcefile[0:5].upper() == ".KILL"):
            Xfile = input("Name_File >")
            if (os.path.exists(Rep + Xfile) == True):
                os.remove(Xfile)
            else:
                print("No File Name",Xfile)
            edit = 0
            rep = 0
            break
        #Aide premiere couche
        if (sourcefile[0:5].upper() == ".AIDE" or sourcefile[0:5].upper() == ".HELP"):
            print("LES COMMANDES:")
            print("{.LOCATE CD CD..} {.QUIT .EXIT} {.AIDE .HELP} {.DEL .KILL} del file")
            print("")
            edit = 0
            rep = 0
            break
        #Accédé a n'importequel doccier
        if (sourcefile[0:7].upper() == ".LOCATE" or sourcefile[0:7] == ".FOLDER"):
            rep_loc = input("FILE LOCATION >")
            if (os.path.exists(rep_loc) == True):
                Rep = rep_loc
                repertoir = os.listdir(Rep)
            edit = 0
            rep = 0
            print("")
            break
        #Revenir precedent doccier
        if (sourcefile[0:4].upper() == "CD.." or sourcefile[0:2] == ".."):
            REP = Rep[:-1].split("/")
            REP.pop(-1)
            Rep = "/".join(REP) + "/"
            repertoir = os.listdir(Rep)
            edit = 0
            rep = 0
            print("")
            break
        #Acceder doccier 
        if (sourcefile[0:3].upper() == "CD "):
            if (os.path.exists(Rep + sourcefile[3:]) == True):
                #Ajouté une routinne vérrfie si le nom existe.
                Rep = Rep + sourcefile[3:] + '/'
                repertoir = os.listdir(Rep)
                edit = 0
                rep = 0
                print("")
                break
            else:
                Rep = input("Nom Repertoire > ")
                #Ajouté une routinne vérrfie si le nom existe.
                if (os.path.exists(Rep + sourcefile[3:]) == False):
                    print("(Erreur Folder Name!)")
                    edit = 0
                    rep = 0
                    print("")
                    break
                else:
                    Rep = Rep + sourcefile[3:] + '/'
                    repertoir = os.listdir(Rep)
                    edit = 0
                    rep = 0
                    print("")
                    break
        edit = 1
        print(Rep + sourcefile)
        #repertoir = os.listdir(Rep)
        file = open(Rep + sourcefile, "a")
        file.close()
        #crée un fichier ou ajoute une ligne a la suite sans effacer
        print("")

        while (edit == 1):
            #repertoir = os.listdir(Rep)
            #affiche tout se qui se trouve dans le fichier
            lab = 0
            print(sourcefile,"(Début Fichier) {")
            file = open(Rep + sourcefile.upper(), "r")
            for line in file:
                lab = lab + 1 #Ajoute une identification numérique a chaque ligne du fichier. 1#:_[ligne code]
                print(lab,"#: ",line[:-1]) #:-1 filtre les changement de ligne
                if ((rep/22) == int(rep/22)):
                    key = input("   (ENTER SUITE.)")
            file.close()
            print("} (Fin du Fichier)")
            print("")

            #Edition avancer
            key = input("New line >")
            insert = 1
            if (key[0:2] == ".#"):
                #Ajoute une ligne au milieu du fichier
                if (int(len(key[2:]) >= 1)):
                    if (key[2] == "#"): #désactive insert Remplace Ligne
                        print("Remplace line")
                        insert = 0
                    else:
                        insert = 1 #Auto insert
                    if (int(len(key[3:]) >= 1) and (key[3:].isdigit() == True)):
                        Line = int(key[3:])
                    else:
                        Line = input("#line: ")
                        if (Line.isdigit() == True):
                            Line = int(Line)
                        else:
                            print("(Erreur!)")
                    if (key[2:].isdigit() == True):
                        Line = int(key[2:])
                else:
                    Line = input("#line: ")
                    if (Line.isdigit() == True):
                        Line = int(Line)
                    else:
                        print("(Erreur!)")                
                Xline = input("? > ")
                testline = 0
                file = open(Rep + sourcefile.upper(), "r")
                for line in file: #mesure le nombre de ligne
                    testline = testline + 1
                file.close()
                #Verrifie si le ligne est possible!!!
                if (Line <= testline):
                    test = 0
                    file = open(Rep + sourcefile.upper(), "r")
                    for line in file:
                        if (test == (Line - 1)):
                            #Quand la ligne indiqué arrive
                            file = open(Rep + sourcefile + ".tmp".upper(), "a")
                            file.write(Xline + "\n")
                            file.close()
                            if (insert == 1):
                                #incluant la ligne remplacé
                                file = open(Rep + sourcefile + ".tmp".upper(), "a")
                                file.write(line[:-1] + "\n")
                                file.close()
                                test = test + 1
                        else:
                            #reecrit tout le fichier jusqu'a la ligne indiqué
                            file = open(Rep + sourcefile + ".tmp".upper(), "a")
                            file.write(line[:-1] + "\n")
                            file.close()
                        test = test + 1
                    file.close()
                    #kill fichier origine
                    os.remove(Rep + sourcefile)
                    file = open(Rep + sourcefile + ".tmp".upper(), "r")
                    for line in file:
                        #reecrit tout le fichier tmp dans le fichier d'origine
                        file = open(Rep + sourcefile.upper(), "a")
                        file.write(line[:-1] + "\n")
                        file.close()
                    file.close()
                    #kill fichier tmp
                    os.remove(Rep + sourcefile + ".tmp")
                else:
                    #Si la ligne ajouté est sortie de la structure du fichier
                    print("(Edition Hore Range!)")
                    qt = input("Correction at EOF? [Oui/Non]")
                    if (qt.upper() == "OUI" or qt.upper() == "O" or qt.upper() == "YES" or qt.upper() == "Y" or qt.upper() == ""):
                        file = open(Rep + sourcefile.upper(), "r")
                        for line in file:
                            if (test < (testline - 1)): #reecrit tout le fichier moins la derniere ligne
                                file = open(Rep + sourcefile + ".tmp".upper(), "a")
                                file.write(line[:-1] + "\n")
                                file.close()
                            test = test + 1
                        file.close()
                        #kill fichier origine
                        os.remove(Rep + sourcefile)
                        file = open(Rep + sourcefile + ".tmp".upper(), "r")
                        for line in file:
                            #reecrit tout le fichier tmp dans le fichier d'origine
                            file = open(Rep + sourcefile.upper(), "a")
                            file.write(line[:-1] + "\n")
                            file.close()
                        file.close()
                        #kill fichier tmp
                        os.remove(sourcefile + ".tmp")
                    else:    
                        #Ajoute une ligne a la suite dans le fichier
                        file = open(Rep + sourcefile.upper(), "a")
                        if (key.upper() == "" or key.upper() == ".." or key[0:2].upper() == ".#" or key[0:3].upper() == ".#" or key.upper() == ".DEL" or key.upper() == ".AIDE" or key.upper() == ".ETAPE" or key.upper() == ".SEQUENCE" or key.upper() == ".BLOCK" or key.upper() == ".DOUBLE" or key.upper() == ".PUZZLE" or key.upper() == ".CHAPITRE" or key.upper() == ".CHAP" or key.upper() == ".FIN" or key.upper() == ".CHOIX" or key.upper() == ".SEQUENCE" or key.upper() == ".COND" or key.upper() == ".COND=" or key.upper() == ".COND>" or key.upper() == ".COND<" or key.upper() == ".VAR" or key.upper() == ".VAR>" or key.upper() == ".VAR<"):
                            print(" ")
                        else:
                            file.write(key + "\n")
                        file.close()
                    #print("(Auto SAVE)")
                    print("")

            if (key == ".."):
                #Efface un ligne a la fin du fichier
                remove_EOF()
            else:    
                #Ajoute une ligne a la suite dans le fichier
                file = open(Rep + sourcefile.upper(), "a")
                if (key.upper() == "" or key.upper() == ".." or key[0:2].upper() == ".#" or key[0:3].upper() == "..#" or key.upper() == ".DEL" or key.upper() == ".AIDE" or key.upper() == ".ETAPE" or key.upper() == ".SEQUENCE" or key.upper() == ".BLOCK" or key.upper() == ".DOUBLE" or key.upper() == ".PUZZLE" or key.upper() == ".CHAPITRE" or key.upper() == ".CHAP" or key.upper() == ".FIN" or key.upper() == ".CHOIX" or key.upper() == ".SEQUENCE" or key.upper() == ".COND" or key.upper() == ".COND=" or key.upper() == ".COND>" or key.upper() == ".COND<" or key.upper() == ".VAR" or key.upper() == ".VAR>" or key.upper() == ".VAR<"):
                    print(" ")
                else:
                    file.write(key + "\n")
                file.close()
            #print("(Auto SAVE)")
            print("")
            
            if (key[0:3] == "..#"):
                #Efface une ligne au milieu du fichier
                if (int(len(key[3:]) >= 1) and (key[3:].isdigit() == True)):
                    Line = int(key[3:])
                else:
                    Line = int(input("#line: "))
                testline = 0
                file = open(Rep + sourcefile.upper(), "r")
                for line in file: #mesure le nombre de ligne
                    testline = testline + 1
                file.close()
                if (testline > 1):
                    #Verrifie si la ligne est possible!!!
                    if (Line <= testline):
                        test = 0
                        file = open(Rep + sourcefile.upper(), "r")
                        for line in file:
                            if (test == (Line - 1)):
                                #Quand la ligne indiqué arrive
                                file = open(Rep + sourcefile + ".tmp".upper(), "a")
                                file.close()
                            else:
                                #reécrit tout le fichier jusqu'a la ligne indiqué
                                file = open(Rep + sourcefile + ".tmp".upper(), "a")
                                file.write(line[:-1] + "\n")
                                file.close()
                            test = test + 1
                        file.close()
                        #kill fichier origine
                        os.remove(Rep + sourcefile)
                        file = open(Rep + sourcefile + ".tmp".upper(), "r")
                        for line in file:
                            #reecrit tout le fichier tmp dans le fichier d'origine
                            file = open(Rep + sourcefile.upper(), "a")
                            file.write(line[:-1] + "\n")
                            file.close()
                        file.close()
                        #kill fichier tmp
                        os.remove(Rep + sourcefile + ".tmp")
                else:
                    #kill fichier origine
                    os.remove(Rep + sourcefile)
                    #Recré nouveau fichier vide au même nom
                    file = open(Rep + sourcefile.upper(), "a")
                    file.close()

            #kill fichier
            if (key[0:4].upper() == ".DEL" or key[0:5].upper() == ".KILL"):
                Xfile = input("Name_File >")
                remove_EOF()
                file.close()
                if (os.path.exists(Rep + Xfile) == True):
                    os.remove(Xfile)
                    edit = 0 #?
                    rep = 0
                break

            #Return
            if (key[0:6].upper() == ".CLOSE" or key[0:4].upper() == ".END" or key[0:7].upper() == ".RETURN"  or key[0:5].upper() == ".LOAD" or key[0:5].upper() == ".OPEN"):
                edit = 0
                rep = 0
                if (os.path.exists(Rep + sourcefile) == True):
                    remove_EOF()
                break
                
            #Quit
            if (key[0:5].upper() == ".QUIT" or key[0:7].upper() == ".SORTIE" or key[0:8].upper() == ".QUITTER" or key[0:8].upper() == ".EXIT"):
                if (os.path.exists(Rep + sourcefile) == True):
                    remove_EOF()
                edit = 0
                rep = 0
                run = 0
                break
                exit()

            #Aide
            if (key[0:5].upper() == ".AIDE" or key[0:5].upper() == ".HELP"):
                print("LES COMMANDES:")
                print("{.QUIT .EXIT} {.AIDE .HELP} {.DEL .KILL} del file, {.LOAD .ClOSE .END .RETURN}")
                print("{..} Del last line, {.#} Insert on line, {.##} Remplace on line, {..#} Remove")
                print(Rep)
                if (os.path.exists(Rep + sourcefile) == True):
                    remove_EOF()
                edit = 0
                rep = 0
