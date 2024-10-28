import pygame
from abc import ABC, abstractmethod #ABC = Abstract Base Class
from datetime import datetime

pygame.init()

FEHER = (255, 255, 255)
FEKETE = (0, 0, 0)
KEK = (0, 0, 255)
ZOLD = (0, 255, 0)
PIROS = (255, 0, 0)

# Képernyő beállításai:
ablak_tuple = (1920,1080) # Az ablak_tuple-ben a ablak_tuple[0] jelenti a szélességet míg az ablak_tuple[1] a magasságot

ablak = pygame.display.set_mode((ablak_tuple), pygame.RESIZABLE , pygame.FULLSCREEN) #Teljes képernyős mód az " | " is lehet használni
#ablak = pygame.display.set_mode(ablak_tuple) #Alap megjelenítés

pygame.display.set_caption('Autókölcsönző rendszer || OOP || Fauszt Tibor Zoltán || C6ZMWT')

font = pygame.font.Font(None, 36) # Betűkészlet


# Auto absztrakt osztály (Fő osztályok 1.1 Kész)
class Auto(ABC):
    def __init__(self, rendszam, tipus, evjarat, berleti_dij):
        self.rendszam = rendszam
        self.tipus = tipus
        self.berleti_dij = berleti_dij
        self.evjarat = evjarat
        self.berelve = False

    @abstractmethod
    def auto_info(self):
        pass


# Személyauto osztály (Fő osztályok 1.2 Kész)
class Szemelyauto(Auto):
    def __init__(self, rendszam, tipus, evjarat, berleti_dij, szin):
        super().__init__(rendszam, tipus, evjarat, berleti_dij)
        self.szin = szin

    def auto_info(self):
        return f"Személyautó: {self.tipus}, Rendszám: {self.rendszam}, Színe: {self.szin}, Évjárat: {self.evjarat} Bérleti díj: {self.berleti_dij} HUF/nap"


# Teherauto osztály (Fő osztályok 1.3 Kész)
class Teherauto(Auto):
    def __init__(self, rendszam, tipus, evjarat, berleti_dij, teherbiras):
        super().__init__(rendszam, tipus, evjarat, berleti_dij)
        self.teherbiras = teherbiras

    def auto_info(self):
        return f"Teherautó: {self.tipus}, Rendszám: {self.rendszam}, Évjárat: {self.evjarat}, Bérleti díj: {self.berleti_dij} HUF/nap, Teherbírás: {self.teherbiras} tonna"


# Autokolcsonzo osztály (Fő osztály 1.4 Kész)
class Autokolcsonzo:
    def __init__(self, nev):
        self.nev = nev
        self.autok = []
        self.berlesek = []

    def auto_hozzaadasa(self, auto):
        self.autok.append(auto)

    def autok_listazasa(self):
        return [auto.auto_info() for auto in self.autok]

    def berles_hozzaadasa(self, berles):
        self.berlesek.append(berles)

    '''def auto_keresese_tipus_alapjan(self, tipus):
        for auto in self.autok:
            if auto.tipus == tipus:
                return auto'''

    def auto_keresese_rendszam_alapjan(self, rendszam):
        for auto in self.autok:
            if auto.rendszam == rendszam:
                return auto
        return None


    def berles_torlese(self, auto, vissza_datum):
        for berles in self.berlesek:
            if berles.auto == auto:
                self.berlesek.remove(berles)
                auto.berelve = False
                napok = (vissza_datum - berles.datum).days
                if napok < 1:
                    napok = 1
                fizetendo = napok * auto.berleti_dij
                print(f"A(z) {auto.tipus} típusú autó vissza lett adva. "
                      f"Fizetendő összeg: {fizetendo} HUF ({napok} nap).")
                return True
        print(f"Nincs ilyen bérlés.")
        return False

    def berlesek_listazasa(self):
        return [berles.berles_info() for berles in self.berlesek]


# Berles osztály (Fő osztály 1.5 Kész)
class Berles:
    def __init__(self, auto, datum):
        self.auto = auto
        self.datum = datum

    def berles_info(self):
        return f"Autó: {self.auto.tipus}, Bérlés kezdete: {self.datum}"


# Szövegbevitel funkció (Extra 9.1 Kész)
def szoveg_bevitel(prompt):
    fut = True
    bevitel = ''
    while fut:
        ablak.fill(FEHER)

        prompt_szoveg = font.render(prompt, True, FEKETE)
        ablak.blit(prompt_szoveg, (50, 50))

        # Bevitt szöveg megjelenítése
        bevitel_szoveg = font.render(bevitel, True, KEK)
        ablak.blit(bevitel_szoveg, (50, 100))

        vissza_gomb = pygame.Rect(50, 150, 285, 50)
        pygame.draw.rect(ablak, KEK, vissza_gomb)
        vissza_szoveg = font.render("|| Vissza a főmenübe ||", True, FEHER)
        ablak.blit(vissza_szoveg, (vissza_gomb.x + 10, vissza_gomb.y + 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and vissza_gomb.collidepoint(event.pos):
                return "vissza"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    fut = False
                elif event.key == pygame.K_BACKSPACE:
                    bevitel = bevitel[:-1]
                else:
                    bevitel += event.unicode

        pygame.display.flip()

    return bevitel


# Pygame megjelenítő (Extra 9.2)
def megjelenito(kolcsonzo):
    fut = True
    while fut:
        ablak.fill(FEHER)

        # Fő menü
        cim_szoveg = font.render("Autókölcsönző rendszer", True, FEKETE)
        ablak.blit(cim_szoveg, (ablak_tuple[1] // 4 - cim_szoveg.get_width() // 2, 50))

        gomb_auto_lista = pygame.Rect(ablak_tuple[0] // 5 - 100, 150, 225, 50)
        gomb_berles_auto = pygame.Rect(ablak_tuple[0] // 5 - 100, 220, 225, 50)
        gomb_berles_lista = pygame.Rect(ablak_tuple[0] // 5 - 100, 290, 225, 50)
        gomb_visszaadas = pygame.Rect(ablak_tuple[0] // 5 - 100, 360, 225, 50)
        gomb_kilepes = pygame.Rect(ablak_tuple[0] // 5 - 100, 430, 225, 50)

        pygame.draw.rect(ablak, KEK, gomb_auto_lista)
        pygame.draw.rect(ablak, KEK, gomb_berles_auto)
        pygame.draw.rect(ablak, KEK, gomb_berles_lista)
        pygame.draw.rect(ablak, KEK, gomb_visszaadas)
        pygame.draw.rect(ablak, KEK, gomb_kilepes)

        auto_lista_szoveg = font.render("Autók listázása", True, FEHER)
        ablak.blit(auto_lista_szoveg, (gomb_auto_lista.x + 25, gomb_auto_lista.y + 10))

        berles_auto_szoveg = font.render("Autó bérlése", True, FEHER)
        ablak.blit(berles_auto_szoveg, (gomb_berles_auto.x + 35, gomb_berles_auto.y + 10))

        berles_lista_szoveg = font.render("Bérlések listázása", True, FEHER)
        ablak.blit(berles_lista_szoveg, (gomb_berles_lista.x + 10, gomb_berles_lista.y + 10))

        visszaadas_szoveg = font.render("Autó visszaadása", True, FEHER)
        ablak.blit(visszaadas_szoveg, (gomb_visszaadas.x + 10, gomb_visszaadas.y + 10))

        kilepes_szoveg = font.render("Kilépés", True, FEHER)
        ablak.blit(kilepes_szoveg, (gomb_kilepes.x + 75, gomb_kilepes.y + 10))

        # Események kezelése
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fut = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if gomb_auto_lista.collidepoint(event.pos):
                    autok_megjelenitese(kolcsonzo)
                elif gomb_berles_auto.collidepoint(event.pos):
                    auto_berlese(kolcsonzo)
                elif gomb_berles_lista.collidepoint(event.pos):
                    berlesek_megjelenitese(kolcsonzo)
                elif gomb_visszaadas.collidepoint(event.pos):
                    auto_visszaadasa(kolcsonzo)
                elif gomb_kilepes.collidepoint(event.pos):
                    fut = False

        pygame.display.flip()


# Autók megjelenítése a Pygame felületén, foglaltság színek jelzése (Extra 9.3 Kész)
def autok_megjelenitese(kolcsonzo):
    fut = True
    while fut:
        ablak.fill(FEHER)
        y = 50
        for auto in kolcsonzo.autok:
            auto_szoveg = font.render(auto.auto_info(), True, FEKETE)
            ablak.blit(auto_szoveg, (100, y))

            # Pötty megjelenítése az autó foglaltsága alapján
            if auto.berelve:
                pygame.draw.circle(ablak, PIROS, (50, y + 15), 10)
            else:
                pygame.draw.circle(ablak, ZOLD, (50, y + 15), 10)

            y += 40

        vissza_gomb = pygame.Rect(50, y + 20, 360, 50)
        pygame.draw.rect(ablak, KEK, vissza_gomb)
        vissza_szoveg = font.render("|| Vissza a főmenübe ||", True, FEHER)
        ablak.blit(vissza_szoveg, (vissza_gomb.x + 50, vissza_gomb.y + 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if vissza_gomb.collidepoint(event.pos):
                    fut = False

        pygame.display.flip()


# Autó bérlése típus alapján, hibakezeléssel (Funkciók 2.1 Kész) (Adatvalidáció Kész)
def auto_berlese(kolcsonzo):

    rendszam = szoveg_bevitel("Add meg az autó rendszámát: ").upper()
    if rendszam == "vissza":
        return
    auto = kolcsonzo.auto_keresese_rendszam_alapjan(rendszam)

    if auto:
        if auto.berelve:
            print(f"A(z) {auto.rendszam} típusú autó már ki van bérelve.")
        else:
            while True:
                datum = szoveg_bevitel("Add meg a bérlés dátumát (ÉÉÉÉ-HH-NN): ")
                if datum == "vissza":
                    return
                try:
                    datum = datetime.strptime(datum, '%Y-%m-%d')
                    break
                except ValueError:
                    print("Érvénytelen dátumformátum! Kérlek, használd az ÉÉÉÉ-HH-NN formátumot.")

            uj_berles = Berles(auto, datum)
            kolcsonzo.berles_hozzaadasa(uj_berles)
            auto.berelve = True
            print(f"Bérlés sikeres: {auto.auto_info()} a {datum.date()} dátummal.")
    else:
        print("Nincs ilyen típusú autó a kölcsönzőben.")

# (Funkciók 2.2 Kész)
def auto_visszaadasa(kolcsonzo):
    rendszam = szoveg_bevitel("Add meg a visszaadni kívánt autó rendszamat: ").upper()
    if rendszam == "vissza":
        return
    auto = kolcsonzo.auto_keresese_rendszam_alapjan(rendszam)

    if auto:
        if auto.berelve:
            berles = next((b for b in kolcsonzo.berlesek if b.auto == auto), None)
            if berles:
                while True:
                    vissza_datum = szoveg_bevitel("Add meg a visszaadás dátumát (ÉÉÉÉ-HH-NN): ")
                    if vissza_datum == "vissza":
                        return
                    try:
                        vissza_datum = datetime.strptime(vissza_datum, '%Y-%m-%d')
                        if vissza_datum < berles.datum:
                            print("A visszaadás dátuma nem lehet korábbi, mint a bérlés dátuma!")
                        else:
                            break
                    except ValueError:
                        print("Érvénytelen dátumformátum! Kérlek, használd az ÉÉÉÉ-HH-NN formátumot.")
                kolcsonzo.berles_torlese(auto, vissza_datum)
            else:
                print(f"Nincs bérlés rögzítve a(z) {auto.tipus} típusú autóhoz.")
        else:
            print(f"A(z) {auto.tipus} típusú autó nincs kölcsönözve.")
    else:
        print("Nincs ilyen típusú autó a kölcsönzőben.")


# Bérlések megjelenítése  (Funkciók 2.3 Kész)
def berlesek_megjelenitese(kolcsonzo):
    fut = True
    while fut:
        ablak.fill(FEHER)
        berlesek = kolcsonzo.berlesek_listazasa()
        y = 50
        for berles in berlesek:
            berles_szoveg = font.render(berles, True, FEKETE)
            ablak.blit(berles_szoveg, (50, y))
            y += 40

        vissza_gomb = pygame.Rect(100, y + 10, 280, 50)
        pygame.draw.rect(ablak, KEK, vissza_gomb)
        vissza_szoveg = font.render(" || Vissza a főmenübe ||", True, FEHER)
        ablak.blit(vissza_szoveg, (vissza_gomb.x + 0, vissza_gomb.y + 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if vissza_gomb.collidepoint(event.pos):
                    fut = False

        pygame.display.flip()


# Program indítása
if __name__ == "__main__": #Meghatározása hogy a kódot közvetlenül vagy inportálva szeretnék-e felhasználni..

    kolcsonzo = Autokolcsonzo("CityCar Rent")

    # Toyota Yaris 2024 autók (5000 HUF/nap)
    auto1 = Szemelyauto("GDE-001", "Toyota Yaris 2024", 2024, 5000, "Fehér")
    auto2 = Szemelyauto("GDE-002", "Toyota Yaris 2024", 2024, 5000, "Szürke")
    auto3 = Szemelyauto("GDE-003", "Toyota Yaris 2024", 2024, 5000, "Bordó")
    auto4 = Szemelyauto("GDE-004", "Toyota Yaris 2024", 2024, 5000, "Pezsgő")
    auto5 = Szemelyauto("GDE-005", "Toyota Yaris 2024", 2024, 5000, "Fehér")

    # Skoda Octavia 2024 autók (6000 HUF/nap)
    auto6 = Szemelyauto("GDE-006", "Skoda Octavia 2024", 2024, 6000, "Bordó")
    auto7 = Szemelyauto("GDE-007", "Skoda Octavia 2024", 2024, 6000, "Pezsgő")
    auto8 = Szemelyauto("GDE-008", "Skoda Octavia 2024", 2024, 6000, "Fehér")
    auto9 = Szemelyauto("GDE-009", "Skoda Octavia 2024", 2024, 6000, "Szürke")
    auto10 = Szemelyauto("GDE-010", "Skoda Octavia 2024", 2024, 6000, "Bordó")
    auto11 = Szemelyauto("GDE-011", "Skoda Octavia 2024", 2024, 6000, "Pezsgő")

    # Ford Transit 2019 autók (7000 HUF/nap)
    auto12 = Teherauto("GDE-012", "Ford Transit 2019", 2019, 7000, 2)
    auto13 = Teherauto("GDE-013", "Ford Transit 2019", 2019, 7000, 2)
    auto14 = Teherauto("GDE-014", "Ford Transit 2019", 2019, 7000, 2)
    auto15 = Teherauto("GDE-015", "Ford Transit 2019", 2019, 7000, 2)
    auto16 = Teherauto("GDE-016", "Ford Transit 2019", 2019, 7000, 2)

    autok = [
        auto1, auto2, auto3, auto4, auto5, auto6, auto7, auto8, auto9, auto10,
        auto11, auto12, auto13, auto14, auto15, auto16
    ]

    for auto in autok:
        kolcsonzo.auto_hozzaadasa(auto)


    megjelenito(kolcsonzo)
    pygame.quit()
