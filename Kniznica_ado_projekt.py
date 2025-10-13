
import json
from datetime import datetime, timedelta

class Kniha:
    id_counter = 1
    
    def __init__(self, nazov_autora, nazov_knihy, ISBN, rok_vydania, pozicanie, kategoria, zaciatok_vypozicky, koniec_vypozicky):
        self.id = Kniha.id_counter
        Kniha.id_counter +=1
        
        self.nazov_autora = nazov_autora
        self.nazov_knihy = nazov_knihy
        self.ISBN = int(ISBN)
        self.rok_vydania = int(rok_vydania)
        self.pozicanie = pozicanie
        self.kategoria = kategoria
        self.zaciatok_vypozicky = zaciatok_vypozicky
        self.koniec_vypozicky = koniec_vypozicky 

    def __str__(self):
        return f"{self.id}: {self.nazov_autora}: {self.nazov_knihy}, {self.rok_vydania}, {self.pozicanie}, {self.ISBN}, {self.kategoria}, {self.zaciatok_vypozicky} - {self.koniec_vypozicky}"

    def kniha_dict(self):
        return{
            "Meno autora": self.nazov_autora,
            "Názov knihy": self.nazov_knihy,
            "Číslo ISBN": self.ISBN,
            "Rok vydania": self.rok_vydania,
            "Požičaná": self.pozicanie,
            "Kategória": self.kategoria,
            "Dátum vypožičania": self.zaciatok_vypozicky, 
            "Koniec výpožičky": self.koniec_vypozicky 
          }


        
class Clen:
    id_counter = 1
    
    def __init__(self, meno_clena, priezvisko_clena, rok_narodenia, zoznam_pozicanych):
        self.id = Clen.id_counter
        Clen.id_counter += 1
        self.meno_clena = meno_clena
        self.priezvisko_clena = priezvisko_clena
        self.rok_narodenia = rok_narodenia
        self.zoznam_pozicanych = zoznam_pozicanych
        

    def __str__(self):
        return f"{self.id}: {self.meno_clena} {self.priezvisko_clena} {self.rok_narodenia} {self.zoznam_pozicanych}"

    def clen_dict(self):
        return {
            "ID": self.id,
            "Meno": self.meno_clena,
            "Priezvisko": self.priezvisko_clena,
            "Rok_narodenia": self.rok_narodenia,
            "Požičané knihy": self.zoznam_pozicanych
        }
        

class Kniznica:
    
    
    def __init__(self):
        self.knizny_zoznam = []
        self.zoznam_clenov = []
        self.nacitaj_zoznam_clenov()
        self.nacitaj_knizny_zoznam()
        


    def __str__(self):
        return f"{self.knizny_zoznam}"
        return f"{self.zoznam_clenov}"

    def nacitaj_knizny_zoznam(self):
         with open("book.json", "r", encoding = "utf-8") as subor:
            books = json.load(subor)
            for book in books:
                existujuca_kniha = Kniha(book["Meno autora"], book["Názov knihy"], book["Číslo ISBN"], book["Rok vydania"], book["Požičaná"], book["Kategória"], book["Dátum vypožičania"], book["Koniec výpožičky"])
                self.knizny_zoznam.append(existujuca_kniha)
            print("Dáta zo súboru book.json sú načítané.")
  
    
    def vypis_knizny_zoznam(self):
        for kniha in self.knizny_zoznam:
            print(f"\n{kniha}")

    def pridaj_novu_knihu(self):
        print("\nZadaj informácie o knihe: názov autora, názov knihy, ISBN číslo a rok vydania.\n")
        print("Zadaj meno autora: ")
        nazov_autora = input()
        print("Zadaj názov knihy: ")
        nazov_knihy = input()
        print("Zadaj číslo ISBN: (len číslo bez pomlčiek) ")
        ISBN = int(input())

        for kniha in self.knizny_zoznam:
            if kniha.nazov_knihy.lower()== nazov_knihy.lower():
                print(f"Kniha {nazov_knihy} už existuje v zozname")
                return
            if kniha.ISBN == ISBN:
                print(f"Kniha s ISBN {ISBN} už existuje v zozname")
                return
        
        print("Napíš rok vydania knihy: ")
        rok_vydania = input()
        print("Poskytnite informáciu, či je kniha požičana. Ak áno, napíšte Y, ak nie, tak napíšte N")
        pozicanie = input()
        print("Napíšte do akej kategórie kniha patrí: ")
        kategoria = input()
        #print("Zadajte datum pozicania, ak nie je pozicana, tak napiste None")
        zaciatok_vypozicky = None #input()
        koniec_vypozicky = None
        
        nova_kniha = Kniha(nazov_autora, nazov_knihy, ISBN, rok_vydania, pozicanie, kategoria, zaciatok_vypozicky, koniec_vypozicky)
        self.knizny_zoznam.append(nova_kniha)
        print(f"{str(nova_kniha)} \nbola pridaná do knižného zoznamu.")
        #for kniznica in self.knizny_zoznam:
            #print(f" - {kniznica}")

        self.akutalizacia_knizneho_zoznamu()
        
        #kniha_to_dict = []
        #for kniha in self.knizny_zoznam:
         #   data_in_dict = kniha.kniha_dict()
          #  kniha_to_dict.append(data_in_dict)
            
        
    
        #with open ("book.json", "w", encoding = "utf-8") as subor:
         #   json.dump(kniha_to_dict, subor, indent = 4, ensure_ascii = False)

    

       


    def najdi_knihu_nazov_knihy(self):
        hladany = input("\nZadaj názov knihy: ")
        iter = 0
        for kniha in self.knizny_zoznam:
            if kniha.nazov_knihy.lower() == hladany.lower():
                print(f"Kniha bola nájdená: {kniha}")
                iter += 1
                
        if iter == 0:
            print("Knina nie je v zozname!")




    def pozicaj_knihu(self):
        vyber_zo_zoznamu = input("Akú knižku chcete požičať? Napíšte názov knihy: ")


        for vyber in self.knizny_zoznam:
            if vyber.nazov_knihy.lower() == vyber_zo_zoznamu.lower():
                if vyber.pozicanie == "N":
                    print(f"{vyber.id}: {vyber.nazov_knihy} od {vyber.nazov_autora}")

                    pozicanie = input("Chcete požičať túto knihu? (napíšte Y alebo N): ")

                    if pozicanie == "Y":
                        existuje = self.najdi_clena()
                    
                        if existuje == True:
                            id_cloveka = int(input("Zadajte ID člena, ktorý si knihu požičiava: "))
                            for clovek in self.zoznam_clenov:
                               # print(f"vypis {id_cloveka} a {clovek.id}")
                                if id_cloveka == clovek.id:
                                    clovek.zoznam_pozicanych.append(vyber.id)
                                    print("Kniha bola priradená.")

                                    zaciatok_vyp = datetime.now()
                                    koniec_vyp = zaciatok_vyp + timedelta(days = 10)
                                    
                                    vyber.zaciatok_vypozicky = zaciatok_vyp.strftime("%d.%m.%Y")
                                    vyber.koniec_vypozicky = koniec_vyp.strftime("%d.%m.%Y")

                                    self.aktualizacia_zoznamu_clenov()

                                    

                        if vyber.pozicanie == "N":
                            vyber.pozicanie = "Y"
                            #self.knizny_zoznam.append(vyber)
                            print(f"{vyber.nazov_knihy} je úspešne požičaná.")

                        self.akutalizacia_knizneho_zoznamu()
                
                            
                                
                else:
                    print("Kniha je uz pozicana")





    def vratenie_knihy(self):       
        vratka = input("Napíšte názov knihy, ktorú chcete vrátiť: ")
        
        for vyber in self.knizny_zoznam:
            if vyber.nazov_knihy.lower() == vratka.lower():
                if vyber.pozicanie == "Y":
                    print(f"{vyber.id}: {vyber.nazov_knihy} od {vyber.nazov_autora}")

                    pozicanie = input("Chcete vrátiť túto knihu? (napíšte Y alebo N): ")

                    if pozicanie == "Y":
                        existuje = self.najdi_clena()
                    
                        if existuje == True:
                            id_cloveka = int(input("Zadajte ID člena, ktorý knihu vracia: "))
                            for clovek in self.zoznam_clenov:
                                print(f"vypis {id_cloveka} a {clovek.id}")
                                if id_cloveka == clovek.id:
                                    #print(f"{vyber.id}")
                                    print(f"{clovek.zoznam_pozicanych}")
                                    clovek.zoznam_pozicanych.remove(int(vyber.id))
                                    
                                    print("Kniha bola odstránená zo zoznamu.")

                                    self.aktualizacia_zoznamu_clenov()
                                    

                                    if vyber.pozicanie == "Y":
                                        vyber.pozicanie = "N"
                                        vyber.zaciatok_vypozicky = None
                                        vyber.koniec_vypozicky = None
                                        #self.knizny_zoznam.append(vyber)
                                        print(f"{vyber.nazov_knihy} je úspešne vráten´á.")

                                        self.akutalizacia_knizneho_zoznamu()

                                    

                                    break


                                
    def vymaz_knihu_nazov_knihy(self):
        vymaz_knihu = input("Napíš názov knihy, ktorú chcete vymazať: ")

        count = 0
        for meno_knihy in self.knizny_zoznam:
            if  meno_knihy.nazov_knihy.lower()== vymaz_knihu.lower():
                count += 1

                if meno_knihy.pozicanie == "Y":
                    print("Kniha je požičaná. Nemôžete ju vymazať!")
                    return False
                    
                self.knizny_zoznam.remove(meno_knihy)
                print(f"Kniha {vymaz_knihu} bola vymazaná")

        if count == 0:
            print("Táto kniha neexistuje v zozname.")

        self.akutalizacia_knizneho_zoznamu()

            




    def vymaz_knihu_ISBN(self):
        isbn_vymaz = int(input("Napíš číslo ISBN, ktoré chceš vymazať: \nNapíšte len číslo bez pomlčiek: "))
        count = 0
        for isbn in self.knizny_zoznam:
            if isbn.ISBN == isbn_vymaz:
                count += 1

                if isbn.pozicanie == "Y":
                    print("Kniha je požičaná. Nemôžete ju vymazať!")
                    return False
                
                self.knizny_zoznam.remove(isbn)
                print(f"Kniha s ISBN {isbn_vymaz} bola vymazaná")

        if count == 0:
            print("Takéto číslo ISBN neexistuje")

        self.akutalizacia_knizneho_zoznamu()



    def sledovanie_pozicanych(self):
        print("Zoznam požičaných kníh: \n")

        for kniha in self.knizny_zoznam:
            if not (kniha.pozicanie == "N" and
                kniha.koniec_vypozicky == None):
                print(f"{kniha.nazov_autora}\n {kniha.nazov_knihy}\n Dátum vrátenia:{kniha.koniec_vypozicky}\n")
                


    def nacitaj_zoznam_clenov(self):
        with open("data.json", "r", encoding = "utf-8") as subor:
            data = json.load(subor)
            for clen in data:
                existujuci_clen = Clen(clen["Meno"], clen["Priezvisko"], clen["Rok_narodenia"], clen["Požičané knihy"])
                self.zoznam_clenov.append(existujuci_clen)
        print("Dáta zo súboru data.json sú načítané.")

        #for clenovia in self.zoznam_clenov:
            #print(f"{clenovia.zoznam_pozicanych}")
 

    def pridaj_noveho_clena(self):
        print("Poskytnite informácie o novom členovi pre zápis: ")
        meno_clena = input("Napíš meno nového člena: ")
        priezvisko_clena = input("Napíš priezvisko nového člena: ")
        rok_narodenia = int(input("Napíš rok narodenia: "))
        zoznam_pozicanych = []
        
        novy_clen = Clen(meno_clena, priezvisko_clena, rok_narodenia, zoznam_pozicanych)
        
        for clen in self.zoznam_clenov:
            if (clen.meno_clena.lower() == meno_clena.lower() and
                clen.priezvisko_clena.lower() == priezvisko_clena.lower() and
                clen.rok_narodenia == rok_narodenia):
                print(f"Tento člen {meno_clena} {priezvisko_clena} {rok_narodenia} už existuje v zozname.")
                return
        
        self.zoznam_clenov.append(novy_clen)

        self.aktualizacia_zoznamu_clenov()

            
        print(f"\nNový člen {meno_clena} {priezvisko_clena} je pridaný.\n")
        print("Údaje boli pridané do súboru data.json.\n")

        return True


    def vypis_zoznam(self):
        for osoba in self.zoznam_clenov:
            print(f"{osoba}")
        


    def najdi_clena(self):
        hladany_clen = input("\nZadaj meno člena: ")
        
        count = 0
        for osoba in self.zoznam_clenov:
            if osoba.meno_clena.lower() == hladany_clen.lower():
                print(f"Člen bol nájdený: {osoba.id}: {osoba.meno_clena} {osoba.priezvisko_clena}")
                count += 1   
            
        if count == 0:
            print("Člen nie je v zozname!")
            return False
        
        else:
           return True 


    def najdi_clena_podla_priezviska(self):
        hladany_clen = input("\nNapíš priezvisko hladaného: ")
        count = 0
        for osoba in self.zoznam_clenov:
            if osoba.priezvisko_clena.lower() == hladany_clen.lower():
                print(f"Člen bol nájdený: {osoba.id} {osoba.meno_clena} {osoba.priezvisko_clena}")
                count += 1
        
        if count == 0:
            print("člen s týmto priezviskom sa nenachádza v zozname.")
        return


    def vymaz_clena(self):
        odstranit = int(input("\nZadajte ID/číslo člena, ktorého chcete vymazať: "))
        potvrdenie = input(f"\nNaozaj chcete vymazať člena s ID {odstranit}? Ak áno stlačte Y, ak nie stlačte N: ")
        
        if potvrdenie == "Y":
            count = 0
            for number in self.zoznam_clenov:
                if number.id == odstranit:
                    count += 1
                    break
                
            if count > 0:
                for clen in self.zoznam_clenov:
                    if clen.id == odstranit:
                        if clen.zoznam_pozicanych:
                            print(f"Člen má stále požičané knihy (ID kníh: {clen.zoznam_pozicanych})")
                            print("Najprv je potrebné vrátiť všetky požičané knihy.")
                            return False
                        
                        self.zoznam_clenov.remove(clen)
                        print("Člen bol vymazaný.")

                        self.aktualizacia_zoznamu_clenov()


            else:
                print("Člen s týmto ID neexistuje.")
                    
        else:
            print("Člen bol ponechaný v zozname.")


    def zobrazit_knihy_clen(self):
        print("Pre zobrazenie kníh, ktoré má člen požičané zadaj ID člena: ")
        try:
            ID_clen = int(input())

            for clen in self.zoznam_clenov:
                if clen.id == ID_clen:
                    if not clen.zoznam_pozicanych:
                        print(f"{clen.meno_clena} {clen.priezvisko_clena} nemá požičané žiadne knihy.")
                        return
                
                print(f"Knihy požičané členom {clen.meno_clena} {clen.priezvisko_clena}: ")
                for id_knihy in clen.zoznam_pozicanych:
                    for kniha in self.knizny_zoznam:
                        if kniha.id == id_knihy:
                            print(f"{kniha. nazov_autora} \n{kniha.nazov_knihy} \n{kniha.zaciatok_vypozicky} {kniha.koniec_vypozicky}\n")
                return
                    
            print(f"Člen s ID {ID_clen} nebol nájdený.")
            
        except ValueError:
            print("Neplatné ID! Zadajte číslo.")

    def akutalizacia_knizneho_zoznamu(self):
        kniha_to_dict = []
        for kniha in self.knizny_zoznam:
            data_in_dict = kniha.kniha_dict()
            kniha_to_dict.append(data_in_dict)
            
    
        with open ("book.json", "w", encoding = "utf-8") as subor:
            json.dump(kniha_to_dict, subor, indent = 4, ensure_ascii = False)


    def aktualizacia_zoznamu_clenov(self):
        clen_to_dict = []
        for person in self.zoznam_clenov:
            data_in_dict = person.clen_dict()
            clen_to_dict.append(data_in_dict)
            
        #[person.clen_dict() for person in self.zoznam_clenov] - kratsi zapis for cyklu
    
        with open ("data.json", "w", encoding = "utf-8") as subor:
            json.dump(clen_to_dict, subor, indent = 4, ensure_ascii = False)




def menu():
        
        print("\n|======================================================================|")
        print("|                      Vitajte v knižnici                              |")
        print("|======================================================================|")
        print("|                                                                      |")
        print("|1. Pridať novú knihu              8. Pridať nového člena              |")
        print("|                                                                      |")
        print("|2. Zobraziť zoznam kníh           9. Zobraziť zoznam členov           |")
        print("|                                                                      |")
        print("|3. Požičať knihu                  10. Nájsť člena podľa mena          |")
        print("|                                                                      |")
        print("|4. Vrátiť knihu                   11. Nájsť člena podľa priezviska    |")
        print("|                                                                      |")
        print("|5. Vymazať Knihu podľa ISBN       12. Vymazať člena                   |")
        print("|                                                                      |")
        print("|6. Vymazať knihu podľa názvu      13. Sledovanie požičaných kníh      |")
        print("|                                                                      |")
        print("|7. Vyhľadať knihu podľa názvu     14. Zobraziť členové knihy          |")
        print("|                                                                      |")
        print("|======================================================================|")
        print("|                          e. koniec                                   |")
        print("|======================================================================|")


def spusti_program():
    kniznica = Kniznica()

    while True:
            
        menu()
        volba = input("\nVyberte možnosť (1-14): ")

        match volba:
                
                case "1":
                    kniznica.pridaj_novu_knihu()

                case "2":
                    kniznica.vypis_knizny_zoznam()

                case "3":
                    kniznica.vypis_knizny_zoznam()
                    kniznica.vypis_zoznam()
                    kniznica.pozicaj_knihu()
                    
                case "4":
                    kniznica.vypis_knizny_zoznam()
                    kniznica.vypis_zoznam()
                    kniznica.vratenie_knihy()

                case "5":
                    kniznica.vypis_knizny_zoznam()
                    kniznica.vymaz_knihu_ISBN()

                case "6":
                    kniznica.vypis_knizny_zoznam()
                    kniznica.vymaz_knihu_nazov_knihy()

                case "7":
                    kniznica.najdi_knihu_nazov_knihy()

                case "8":
                    kniznica.pridaj_noveho_clena()

                case "9":
                    kniznica.vypis_zoznam()

                case "10":
                    kniznica.najdi_clena()

                case "11":
                    kniznica.najdi_clena_podla_priezviska()

                case "12":
                    kniznica.vypis_zoznam()
                    kniznica.vymaz_clena()

                case "13":
                    kniznica.sledovanie_pozicanych()

                case "14":
                    kniznica.vypis_zoznam()
                    kniznica.zobrazit_knihy_clen()

                case "e":
                    print("Ukončili ste program.")
                    break

                case _:
                    print("Zadali ste neplatnú voľbu. Skúste ešte raz.")




if __name__ == '__main__': 
    print("Script is running")

    spusti_program()
    




     









