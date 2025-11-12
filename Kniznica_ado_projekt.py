
import json
from datetime import datetime, timedelta


class KniznicnyZaznam:

    def __init__(self, id = None):
        if id is not None:
            self.id = id
        else:
            self.id = self.__class__.id_counter
            self.__class__.id_counter += 1

    @classmethod
    def nacitaj_id(cls):
        try:
            with open(cls.ID_CONF_FILE, 'r', encoding = "utf-8") as f:
                uni_data = json.load(f)
                cls.id_counter = uni_data.get('last_id',1)
        except(FileNotFoundError, json.JSONDecodeError):
            cls.id_counter = 1

    @classmethod
    def uloz_id(cls):
        with open(cls.ID_CONF_FILE, 'w', encoding = "utf-8") as f:
            json.dump({'last_id': cls.id_counter}, f)
            
    @classmethod
    def nacitaj_zoznamy(cls, subor_path, zoznam, vytvor_objekt):
        with open(subor_path, "r", encoding = "utf-8") as subor:
            data = json.load(subor)
            
            max_id = 0
            print(f"\nNačítavam záznamy z {subor_path}")

            for zaznam in data:
                novy_objekt = vytvor_objekt(**zaznam)
                zoznam.append(novy_objekt)
            

                if novy_objekt.id > max_id:
                    max_id = novy_objekt.id
                    
            vytvor_objekt.id_counter = max_id + 1
            print(f"nacitany zaznam")


class Kniha(KniznicnyZaznam):

    id_counter = 1
    ID_CONF_FILE = 'kniha_id.json'
    
    def __init__(self, nazov_autora, nazov_knihy, ISBN, rok_vydania, kategoria, pozicanie = False, zaciatok_vypozicky = None, koniec_vypozicky = None, id = None):
        
        super().__init__(id)

        
        self.nazov_autora = nazov_autora
        self.nazov_knihy = nazov_knihy
        self.ISBN = int(ISBN)
        self.rok_vydania = int(rok_vydania)
        self.pozicanie = pozicanie
        self.kategoria = kategoria
        self.zaciatok_vypozicky = zaciatok_vypozicky
        self.koniec_vypozicky = koniec_vypozicky

    
    def je_k_dispo(self):
        return not self.pozicanie

    def oznac_ako_pozicanu(self):
        self.pozicanie = True
        self.zaciatok_vypozicky = datetime.now().strftime("%d.%m.%Y")
        koniec = datetime.strptime(self.zaciatok_vypozicky, "%d.%m.%Y") + timedelta(days = 10)
        self.koniec_vypozicky = koniec.strftime("%d.%m.%Y")

    def oznac_ako_vratenu(self):
        self.pozicanie = False
        self.zaciatok_vypozicky = None
        self.koniec_vypozicky = None
            

    def __str__(self):
        return (f"ID:{self.id:2d}. {self.nazov_autora:<25}"
                f"{self.nazov_knihy:<34}"
                f"{self.rok_vydania:<10}"
                f"{self.ISBN:<23}"
                f"{'Pozicana' if self.pozicanie else 'Dostupna':<8}"
                f"{f' do: {self.koniec_vypozicky}' if self.pozicanie else '':<20}"
                f"{self.kategoria:<10}"
                )


        
class Clen(KniznicnyZaznam):
    id_counter = 1
    ID_CONF_FILE = 'clen_id.json'
    
    def __init__(self, meno_clena, priezvisko_clena, rok_narodenia, zoznam_pozicanych = None, id = None):

        super().__init__(id)

        self.meno_clena = meno_clena
        self.priezvisko_clena = priezvisko_clena
        self.rok_narodenia = rok_narodenia
        self.zoznam_pozicanych = zoznam_pozicanych if zoznam_pozicanych is not None else []
        

    def __str__(self):
        return f"{self.id}: {self.meno_clena} {self.priezvisko_clena} {self.rok_narodenia} {self.zoznam_pozicanych}"

    def pozicaj_si_knihu(self, kniha_id):
        self.zoznam_pozicanych.append(kniha_id)

    def vrat_knihu(self, kniha_id):
        if kniha_id in self.zoznam_pozicanych:
            self.zoznam_pozicanych.remove(kniha_id)
            return True
        return False
    
        

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
        KniznicnyZaznam.nacitaj_zoznamy(
            subor_path = "book.json",
            zoznam = self.knizny_zoznam,
            vytvor_objekt = Kniha
            )
              
             
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
        print("Napíšte do akej kategórie kniha patrí: ")
        kategoria = input()
       
        
        nova_kniha = Kniha(nazov_autora, nazov_knihy, ISBN, rok_vydania, kategoria)
        self.knizny_zoznam.append(nova_kniha)
        print(f"{str(nova_kniha)} \nbola pridaná do knižného zoznamu.")
        

        self.akutalizacia_knizneho_zoznamu()
        
        
                   


    def najdi_knihu_nazov_knihy(self):
        return self.najdi(
            zoznam = self.knizny_zoznam,
            atribut = "nazov_knihy",
            nazov_objektu = "kniha"
        )



    def pozicaj_knihu(self):
        kniha = self.najdi_knihu_nazov_knihy()
        if not kniha:
            return False

        kniha = kniha[0]
        if kniha.pozicanie:
            print("Kniha je uz pozicana.")
            return False

        clenovia = self.najdi_clena()
        if not clenovia:
            return False
        
        if len(clenovia) > 1:
            try:
                id_clena = int(input("\nZadajte ID clena, ktory si knihu poziciava: "))
                clen = self.najdi_clena_podla_id(id_clena)
                
            except ValueError:
                print("Neplatne ID clena.")
                return False
        else:
            clen = clenovia[0]

        kniha.oznac_ako_pozicanu()
        clen.pozicaj_si_knihu(kniha.id)
        
        self.aktualizacia_zoznamu_clenov()
        self.akutalizacia_knizneho_zoznamu()

        print(f"Kniha {kniha.nazov_knihy} bola uspesne pozicana clenom {clen.meno_clena} {clen.priezvisko_clena}.")
        return True
        

    def vratenie_knihy(self):       
        #vratka = input("Napíšte názov knihy, ktorú chcete vrátiť: ")
        knihy = self.najdi_knihu_nazov_knihy()

        if not knihy:
            print("Kniha nebola najdena.")
            return False
        kniha = knihy[0]
        
        if not kniha.pozicanie:
            print("Tato kniha nie je pozicana.")
            return False

        print(f"{kniha.id}: {kniha.nazov_knihy} od {kniha.nazov_autora}")
        
        if not self.potvrdit_volbu(f"Chcete vratit tuto knihu '{kniha.nazov_knihy}'? (Y/N): "):
            return False

        try:
            id_clena = int(input("Zadajte ID clena, ktory knihu vracia: "))
            clen = self.najdi_clena_podla_id(id_clena)

            if not clen:
                print("Clen  s tymto ID neexistuje")
                return False

            if clen.vrat_knihu(kniha.id):
                kniha.oznac_ako_vratenu()

                self.aktualizacia_zoznamu_clenov()
                self.akutalizacia_knizneho_zoznamu()

                print(f"{kniha.nazov_knihy} bola uspesne vratena.")
                return True
            else:
                print("Tato kniha nie je pozicana tymto clenom.")
                return False
            
        except ValueError:
            print("Neplatne ID clena.")
            return False
            
    
                                
    def vymaz(self, atribut, konverzia = None):

        text_vyzvy = f"Napis {atribut.replace('_', ' ')}, ktory chces vymazat: "
        hodnota = input(text_vyzvy)

        if konverzia:
            try:
                hodnota = konverzia(hodnota)
            except ValueError:
                print(f"Neplatny format pre  {atribut}")
                return False
            
        
        for kniha in self.knizny_zoznam[:]:
            if getattr(kniha, atribut) == hodnota:   
                if kniha.pozicanie:
                    print(f"Kniha je pozicana. Nemozete knihu vymazat!")
                    return False
                
                print(f"\nNasla sa kniha: {kniha}")
                if not self.potvrdit_volbu(f"Naozaj chcete vymazat tuto knihu? (Y/N)"):
                    print("vymazanie knihy bolo zrusene.")
                    return False
                
                self.knizny_zoznam.remove(kniha)
                self.akutalizacia_knizneho_zoznamu()
                print(f"Kniha s {atribut} = {hodnota} bola vymazana.")
                return True
            
       
        print(f"Kniha {atribut} neexistuje v zozname.")
        return False     
            

                                
    def vymaz_knihu_nazov_knihy(self):
        return self.vymaz("nazov_knihy")




    def vymaz_knihu_ISBN(self):
        return self.vymaz("ISBN", konverzia = int)


    def sledovanie_pozicanych(self):
        print("Zoznam požičaných kníh: \n")

        for kniha in self.knizny_zoznam:
           if kniha.pozicanie == True:
            print(f"{kniha.id:2d}.{''} {kniha.nazov_autora}\n "
                  f"   {kniha.nazov_knihy}\n"
                  f"    Dátum vrátenia: {kniha.koniec_vypozicky}\n")


    def nacitaj_zoznam_clenov(self):
        KniznicnyZaznam.nacitaj_zoznamy(
            subor_path = "data.json",
            zoznam = self.zoznam_clenov,
            vytvor_objekt = Clen
            )
        
 

    def pridaj_noveho_clena(self):
        print("Poskytnite informácie o novom členovi pre zápis: ")
        meno_clena = input("Napíš meno nového člena: ")
        priezvisko_clena = input("Napíš priezvisko nového člena: ")
        rok_narodenia = int(input("Napíš rok narodenia: "))
        zoznam_pozicanych = []
        
        novy_clen = Clen(meno_clena, priezvisko_clena, rok_narodenia)
        
        for clen in self.zoznam_clenov:
            if (clen.meno_clena.lower() == meno_clena.lower() and
                clen.priezvisko_clena.lower() == priezvisko_clena.lower() and
                clen.rok_narodenia == rok_narodenia):
                print(f"Tento člen {meno_clena} {priezvisko_clena} {rok_narodenia} už existuje v zozname.")
                return
        
        self.zoznam_clenov.append(novy_clen)

        self.aktualizacia_zoznamu_clenov()

            
        print(f"\nNový člen {novy_clen.id} {meno_clena} {priezvisko_clena} je pridaný.\n")
        print("Údaje boli pridané do súboru data.json.\n")

        return True


    def vypis_zoznam(self):
        for osoba in self.zoznam_clenov:
            print(f"{osoba}")
        


    def najdi(self, zoznam, atribut, nazov_objektu = "zaznam"):
        text_vyzvy = f"\nZadaj {atribut.replace('_', ' ')}: "
        hladana_hodnota = input(text_vyzvy)
        najdeny = []

        for objekt in zoznam:
           if getattr(objekt, atribut).lower() == hladana_hodnota.lower():
               print(f"{nazov_objektu.capitalize()} bol najdeny: {objekt}")
               najdeny.append(objekt)
               
               #return objekt

        if not najdeny:
            print(f"{nazov_objektu.capitalize()} sa nenachadza v zozname.")
            return []
        
        return najdeny
        

    def najdi_clena(self):
         return self.najdi(
             zoznam = self.zoznam_clenov,
             atribut = "meno_clena",
             nazov_objektu = "osoba"
         )


    def najdi_clena_podla_priezviska(self):
        return self.najdi(
            zoznam = self.zoznam_clenov,
            atribut = "priezvisko_clena",
            nazov_objektu = "osoba"
        )

    def najdi_clena_podla_id(self, hladane_id):
        for clen in self.zoznam_clenov:
            if clen.id == hladane_id:
                return clen
        return None
        
    def vymaz_clena(self):
        odstranit = int(input("\nZadajte ID/číslo člena, ktorého chcete vymazať: "))
       
        for clen in self.zoznam_clenov:
            if clen.id == odstranit:
                if clen.zoznam_pozicanych:
                    print(f"Člen má stále požičané knihy (ID kníh: {clen.zoznam_pozicanych})")
                    print("Najprv je potrebné vrátiť všetky požičané knihy.")
                    return False
                else:
                    print(f"{clen}")
                    potvrdenie = input(f"\nNaozaj chcete vymazať člena s ID {odstranit}? Ak áno stlačte Y, ak nie stlačte N: ") 
                    if potvrdenie == "Y":
                        self.zoznam_clenov.remove(clen)
                        self.aktualizacia_zoznamu_clenov()
                        print("Člen bol vymazaný.")
                        return True
                    else:
                        print("Člen bol ponechaný v zozname.")
                        return False

        else:
            print("Člen s týmto ID neexistuje.")
            return False
                    
        


    def zobrazit_knihy_clen(self):
        print("Pre zobrazenie kníh, ktoré má člen požičané zadaj ID člena: ")
        try:
            ID_clen = int(input())
            clen_najdeny = False
            
            for clen in self.zoznam_clenov:
                if clen.id == ID_clen:
                    clen_najdeny = True
                    print(f"Knihy požičané členom {clen.meno_clena} {clen.priezvisko_clena}: ")

                    if not clen.zoznam_pozicanych:
                        print(f"{clen.meno_clena} {clen.priezvisko_clena} nemá požičané žiadne knihy.")
                        
                
                    else:
                        for id_knihy in clen.zoznam_pozicanych:
                            for kniha in self.knizny_zoznam:
                                if kniha.id == id_knihy:
                                    print(f"{kniha. nazov_autora} \n{kniha.nazov_knihy} \n{kniha.zaciatok_vypozicky} - {kniha.koniec_vypozicky}\n")
                    break
                
            if not clen_najdeny:        
                print(f"Člen s ID {ID_clen} nebol nájdený.")
            
        except ValueError:

            print("Neplatné ID! Zadajte číslo.")

    def akutalizacia_knizneho_zoznamu(self):
        kniha_to_dict = []
        for kniha in self.knizny_zoznam:
            data_in_dict = vars(kniha)
            kniha_to_dict.append(data_in_dict)
            
    
        with open ("book.json", "w", encoding = "utf-8") as subor:
            json.dump(kniha_to_dict, subor, indent = 4, ensure_ascii = False)


    def aktualizacia_zoznamu_clenov(self):
        clen_to_dict = []
        for person in self.zoznam_clenov:
            data_in_dict = vars(person)
            clen_to_dict.append(data_in_dict)
            
        #[person.clen_dict() for person in self.zoznam_clenov] - kratsi zapis for cyklu
    
        with open ("data.json", "w", encoding = "utf-8") as subor:
            json.dump(clen_to_dict, subor, indent = 4, ensure_ascii = False)
            

    def potvrdit_volbu(self, sprava="Potvrdte volbu (Y/N): "):
        while True:
            odpoved = input(sprava).upper()
            if odpoved == "Y":
                return True
            elif odpoved == "N":
                return False
            else:
                print("Neplatna volba. Zadajte Y pre ano ale N pre nie.")




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

    Kniha.nacitaj_id()
    Clen.nacitaj_id()
    
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
    




     









