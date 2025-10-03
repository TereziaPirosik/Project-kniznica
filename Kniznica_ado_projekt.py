
import json

class Kniha:
    id_counter = 1
    
    def __init__(self, nazov_autora, nazov_knihy, ISBN, rok_vydania, pozicanie, kategoria, zaciatok_vypozicky):
        self.id = Kniha.id_counter
        Kniha.id_counter +=1
        
        self.nazov_autora = nazov_autora
        self.nazov_knihy = nazov_knihy
        self.ISBN = ISBN
        self.rok_vydania = int(rok_vydania)
        self.pozicanie = pozicanie
        self.kategoria = kategoria
        self.zaciatok_vypozicky = zaciatok_vypozicky
        self.koniec_vypozicky = int(self.zaciatok_vypozicky + 10) if self.zaciatok_vypozicky is not None else None

    def __str__(self):
        return f"{self.nazov_autora}: {self.nazov_knihy}, {self.rok_vydania}, {self.pozicanie}, {self.ISBN},{self.kategoria}"

    def kniha_dict(self):
        return{
            "Meno autora": self.nazov_autora,
            "Nazov knihy": self.nazov_knihy,
            "cislo ISBN": self.ISBN,
            "Rok vydania": self.rok_vydania,
            "Pozicana": self.pozicanie,
            "Kategoria": self.kategoria,
            "Datum vypozicania": self.zaciatok_vypozicky,
            "Koniec vypozicky": self.koniec_vypozicky
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
            "Pozicane knihy": self.zoznam_pozicanych
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
                existujuca_kniha = Kniha(book["Meno autora"], book["Nazov knihy"], book["cislo ISBN"], book["Rok vydania"], book["Pozicana"], book["Kategoria"], book["Datum vypozicania"]  )
                self.knizny_zoznam.append(existujuca_kniha)
            print("Data zo suboru book.json su nacitane.")
  
    
    def vypis_knizny_zoznam(self):
        for kniha in self.knizny_zoznam:
            print(f"\n{kniha}")

    def pridaj_novu_knihu(self):
        print("\nZadaj informacie o knihe: nazov autora, nazov knihz, ISBN cislo a rok vydania.\n")
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
        #for kniznica in self.knizny_zoznam:
            #print(f" - {kniznica}")

        kniha_to_dict = []
        for kniha in self.knizny_zoznam:
            data_in_dict = kniha.kniha_dict()
            kniha_to_dict.append(data_in_dict)
            
        
    
        with open ("book.json", "w", encoding = "utf-8") as subor:
            json.dump(kniha_to_dict, subor, indent = 4, ensure_ascii = False)

    

       


    def najdi_knihu_nazov_knihy(self):
        hladany = input("\nZadaj nazov knihy: ")
        iter = 0
        for kniha in self.knizny_zoznam:
            if kniha.nazov_knihy.lower() == hladany.lower():
                print(f"Kniha bola najdena: {kniha}")
                iter += 1
                
        if iter == 0:
            print("Knina nie je v zozname!")




    def pozicaj_knihu(self):
        vyber_zo_zoznamu = input("Aku knizku chcete pozicat? Napiste nazov knihy: ")


        for vyber in self.knizny_zoznam:
            if vyber.nazov_knihy.lower() == vyber_zo_zoznamu.lower():
                if vyber.pozicanie == "N":
                    print(f"{vyber.id}: {vyber.nazov_knihy} od {vyber.nazov_autora}")

                    pozicanie = input("Chcete pozicat tuto knihu? (napiste Y alebo N): ")

                    if pozicanie == "Y":
                        existuje = self.najdi_clena()
                    
                        if existuje == True:
                            id_cloveka = int(input("Zadajte ID clena, ktory si knihu poziciava: "))
                            for clovek in self.zoznam_clenov:
                                print(f"vypis {id_cloveka} a {clovek.id}")
                                if id_cloveka == clovek.id:
                                    clovek.zoznam_pozicanych.append(vyber.id)
                                    print("Kniha bola priradena.")

                                    clen_to_dict = []
                                    for person in self.zoznam_clenov:
                                        data_in_dict = person.clen_dict()
                                        clen_to_dict.append(data_in_dict)
        
    
                                    with open ("data.json", "w", encoding = "utf-8") as subor:
                                        json.dump(clen_to_dict, subor, indent = 4, ensure_ascii = False)

                        if vyber.pozicanie == "N":
                            vyber.pozicanie = "Y"
                            #self.knizny_zoznam.append(vyber)
                            print(f"{vyber.nazov_knihy} je uspesne pozicana.")

                            kniha_to_dict = []
                            for kniha in self.knizny_zoznam:
                                data_in_dict = kniha.kniha_dict()
                                kniha_to_dict.append(data_in_dict)
            
        
    
                            with open ("book.json", "w", encoding = "utf-8") as subor:
                                json.dump(kniha_to_dict, subor, indent = 4, ensure_ascii = False)
                                
                #else:
                    #print("Kniha je uz pozicana")


    def vratenie_knihy(self):       
        vratka = input("Napiste nazov knihy, ktoru chcete vratit: ")
        
        for vyber in self.knizny_zoznam:
            if vyber.nazov_knihy.lower() == vratka.lower():
                if vyber.pozicanie == "Y":
                    print(f"{vyber.id}: {vyber.nazov_knihy} od {vyber.nazov_autora}")

                    pozicanie = input("Chcete vratit tuto knihu? (napiste Y alebo N): ")

                    if pozicanie == "Y":
                        existuje = self.najdi_clena()
                    
                        if existuje == True:
                            id_cloveka = int(input("Zadajte ID clena, ktory knihu vracia: "))
                            for clovek in self.zoznam_clenov:
                                print(f"vypis {id_cloveka} a {clovek.id}")
                                if id_cloveka == clovek.id:
                                    print(f"{vyber.id}")
                                    print(f"{clovek.zoznam_pozicanych}")
                                    clovek.zoznam_pozicanych.remove(int(vyber.id))
                                    
                                    print("Kniha bola odstranena zo zoznamu.")

                                    clen_to_dict = []
                                    for person in self.zoznam_clenov:
                                        data_in_dict = person.clen_dict()
                                        clen_to_dict.append(data_in_dict)
        
    
                                    with open ("data.json", "w", encoding = "utf-8") as subor:
                                        json.dump(clen_to_dict, subor, indent = 4, ensure_ascii = False)

                                    if vyber.pozicanie == "Y":
                                        vyber.pozicanie = "N"
                                        #self.knizny_zoznam.append(vyber)
                                        print(f"{vyber.nazov_knihy} je uspesne vratena.")

                                    kniha_to_dict = []
                                    for kniha in self.knizny_zoznam:
                                        data_in_dict = kniha.kniha_dict()
                                        kniha_to_dict.append(data_in_dict)
            
    
                                    with open ("book.json", "w", encoding = "utf-8") as subor:
                                        json.dump(kniha_to_dict, subor, indent = 4, ensure_ascii = False)

                                    break

                                
    def vymaz_knihu_nazov_knihy(self):
        vymaz_knihu = input("Napis nazov knihy, ktoru chcete vymazat: ")

        count = 0
        for nazov_knihy in self.knizny_zoznam:
            if  nazov_knihy.nazov_knihy.lower()== vymaz_knihu.lower():
                count += 1
                self.knizny_zoznam.remove(nazov_knihy)
                print(f"Kniha {nazov_knihy} bola vymazana")

        if count == 0:
            print("Tato kniha neexistuje v zozname.")

            kniha_to_dict = []
            for kniha in self.knizny_zoznam:
                data_in_dict = kniha.kniha_dict()
                kniha_to_dict.append(data_in_dict)
            
    
            with open ("book.json", "w", encoding = "utf-8") as subor:
                json.dump(kniha_to_dict, subor, indent = 4, ensure_ascii = False)




    def vymaz_knihu_ISBN(self):
        isbn_vymaz = input("Napis cislo ISBN, ktore chces vymazat: \nNapis ho v tomto tvare: ISBN798465164: ")
        count = 0
        for isbn in self.knizny_zoznam:
            if isbn.ISBN == isbn_vymaz:
                count += 1
                self.knizny_zoznam.remove(isbn)
                print(f"Kniha s ISBN {isbn_vymaz} bola vymazana")

        if count == 0:
            print("Taketo cislo ISBN neexistuje")

            kniha_to_dict = []
            for kniha in self.knizny_zoznam:
                data_in_dict = kniha.kniha_dict()
                kniha_to_dict.append(data_in_dict)
            
    
            with open ("book.json", "w", encoding = "utf-8") as subor:
                json.dump(kniha_to_dict, subor, indent = 4, ensure_ascii = False)

                


    def nacitaj_zoznam_clenov(self):
        with open("data.json", "r", encoding = "utf-8") as subor:
            data = json.load(subor)
            for clen in data:
                existujuci_clen = Clen(clen["Meno"], clen["Priezvisko"], clen["Rok_narodenia"], clen["Pozicane knihy"])
                self.zoznam_clenov.append(existujuci_clen)
        print("Data zo suboru data.json su nacitane.")

        for clenovia in self.zoznam_clenov:
            print(f"{clenovia.zoznam_pozicanych}")
 

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
                print(f"Clen bol najdeny: {osoba.id}: {osoba.meno_clena} {osoba.priezvisko_clena}")
                count += 1
                return True
        if count == 0:
            print("Clen nie je v zozname!")
            return False 


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







if __name__ == '__main__': 
    print("Script is running")


     
kniznica = Kniznica()
#kniznica.vypis_knizny_zoznam()
#kniznica.pridaj_novu_knihu()
#kniznica.pridaj_novu_knihu()
#kniznica.najdi_knihu_nazov_knihy()
#kniznica.pridaj_novu_knihu()

kniznica.vypis_zoznam()

print("-----------------------------")
print("ZOZNAM KNIH")
print("-----------------------------")
kniznica.vypis_knizny_zoznam()

#print("-----------------------------")
#print("POZICANIE KNIHY")
#print("-----------------------------")
#kniznica.pozicaj_knihu()

#print("-----------------------------")
#print("POZICANIE KNIHY")
#print("-----------------------------")
#kniznica.pozicaj_knihu()
print("-----------------------------")
print("VRATENIE KNIHY")
print("-----------------------------")
kniznica.vratenie_knihy()

#kniznica.vypis_knizny_zoznam()

#kniznica.vymaz_knihu_ISBN()
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









