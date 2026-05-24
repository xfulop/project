from kolcsonzo import Autokolcsonzo

ADATFAJL = "adatok.json"

def menu_kiiras():
    print("\n=== Autókölcsönző ===")
    print("1. Autók listázása")
    print("2. Bérlések listázása")
    print("3. Autó bérlése")
    print("4. Bérlés lemondása")
    print("0. Kilépés")
    print("====================")

def auto_berlese(kolcsonzo):
    print("\n-- Autó bérlése --")
    kolcsonzo.autok_listazasa()
    rendszam = input("Add meg a rendszámot: ").strip().upper()
    datum = input("Add meg a dátumot (ÉÉÉÉ-HH-NN): ").strip()
    try:
        berles = kolcsonzo.auto_berlese(rendszam, datum)
        print(f"Sikeres bérlés! {berles}")
    except ValueError as e:
        print(f"Hiba: {e}")

def berles_lemondasa(kolcsonzo):
    print("\n-- Bérlés lemondása --")
    kolcsonzo.berlesek_listazasa()
    try:
        berles_id = int(input("Add meg a bérlés azonosítóját: ").strip())
        berles = kolcsonzo.berles_lemondasa(berles_id)
        print(f"Bérlés #{berles.get_id()} sikeresen lemondva.")
    except ValueError as e:
        print(f"Hiba: {e}")

def main():
    kolcsonzo = Autokolcsonzo("Budapest Autókölcsönző")

    try:
        kolcsonzo.betoltes_json(ADATFAJL)
    except FileNotFoundError as e:
        print(f"Figyelmeztetés: {e} – Hiányzik az adatok.json fájl.")

    while True:
        menu_kiiras()
        valasztas = input("Választás: ").strip()

        if valasztas == "1":
            print("\n-- Autók --")
            kolcsonzo.autok_listazasa()
        elif valasztas == "2":
            print("\n-- Bérlések --")
            kolcsonzo.berlesek_listazasa()
        elif valasztas == "3":
            auto_berlese(kolcsonzo)
        elif valasztas == "4":
            berles_lemondasa(kolcsonzo)
        elif valasztas == "0":
            kolcsonzo.mentes_json(ADATFAJL)
            print("Viszlát!")
            break
        else:
            print("Érvénytelen választás, próbáld újra.")

if __name__ == "__main__":
    main()
