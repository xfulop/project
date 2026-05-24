from abc import ABC, abstractmethod
from datetime import date
import json


#  Absztrakt alap osztály


class Auto(ABC):
    def __init__(self, rendszam, tipus, berleti_dij):
        self.__rendszam = rendszam
        self.__tipus = tipus
        self.__berleti_dij = berleti_dij
        self.__elerheto = True

    # Getterek
    def get_rendszam(self):
        return self.__rendszam

    def get_tipus(self):
        return self.__tipus

    def get_berleti_dij(self):
        return self.__berleti_dij

    def is_elerheto(self):
        return self.__elerheto

    # Setterek

    def set_elerheto(self, ertek):
        self.__elerheto = ertek

    @abstractmethod
    def __str__(self):
        pass


#  Személyautó

class Szemelvauto(Auto):
    def __init__(self, rendszam, berleti_dij, utasok_szama):
        super().__init__(rendszam, "szemely", berleti_dij)
        self.__utasok_szama = utasok_szama

    def get_utasok_szama(self):
        return self.__utasok_szama

    def __str__(self):
        allapot = "szabad" if self.is_elerheto() else "szervizben"
        return (f"[Személyautó] {self.get_rendszam()} | "
                f"{self.get_utasok_szama()} utas | "
                f"{self.get_berleti_dij()} Ft/nap | {allapot}")


#  Teherautó

class Teherauto(Auto):
    def __init__(self, rendszam, berleti_dij, teherbiras):
        super().__init__(rendszam, "teher", berleti_dij)
        self.__teherbiras = teherbiras

    def get_teherbiras(self):
        return self.__teherbiras

    def __str__(self):
        allapot = "szabad" if self.is_elerheto() else "szervizben"
        return (f"[Teherautó]   {self.get_rendszam()} | "
                f"{self.get_teherbiras()} kg | "
                f"{self.get_berleti_dij()} Ft/nap | {allapot}")


#  Bérlés

class Berles:
    def __init__(self, berles_id, auto, datum):
        self.__id = berles_id
        self.__auto = auto
        self.__datum = datum

    def get_id(self):
        return self.__id

    def get_auto(self):
        return self.__auto

    def get_datum(self):
        return self.__datum

    def __str__(self):
        return (f"Bérlés #{self.__id} | "
                f"{self.__auto.get_rendszam()} | "
                f"Dátum: {self.__datum}")


#  Autókölcsönző

class Autokolcsonzo:
    def __init__(self, nev):
        self.__nev = nev
        self.__autok = []
        self.__berlesek = []
        self.__kovetkezo_id = 1

    def get_nev(self):
        return self.__nev

    #  Belső segédmetódusok

    def __auto_keresese(self, rendszam):
        for auto in self.__autok:
            if auto.get_rendszam() == rendszam:
                return auto
        return None

    def __berles_keresese(self, berles_id):
        for berles in self.__berlesek:
            if berles.get_id() == berles_id:
                return berles
        return None

    def __van_berlese_arra_a_napra(self, auto, datum_str):
        for berles in self.__berlesek:
            if berles.get_auto().get_rendszam() == auto.get_rendszam() and berles.get_datum() == datum_str:
                return True
        return False

    # Fő műveletek

    def auto_berlese(self, rendszam, datum_str):
        try:
            datum = date.fromisoformat(datum_str)
        except ValueError:
            raise ValueError("Érvénytelen dátumformátum. Használj ÉÉÉÉ-HH-NN formátumot.")

        if datum <= date.today():
            raise ValueError("A bérlési dátumnak jövőbelinek kell lennie.")

        auto = self.__auto_keresese(rendszam)
        if auto is None:
            raise ValueError(f"Nem található ilyen rendszámú autó: {rendszam}")

        if not auto.is_elerheto():
            raise ValueError(f"Az autó ({rendszam}) jelenleg szervizben van.")

        if self.__van_berlese_arra_a_napra(auto, datum_str):
            raise ValueError(f"Az autó ({rendszam}) erre a napra már foglalt: {datum_str}")

        uj_berles = Berles(self.__kovetkezo_id, auto, datum_str)
        self.__berlesek.append(uj_berles)
        self.__kovetkezo_id += 1
        return uj_berles

    def berles_lemondasa(self, berles_id):
        berles = self.__berles_keresese(berles_id)
        if berles is None:
            raise ValueError(f"Nem található ilyen azonosítójú bérlés: {berles_id}")

        self.__berlesek.remove(berles)
        return berles

    def berlesek_listazasa(self):
        if not self.__berlesek:
            print("Jelenleg nincsenek aktív bérlések.")
            return
        for berles in self.__berlesek:
            print(berles)

    def autok_listazasa(self):
        for auto in self.__autok:
            print(auto)

    #  JSON mentés / betöltés

    def mentes_json(self, fajlnev="adatok.json"):
        adatok = {
            "kolcsonzo": {
                "nev": self.__nev
            },
            "autok": [],
            "berlesek": []
        }

        for auto in self.__autok:
            auto_adat = {
                "tipus": auto.get_tipus(),
                "rendszam": auto.get_rendszam(),
                "berleti_dij": auto.get_berleti_dij(),
                "elerheto": auto.is_elerheto()
            }
            if isinstance(auto, Szemelvauto):
                auto_adat["utasok_szama"] = auto.get_utasok_szama()
            elif isinstance(auto, Teherauto):
                auto_adat["teherbiras"] = auto.get_teherbiras()
            adatok["autok"].append(auto_adat)

        for berles in self.__berlesek:
            adatok["berlesek"].append({
                "id": berles.get_id(),
                "auto_rendszam": berles.get_auto().get_rendszam(),
                "datum": berles.get_datum()
            })

        with open(fajlnev, "w", encoding="utf-8") as f:
            json.dump(adatok, f, ensure_ascii=False, indent=2)

        print(f"Adatok elmentve: {fajlnev}")

    def betoltes_json(self, fajlnev="adatok.json"):
        try:
            with open(fajlnev, "r", encoding="utf-8") as f:
                adatok = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Nem található a fájl: {fajlnev}")

        self.__autok = []
        self.__berlesek = []

        for a in adatok["autok"]:
            if a["tipus"] == "szemely":
                auto = Szemelvauto(a["rendszam"], a["berleti_dij"], a["utasok_szama"])
            elif a["tipus"] == "teher":
                auto = Teherauto(a["rendszam"], a["berleti_dij"], a["teherbiras"])
            else:
                continue
            auto.set_elerheto(a["elerheto"])
            self.__autok.append(auto)

        max_id = 0
        for b in adatok["berlesek"]:
            auto = self.__auto_keresese(b["auto_rendszam"])
            if auto is None:
                continue
            berles = Berles(b["id"], auto, b["datum"])
            self.__berlesek.append(berles)
            if b["id"] > max_id:
                max_id = b["id"]

        self.__kovetkezo_id = max_id + 1
        print(f"Adatok betöltve: {fajlnev}")