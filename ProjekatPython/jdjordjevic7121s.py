from __future__ import annotations
from abc import ABC
from abc import abstractmethod
from os.path import isfile 
import csv

from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By

from selenium.webdriver.remote.webelement import WebElement

class Proizvod(ABC):
    __naziv_modela: str
    __cena: int

    def __init__(self, naziv_modela, cena):
        self.__naziv_modela = naziv_modela
        self.__cena = cena

    def get_naziv_modela(self):
        return self.__naziv_modela

    def get_cena(self):
        return self.__cena

    def set_naziv_modela(self, nov_naziv_modela):
        if len(nov_naziv_modela) < 3:
            print("Naziv modela mora da ima min 3 karaktera")
            return

        self.__naziv_modela = nov_naziv_modela

    def set_cena(self, nova_cena):
        if nova_cena < 0:
            print("Cena mora biti pozitivan broj")
            return

        self.__cena = nova_cena

    def __str__(self) -> str:
        rez = ""
        rez += f"Naziv modela: {self.__naziv_modela}\n"
        rez += f"Cena: {self.__cena}\n"
        return rez
    
    @abstractmethod
    def to_csv(self):
        pass
    
    
    
    @staticmethod
    def sortiraj_listu_ime(l: list[Proizvod]):
        return sorted(l, key=lambda x: x.__naziv_modela)

    @staticmethod
    def sortiraj_listu_cena(l: list[Proizvod]):
        return sorted(l, key=lambda x: -x.__cena)
        
    
class ObicneSlusalice(Proizvod):
    __tip_slusalica: str #sa_mik/bez_mik
    __tip_povezivanja: str #zicano/bezicno/usb
    __tip_sistema: str #stereo/mono/surround
    
    def __init__(self, naziv_modela, cena, tip_slusalica, tip_povezivanja, tip_sistema):
        super().__init__(naziv_modela, cena)
        self.__tip_slusalica = tip_slusalica
        self.__tip_povezivanja = tip_povezivanja
        self.__tip_sistema = tip_sistema
        
    def get_tip_slusalica(self):
        return self.__tip_slusalica
    
    def set_tip_slusalica(self, nov_tip_slusalica):
        if nov_tip_slusalica < 3:
            print("Tip Slusalica mora imati min 3 karaktera")
            return
        self.__tip_slusalica = nov_tip_slusalica
    
    def get_tip_povezivanja(self):
        return self.__tip_povezivanja
    
    def set_tip_povezivanja(self, nov_tip_povezivanja):
        if nov_tip_povezivanja < 2:
            print("Tip povezivanja mora imati min 2 karaktera")
            return
        self.__tip_povezivanja = nov_tip_povezivanja
        
    def get_tip_sistema(self):
        return self.__tip_sistema
    
    def set_tip_sistema(self, nov_tip_sistema):
        if nov_tip_sistema < 3:
            print("Tip sistema ne moze imati ispod 3 karaktera")
            return
        self.__tip_sistema = nov_tip_sistema
        
    def __str__(self) -> str:
        rez = super().__str__()
        rez += f"Tip slusalica: {self.__tip_slusalica}\n"
        rez += f"Tip povezivanja: {self.__tip_povezivanja}\n"
        rez += f"Tip sistema: {self.__tip_sistema}\n"
        return rez
    
#csv - comma separated values -> pretvara objekat u string
    def to_csv(self):
        lista_atributa = [self.get_naziv_modela(), self.get_cena(), self.__tip_slusalica, self.__tip_povezivanja, self.__tip_sistema]
        rez = ""
        for i in lista_atributa:
            rez += f"{i},"

        rez = rez[:-1]

        return rez


# "Dodatni konstruktor"
    @classmethod 
    def from_csv(cls, karakteristike:str):
        
        delovi_teksta = karakteristike.split(",")
        naziv = str(delovi_teksta[0])
        cena = int(delovi_teksta[1])
        tip_slusalica = str(delovi_teksta[2])
        tip_povezivanja = str(delovi_teksta[3])
        tip_sistema = str(delovi_teksta[4])
        nove_slusalice = cls(naziv,cena,tip_slusalica,tip_povezivanja,tip_sistema)
        
        return nove_slusalice
    
    @staticmethod
    def otvori_fajl(naziv_fajla):
        
        if not isfile(naziv_fajla):
            print("Fajl ne postoji")
            return
        
        f = open(naziv_fajla,"r")
        csvreader = csv.reader(f)
        header = []
        header = next(csvreader)

        nizovi_itema = []
        for row in csvreader:
            novi_item = ObicneSlusalice(row[0],int(row[1]), row[2], row[3], row[4])
            nizovi_itema.append(novi_item)
        
        f.close()

        return  nizovi_itema
        
    
    @staticmethod
    def upisi_u_fajl(lista: list[ObicneSlusalice], naziv_fajla:str):
        
        f = open(naziv_fajla,"w")
        
        f.write("Naziv,cena,tip_slusalica,tip_povezivanja,tip_sistema\n")
        
        for i in lista:

            f.write(i.to_csv() + "\n")
        
        f.close()
        return
    
    @staticmethod
    def dohvati_u_opsegu_cene(lista: list[ObicneSlusalice], cena1:int, cena2:int):
        nova_lista = []
        for slusalice in lista:
            if cena1 <= slusalice.get_cena() <= cena2:
                nova_lista.append(slusalice)
        return nova_lista
    





class GamingSlusalice(Proizvod):
    __boja: str
    __tezina: int
    __tip_mikrofona: str
    
    def __init__(self, naziv_modela, cena, boja, tezina, tip_mikrofona):
        super().__init__(naziv_modela, cena)
        self.__boja = boja
        self.__tezina = tezina
        self.__tip_mikrofona = tip_mikrofona
        
    def get_boja(self):
        return self.__boja
    
    def set_boja(self, nova_boja):
        if len(nova_boja) < 3:
            print("Boja mora da ima vise od 3 karaktera")
            return
        self.__boja = nova_boja
        
    def get_tezina(self):
        return self.__tezina
    
    def set_tezina(self, nova_tezina):
        if nova_tezina < 30:
            print("Ne moze biti lakse od 30g")
            return
        self.__tezina = nova_tezina
        
    def get_tip_mikrofona(self):
        return self.__tip_mikrofona
    
    def set_tip_mikrofona(self, nov_tip_mikrofona):
        if len(nov_tip_mikrofona)<3:
            print("Ne moze imati ispod 3 karaktera")
            return
        self.__tip_mikrofona = nov_tip_mikrofona
        
    def __str__(self) -> str:
        rez = super().__str__()
        rez += f"Boja slusalica: {self.__boja}"
        rez += f"Tezina slusalica: {self.__tezina}"
        rez += f"Tip mikrofona: {self.__tip_mikrofona}"
        
    def to_csv(self):
        lista_atributa = [self.__naziv_modela, self.__cena, self.__boja, self.__tezina, self.__tip_mikrofona]
        rez = ""
        for i in lista_atributa:
            rez += f"{i},"
            
        rez = rez[:-1]

        return rez
    
# "Dodatni konstruktor"
    @classmethod 
    def from_csv(cls, karakteristike:str):
        
        delovi_teksta = karakteristike.split(",")
        naziv = str(delovi_teksta[0])
        cena = int(delovi_teksta[1])
        boja = str(delovi_teksta[2])
        tezina = int(delovi_teksta[3])
        tip_mikrofona = str(delovi_teksta[4])
        nove_slusalice = cls(naziv,cena,boja,tezina,tip_mikrofona)
        
        return nove_slusalice
    
    @staticmethod
    def otvori_fajl(naziv_fajla):
        
        if not isfile(naziv_fajla):
            print("Fajl ne postoji")
            return
        
        f = open(naziv_fajla,"r")
        csvreader = csv.reader(f)
        header = []
        header = next(csvreader)

        nizovi_itema = []
        for row in csvreader:
            novi_item = GamingSlusalice(row[0],int(row[1]), row[2], int(row[3]), row[4])
            nizovi_itema.append(novi_item)
        
        f.close()

        return  nizovi_itema
    
    @staticmethod
    def upisi_u_fajl(lista: list[GamingSlusalice], naziv_fajla:str):
        
        f = open(naziv_fajla,"w")
        
        f.write("Naziv,cena,boja,tezina,tip_mikrofona\n")
        
        for i in lista:

            f.write(i.to_csv() + "\n")
        
        f.close()
        return

    @staticmethod
    def dohvati_u_opsegu_cene(lista: list[GamingSlusalice], cena1:int, cena2:int):
        nova_lista = []
        for slusalice in lista:
            if cena1 <= slusalice.get_cena() <= cena2:
                nova_lista.append(slusalice)
        return nova_lista
    
        
    
#=================================================  PYTHON DEO TST ============================================================

# p1 = ObicneSlusalice("Asus", 300, "Sa_mikrofonom", "Bezicne", "Stereo")
# p3 = ObicneSlusalice("Hamma", 50, "Sa_mikrofonom", "Zicane", "Mono")



# lista=[p1,p3]

# s = p1.to_csv()
# print(s)

# p1.from_csv(s)

# print(p1)

# ObicneSlusalice.otvori_fajl("slusalice.txt")

# ObicneSlusalice.upisi_u_fajl(lista, "out.txt")



# filtrirana_lista = ObicneSlusalice.dohvati_u_opsegu_cene(lista,40,100)

# for i in filtrirana_lista:
#     print(i)

#=================================================  PYTHON DEO TST ============================================================



class Tehnomanija:
    __driver : webdriver.Chrome

    def __init__(self, putanja_do_chromedrivera="chromedriver") -> None:
        self.__driver = webdriver.Chrome(putanja_do_chromedrivera)


    
    def poseti_stranicu(self, putanja_do_stranice):
        self.__driver.get(putanja_do_stranice)
    
    def zatvori_stranicu(self):
        self.__driver.quit()
    
    def zatvori_tab(self):
        self.__driver.close()

    def sacekaj(self, broj_sekundi = 10):
        sleep(broj_sekundi)
    
    def implicitly_wait(self, broj_sekundi = 10):
        self.__driver.implicitly_wait(broj_sekundi)
    
    def dohvati_elemente(self,pretraga_id = "", pretraga_klasa="",pretraga_tag_name="",pretraga_name="",pretraga_link_text="",pretraga_partial_link_text = "",pretraga_css_selektor=""):
        self.__driver.implicitly_wait(10)
        if len(pretraga_id) != 0:
            try:
                rez = self.__driver.find_element(By.ID, pretraga_id)  
                return rez  
            except:
                return None  
            
        if len(pretraga_klasa) != 0:
            try:
                rez = self.__driver.find_elements(By.CLASS_NAME, pretraga_klasa) 
                return rez 
            except:
                return []  

        if len(pretraga_tag_name) != 0:
            try:
                rez = self.__driver.find_elements(By.TAG_NAME, pretraga_tag_name)
                return rez 
            except:
                return []  
        
        if len(pretraga_name) != 0:
            try:
                rez = self.__driver.find_elements(By.NAME, pretraga_name)
                return rez 
            except:
                return [] 
        
        if len(pretraga_link_text) != 0:
            try:
                rez = self.__driver.find_elements(By.LINK_TEXT, pretraga_link_text)
                return rez 
            except:
                return []
            
        if len(pretraga_partial_link_text) != 0:
            try:
                rez = self.__driver.find_elements(By.PARTIAL_LINK_TEXT, pretraga_partial_link_text)
                return rez 
            except:
                return []
        
        if len(pretraga_css_selektor) != 0:
            try:
                rez = self.__driver.find_elements(By.CSS_SELECTOR,pretraga_css_selektor)
                return rez 
            except:
                return []

    

    @staticmethod
    def vrati_listu_putanja(broj_strana):
        pocetna_putanja = "https://www.tehnomanija.rs/c/televizori-audio-i-video/slusalice-zvucnici-i-audio/slusalice-10020108"
        lista_putanja = [pocetna_putanja]
        for i in range(2,broj_strana+1):#krecemo od strane dva
            putanja = f"{pocetna_putanja}?currentPage={i}"
            lista_putanja.append(putanja)
    
        return lista_putanja
    
    def obidji_stranicu(self, putanja_do_stranice):
        self.poseti_stranicu(putanja_do_stranice)
        svi_linkovi:list[WebElement] = self.dohvati_elemente(pretraga_klasa="product-carousel--href")
        n = len(svi_linkovi)
        print(n)
        linkovi_slusalica = []
        
        for link in svi_linkovi:
            linkovi_slusalica.append(link.get_attribute("href"))

        niz_slusalica = []

        for link in linkovi_slusalica:
            self.poseti_stranicu(link)
            features: list[WebElement] = self.dohvati_elemente(
                pretraga_tag_name="tr"
            )

            properties = {}
            for feature in features:
                try:
                    name = feature.find_elements(By.CLASS_NAME, "feature-name")[0]
                    value = feature.find_elements(By.CLASS_NAME, "feature-value")[0]

                    properties[name.text] = value.text
                except:
                    pass

            print(properties)

            try:
                naziv_modela = self.dohvati_elemente(pretraga_tag_name="h1")
                  
            except:
                pass


def main():
    t1 = Tehnomanija()

    # t1.poseti_stranicu("https://www.tehnomanija.rs/c/televizori-audio-i-video/slusalice-zvucnici-i-audio/slusalice-10020108")
    # t1.sacekaj(5)
    
    # rez= t1.dohvati_elemente(pretraga_klasa="product-carousel--href")
    # n = len(rez)
    # print(n)
    t1.obidji_stranicu("https://www.tehnomanija.rs/c/televizori-audio-i-video/slusalice-zvucnici-i-audio/slusalice-10020108")
    # rez =t1.dohvati_elemente(pretraga_tag_name="img")
    # print(len(rez))
    # print(rez)
    t1.sacekaj(5)
    t1.zatvori_stranicu()

    

if __name__ =="__main__":
    main()