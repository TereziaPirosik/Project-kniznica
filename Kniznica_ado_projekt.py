import json

class Kniha:
    
    def __init__(self, nazov_autora, nazov_knihy, ISBN, rok_vydania, pozicanie, kategoria):
        self.nazov_autora = nazov_autora
        self.nazov_knihy = nazov_knihy
        self.ISBN = ISBN
        self.rok_vydania = int(rok_vydania)
        self.pozicanie = pozicanie
        self.kategoria = kategoria

    def __str__(self):
        return f"{self.nazov_autora}: {self.nazov_knihy}, {self.rok_vydania}, {self.pozicanie}, {self.kategoria}"

    def kniha_dict(self):
        return{
            "Meno autora": self.nazov_autora,
            "Nazov knihy": self.nazov_knihy,
            "cislo ISBN": self.ISBN,
            "Rok vydania": self.rok_vydania,
            "Pozicana": self.pozicanie,
            "Kategoria": self.kategoria
          }


        
class Clen:
    id_counter = 1
    
    def __init__(self, meno_clena, priezvisko_clena, rok_narodenia):
        self.id = Clen.id_counter
        Clen.id_counter += 1
        self.meno_clena = meno_clena
        self.priezvisko_clena = priezvisko_clena
        self.rok_narodenia = rok_narodenia
        

    def __str__(self):
        return f"{self.id}: {self.meno_clena} {self.priezvisko_clena} {self.rok_narodenia}"

    def clen_dict(self):
        return {
            "ID": self.id,
            "Meno": self.meno_clena,
            "Priezvisko": self.priezvisko_clena,
            "Rok_narodenia": self.rok_narodenia 
        }
        

class Kniznica:
    
    
    def __init__(self):
        self.knizny_zoznam = []
        self.zoznam_clenov = []
        self.zoznam_pozicanych = []
        self.nacitaj_zoznam_clenov()

    def __str__(self):
        return f"{self.knizny_zoznam}"
        return f"{self.zoznam_clenov}"

    #def nacitaj_knizny_zoznam(self):
         with open("book.json", "r", encoding = "utf-8") as subor:
            books = json.load(subor)
            for book in books:
                existujuca_kniha = Kniha(book["Meno autora"], book["Nazov knihy"], book["ISBN"], book["Rok vydania"], book["Pozicanie"], book["Kategoria"]  )
                self.knizny_zoznam.append(existujuca_kniha)
        print("Data zo suboru su nacitane.")
  
    
    def vypis_knizny_zoznam(self):
        for kniha in self.knizny_zoznam:
            print(f"kniha")

    def pridaj_novu_knihu(self):
        print("Zadaj informacie o knihe: nazov autora, nazov knihz, ISBN cislo a rok vydania.")
        print("Zadaj meno autora: ")
        nazov_autora = input()
        print("Zadaj nazov knihy: ")
        nazov_knihy = input()
        print("Zadaj cislo ISBN: ")
        ISBN = input()
        print("Napis rok vydania knihy: ")
        rok_vydania = input()
        print("Poskytnite informaciu, ci je kniha pozicana. Ak ano, napiste Y, ak nie, tak napiste N")
        pozicanie = input()
        print("Napiste do akej kategoria kniha patri: ")
        kategoria = input()
        
        
        nova_kniha = Kniha(nazov_autora, nazov_knihy, ISBN, rok_vydania, pozicanie, kategoria)
        self.knizny_zoznam.append(nova_kniha)
        print(f"{str(nova_kniha)} bola pridane do knizneho zoznamu.")
        for kniznica in self.knizny_zoznam:
            print(f" - {kniznica}")

        kniha_to_dict = []
        for kniha in self.knizny_zoznam:
            data_in_dict = kniha.clen_dict()
            clen_to_dict.append(data_in_dict)
            
        #[person.clen_dict() for person in self.zoznam_clenov] - kratsi zapis for cyklu
    
        with open ("data.json", "w", encoding = "utf-8") as subor:
            json.dump(clen_to_dict, subor, indent = 4, ensure_ascii = False)

    


   # def vymaz_knihu(self):


    #def najdi_knihu(self)
       # hladany = input("Zadaj nazov knihy: ")
        #for kniha in self.knizny_zoznam:
           # if kniha.nazov_knihy.lower() == hladany.lower():
              #  print(f"Kniha bola najdena: {kniha}")
               # return 
       # else:
          #  print("Knina nie je v zozname!")




    #def pozicaj_knihu(self):


          

    def nacitaj_zoznam_clenov(self):
        with open("data.json", "r", encoding = "utf-8") as subor:
            data = json.load(subor)
            for clen in data:
                existujuci_clen = Clen(clen["Meno"], clen["Priezvisko"], clen["Rok_narodenia"])
                self.zoznam_clenov.append(existujuci_clen)
        print("Data zo suboru su nacitane.")
 

    def pridaj_noveho_clena(self):
        print("Poskytnite informacie o novom clenovi pre zapis: ")
        meno_clena = input("Napis meno noveho clena: ")
        priezvisko_clena = input("Napis priezvisko noveho clena: ")
        rok_narodenia = int(input("Napis rok narodenia: "))
        
        novy_clen = Clen(meno_clena, priezvisko_clena, rok_narodenia)
        self.zoznam_clenov.append(novy_clen)

        clen_to_dict = []
        for person in self.zoznam_clenov:
            data_in_dict = person.clen_dict()
            clen_to_dict.append(data_in_dict)
            
        #[person.clen_dict() for person in self.zoznam_clenov] - kratsi zapis for cyklu
    
        with open ("data.json", "w", encoding = "utf-8") as subor:
            json.dump(clen_to_dict, subor, indent = 4, ensure_ascii = False)
            
        print(f"\nNovy clen {meno_clena} {priezvisko_clena} je pridany.\n")
        print("Udaje boli pridane do suboru.\n")

        return True

    def vypis_zoznam(self):
        for osoba in self.zoznam_clenov:
            print(f"{osoba}")
        

    def najdi_clena(self):
        hladany_clen = input("\nZadaj meno clena: ")
        count = 0
        for osoba in self.zoznam_clenov:
            if osoba.meno_clena.lower() == hladany_clen.lower():
                print(f"Clen bol najdeny: {osoba.meno_clena} {osoba.priezvisko_clena}")
                count += 1
                
        if count == 0:
            print("Clen nie je v zozname!")
            
        return

    def najdi_clena_podla_priezviska(self):
        hladany_clen = input("\nNapis priezvisko hladaneho: ")
        count = 0
        for osoba in self.zoznam_clenov:
            if osoba.priezvisko_clena.lower() == hladany_clen.lower():
                print(f"Clen bol najdeny: {osoba.meno_clena} {osoba.priezvisko_clena}")
                count += 1
        
        if count == 0:
            print("Clen s tymto priezviskom sa nenachadza v zozname.")
        return


    def vymaz_clena(self):
        odstranit = int(input("\nZadajte ID/cislo clena, ktoreho chcete vymazat: "))
        potvrdenie = input(f"\nNaozaj chcete vymazat clena s ID {odstranit}? Ak ano stlacte Y, ak nie stalcte N: ")
        
        if potvrdenie == "Y":
            count = 0
            for number in self.zoznam_clenov:
                if number.id == odstranit:
                    count += 1
                    break
            if count > 0:
                for clen in self.zoznam_clenov:
                    if clen.id == odstranit:
                        self.zoznam_clenov.remove(clen)
                        print("Clen bol vymazany.")


                        clen_to_dict = []
                        for person in self.zoznam_clenov:
                            data_in_dict = person.clen_dict()
                            clen_to_dict.append(data_in_dict)
        
    
                        with open ("data.json", "w", encoding = "utf-8") as subor:
                            json.dump(clen_to_dict, subor, indent = 4, ensure_ascii = False)
            else:
                print("Clen s tymto ID neexistuje.")
                    
        else:
            print("Clen bol ponechany v zozname.")





#kniha1 = Kniha("Tessa Afshar", "Perla z piesku", "ISBN458792", 2020)
#kniha2 = Kniha("Petr Ludwig", "Konec prokrastinace", "ISBN5468754", 2019)

if __name__ == '__main__': 
    print("Script is running")
       
kniznica = Kniznica()
kniznica.vypis_knizny_zoznam()
kniznica.pridaj_novu_knihu()
#kniznica.pridaj_noveho_clena()
#kniznica.pridaj_noveho_clena()
#kniznica.pridaj_noveho_clena()
#kniznica.vypis_zoznam()
#kniznica.najdi_clena()
#kniznica.najdi_clena_podla_priezviska()
#kniznica.vymaz_clena()
#kniznica.vypis_zoznam()  
#kniznica.pridaj_noveho_clena()      
#kniznica.vypis_zoznam()









