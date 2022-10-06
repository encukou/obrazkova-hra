## Ukázková pythoní hra

## Komentáře s dvojím dvojkřížkem jsou od autora vzorové hry;
## ostatním doporučuju komentovat jen s jedním #.

## Potřebujeme několik knihoven:
## random na náhodná čísla: https://docs.python.org/3/library/random.html
import random
## a Pyglet na grafiku: https://pyglet.readthedocs.org/
import pyglet

## Na začátku souboru definujeme konstanty, aby pak bylo jasné co které číslo
## znamená: místo "8" napíšeme rozumné jméno, abychom věděli že jde třeba
## o počet sloupců šachovnice.

COLUMNS = 8         ## počet sloupců "šachovnice"
ROWS = 8            ## počet řádků "šachovnice"

SPACING = 20        ## mezera mezi jednotlivými políčky (v pixelech)
MOVE_SPEED = 5      ## rychlost animace přesouvání
EXPLODE_SPEED = 3   ## rychlost animace odstranění obrázku

# Další konstanty jsou specifické pro tuhle konkrétní hru:

## jména souborů
IMG_PATH = 'assets/animal-pack/PNG/Square without details/{}.png'
ACTIVE_PATH = 'assets/animal-pack/PNG/Square (outline)/{}.png'

## seznam zvířátek: tohle je seznam dvojic (n-tic), ve kterých je vždy jméno
## zvířátka a číslo, které říká kde je střed obrázku: když zvíře velké zuby
## (které přesahují dolů), je číslo kladné; když má velké uši
## (které přesahují nahoru), je číslo záporné. Víc viz funkce image_load.
ANIMAL_INFO = (
    ('snake', 25),
    ('penguin', 0),
    ('monkey', 0),
    ('giraffe', -45),
    ('panda', -25),
    ('pig', -15),
    ('hippo', -10),
    ('parrot', 0),
    ('rabbit', -65),
    ('elephant', 0),
)


## Teď si načteme potřebné obrázky.
## Pro automatizaci toho, co chceme udělat s každým načteným obrázkem,
## si na to uděláme funkci.

def image_load(filename, offset=0):
    """Načte obrázek z daného souboru

    offset určuje, o kolik je posunutý střed obrázku
    """
    ## Načteme obrázek
    img = pyglet.image.load(filename)
    ## Nastavíme "kotevní bod", který říká, kam se obrázek nakreslí.
    ## U nás je to prostředek obrázku, takže když Pygletu řekneme aby obrázek
    ## nakreslil na souřadnice (100, 200), tak na těchto souřadnicích bude
    ## střed obrázku.
    ## V x-ové ose (doprava/doleva) je to vždycky prostředek:
    img.anchor_x = img.width // 2
    ## V y-ové ose (nahoru/dolů) nám někdy nesedí střed obrázku a střed
    ## čtverce, takže je potřeba přičíst "offset"
    img.anchor_y = img.height // 2 + offset
    ## Jo, a anchor_x/anchor_y v Pygletu musí být celá čísla (int), proto
    ## používáme celočíselné dělení (//).

    ## Nakonec obrázek vrátíme – to je celkem důležité.
    return img

## Načteme normální (čtvercové) obrázky: pro každé jméno z ANIMAL_INFO
## jeden obrázek
pictures = [image_load(IMG_PATH.format(name))
            for name, offset in ANIMAL_INFO]
## Načteme aktivní obrázky (s vyčuhujícíma ušima/zubama): tady použijeme
## offset, druhý prvek z dvojice v ANIMAL_INFO
active_pictures = [image_load(ACTIVE_PATH.format(name), offset)
                   for name, offset in ANIMAL_INFO]
## Pak načteme obrázek, který pak použijeme jako pozadí k vybranému obrázku
active_bg_img = image_load('assets/puzzle-pack-2/PNG/Tiles grey/tileGrey_01.png')
## A na pozadí rovnou vytvoříme i sprite – objekt, který můžeme vykreslit.
bg_sprite = pyglet.sprite.Sprite(active_bg_img)


## Mimochodem, obrázky jsou stažené z těchto zdrojů, a jsou k dispozici
## pod licencí CC0 (http://creativecommons.org/publicdomain/zero/1.0/):
## - http://opengameart.org/content/animal-pack
## - http://opengameart.org/content/puzzle-pack-2-795-assets
## Díky autorovi (http://www.kenney.nl/)!


## To by byly konstanty.
## Další věc, kterou budeme potřebovat, je několik funkcí na převod souřadnic.
## Obrázky totiž budeme kreslit na obrazovku, kde se vzdálenosti měří
## v pixelech, ale pro logiku hry budeme číslovat políčka, takhle:

##
##  -------------------------------------------------------------------------
##  |        |        |        |        |        |        |        |        |
##  | (0, 7) | (1, 7) | (2, 7) | (3, 7) | (4, 7) | (5, 7) | (6, 7) | (7, 7) |
##  |        |        |        |        |        |        |        |        |
##  -------------------------------------------------------------------------
##  |        |        |        |        |        |        |        |        |
##  | (0, 6) | (1, 6) | (2, 6) | (3, 6) | (4, 6) | (5, 6) | (6, 6) | (7, 6) |
##  |        |        |        |        |        |        |        |        |
##  -------------------------------------------------------------------------
##  |        |        |        |        |        |        |        |        |
##  | (0, 5) | (1, 5) | (2, 5) | (3, 5) | (4, 5) | (5, 5) | (6, 5) | (7, 5) |
##  |        |        |        |        |        |        |        |        |
##  -------------------------------------------------------------------------
##  |        |        |        |        |        |        |        |        |
##  | (0, 4) | (1, 4) | (2, 4) | (3, 4) | (4, 4) | (5, 4) | (6, 4) | (7, 4) |
##  |        |        |        |        |        |        |        |        |
##  -------------------------------------------------------------------------
##  |        |        |        |        |        |        |        |        |
##  | (0, 3) | (1, 3) | (2, 3) | (3, 3) | (4, 3) | (5, 3) | (6, 3) | (7, 3) |
##  |        |        |        |        |        |        |        |        |
##  -------------------------------------------------------------------------
##  |        |        |        |        |        |        |        |        |
##  | (0, 2) | (1, 2) | (2, 2) | (3, 2) | (4, 2) | (5, 2) | (6, 2) | (7, 2) |
##  |        |        |        |        |        |        |        |        |
##  -------------------------------------------------------------------------
##  |        |        |        |        |        |        |        |        |
##  | (0, 1) | (1, 1) | (2, 1) | (3, 1) | (4, 1) | (5, 1) | (6, 1) | (7, 1) |
##  |        |        |        |        |        |        |        |        |
##  -------------------------------------------------------------------------
##  |        |        |        |        |        |        |        |        |
##  | (0, 0) | (1, 0) | (2, 0) | (3, 0) | (4, 0) | (5, 0) | (6, 0) | (7, 0) |
##  |        |        |        |        |        |        |        |        |
##  -------------------------------------------------------------------------
##
## Levé spodní políčko, (0, 0), se ale vykreslí na obrazovku na pixelové
## souřadnice třeba (50, 50).


def get_tile_size(window):
    """Vrátí velikost políčka pro dané okno, v pixelech"""
    ## Abychom do herního okýnka dostali určitý počet políček vedle sebe,
    ## vydělíme šířku okýnka počtem sloupců a dostaneme velikost políčka.
    ## Abychom tam dostali určitý počet políček pod sebe, vydělíme šířku
    ## okýnka počtem sloupců.
    ## Když chceme, aby se vešla celá šachovnice, vezmeme menší z těchto
    ## hodnot – tak zajistíme že se šachovnice vejde v obou směrech.
    return min(window.width / COLUMNS, window.height / ROWS)


def logical_to_screen(logical_x, logical_y, window):
    """Převede logické (herní) souřadnice na pixely.

    Vrací dvojici (x, y), souřadnice středu daného políčka.
    """
    ## Budeme potřebovat velikost políčka, kterou umí vypočítat funkce
    ## get_tile_size.
    tile_size = get_tile_size(window)
    ## Spočítáme si, kde bude levé spodní políčko – (0, 0).
    ## Chceme šachovnici uprostřed okýnka, takže na pravé i levé straně
    ## má být stejně velká mezera (mezi šachovnicí a okrajem okna).
    ## Celková šířka obou mezer je šířka okýnka minus šířka šachovnice;
    ## polovina toho je šířka jedné mezery.
    ## A šířka šachovnice je šířka políčka krát počet políček.
    start_x = (window.width - tile_size * COLUMNS) / 2
    # To samé pro y-ovou souřadnici.
    start_y = (window.height - tile_size * ROWS) / 2
    ## A kde budeme vykreslovat naše políčko? Od začátku šachovnice
    ## odpočítáme "X"-krát šířku políčka (a "Y"-krát výšku políčka),
    ## a dostaneme pixelovou souřadnici levého dolního rohu našeho políčka.
    ## A protože chceme střed políčka, přidáme půlku velikosti políčka.
    screen_x = start_x + logical_x * tile_size + tile_size / 2
    screen_y = start_y + logical_y * tile_size + tile_size / 2
    # A výsledek vrátíme.
    return screen_x, screen_y


def screen_to_logical(screen_x, screen_y, window):
    """Převede pixelové souřadnice na logické (herní).

    Vrací dvojici (x, y); potřebuješ-li celá čísla, je potřeba výsledek ještě
    zaokrouhlit.
    """
    ## Začátek je stejný jako u logical_to_screen.
    tile_size = get_tile_size(window)
    start_x = (window.width - tile_size * COLUMNS) / 2
    start_y = (window.height - tile_size * ROWS) / 2
    ## Potom vezmeme vzorečky pro screen_x a screen_y z logical_to_screen,
    ## a vyjádříme z nich logical_x a logical_y.
    logical_x = (screen_x - start_x) / tile_size - 1/2
    logical_y = (screen_y - start_y) / tile_size - 1/2
    # A výsledek vrátíme.
    return logical_x, logical_y


## Tak, to by byly funkce, kde se skrývá většina matematiky z téhle hry :)
## Teď si nadefinujeme třídy, které budeme ve hře používat. Budou to tyto:
## - Tile (políčko) obsahuje všechny informace o jednom políčku šachovnice.
##   Bude umět políǩo vykreslit, posunout animaci, a případně bude obsahovat
##   všechnu herní logiku která se vztahuje jenom na jedno políčko.
## - Board (šachovnice) bude obsahovat seznamy všech políček ve hře
##   a logiku vztahující se k několika políčkům (nebo k výběru konkrétního
##   políčka). A bude umět vykreslit celou šachovnici, nebo posunout všechny
##   animace.
## - Animace: několik tříd, které se budou starat o animace políček.

## Objekty třídy Tile si neuchovávají informaci o tom, kde na šachovnici
## se nacházejí. To může na některých místech způsobit trochu složitější program
## (třeba při vykreslování je potřeba pozici předat jako argument funkce),
## ale výhoda je ta, že informace o pozici každého políčka je v programu jen
## jednou (v objektu třídy Board). Kdyby byla stejná informace na víc místech,
## musí si programátor dávat pozor, aby si všechny výskyty vždy odpovídaly:
## když se něco změní na jednom místě, musí se to změnit i všude jinde.

class Tile:
    """Políčko šachovnice"""
    def __init__(self):
        ## Inicializační funkce
        ## Každé políčko může mít nastavenou jednu aktuální animaci.
        ## Když žádná animace neprobíhá, nastavíme políčko na None.
        self.animation = None
        ## Zbytek funkce je specifický pro naši hru.
        ## Každé políčko v této hře má číselnou hodnotu, které určuje
        ## jaké zvířátku na políčku je.
        ## Čím víc je možností, tím je hra těžší.
        self.value = random.randrange(8)
        ## Každé políčko má k dispozici dva "sprity" – obrázky, které
        ## se dají vykreslovat na danou pozici. Jeden s normálním obrázkem,
        ## jeden pro políčko které je zrovna pod myší.
        self.sprite = pyglet.sprite.Sprite(pictures[self.value])
        self.active_sprite = pyglet.sprite.Sprite(active_pictures[self.value])

    def draw(self, x, y, window, selected=False):
        """Vykreslí tohle políčko na obrazovku, na dané souřadnici

        Argumenty: x, y jsou souřadnice; window je okno do kterého kreslíme,
        selected je True pokud je tohle políčko aktivní (t.j. právě pod myší).
        """
        ## Nejdřív vybereme obrázek (sprite), který budeme používat
        if selected:
            sprite = self.active_sprite
        else:
            sprite = self.sprite
        ## Nastavíme pozici spritu podle toho, kam máme kreslit.
        screen_x, screen_y = logical_to_screen(x, y, window)
        sprite.x = screen_x
        sprite.y = screen_y
        ## Nastavíme velikost obrázku. To se dělá pomocí atributu "scale",
        ## který určuje jak moc se obrázek zvětší: scale=1 znamená normální
        ## velikost, scale=2 dvojnásobnou, scale=1/2 poloviční.
        ## My víme jak má být políčko velké – nebo aspoň na to máme funkci.
        ## Od velikosti políčka odečteme velikost mezery mezi obrázky,
        ## aby vyšla velikost samotného obrázku.
        tile_size = get_tile_size(window) - SPACING
        ## ... a víme jak je velký jeden obrázek (vezmeme třeba šířku prvního
        ## obrázku v seznamu, hada) ...
        img_width = pictures[0].width
        ## ... takže stačí tahle čísla podělit:
        sprite.scale = tile_size / img_width

        ## A nakonec obrázek vykreslíme. Je-li aktivní animace, použijeme ji;
        ## jinak jen nakreslíme obrázek.
        if self.animation:
            self.animation.draw(self, x, y, window)
        else:
            sprite.draw()

    def update(self, t):
        """Posune animaci políčka o "t" sekund dopředu.

        Vrací True, pokud animace skončila.
        """
        ## Všechno kolem animací nám zajišťuje speciální objekt, který máme
        ## v atributu "animation".
        ## Může tam ale být i None, takže se zeptáme jestli v tom
        ## atributu něco je:
        if self.animation:
            ## A jestli jo, posuneme příslušnou animaci dál. Metoda
            ## "animation.update" by měla vrátit True, když animace skončila...
            result = self.animation.update(t)
            ## ... a v takovém případě animaci zrušíme:
            if result:
                self.animation = None
            ## Vždycky ale výsledek vrátíme, aby ten, kdo tuhle metodu volal,
            ## měl přehled o tom, jestli animace už doběhla.
            return result


class Board:
    """Šachovnice s herní logikou"""
    def __init__(self):
        ## Inicializace: Vytvoříme seznam seznamů s objekty Tile.
        ## Bude to seznam sloupců šachovnice, kde každý sloupec je seznam
        ## jednotlivých políček.
        self.content = [[Tile() for i in range(ROWS)]
                        for j in range(COLUMNS)]
        ## Zbytek je specifický pro tuhle hru: vybíráme políčka myší:
        ## Budeme si pamatovat poslední pozici myši, v logických souřadnicích
        ## t.j. nad kterým políčkem myš právě je.
        ## Na začátku řekněme že je mimo šachovnici.
        self.last_mouse_pos = -1, -1
        ## Budeme si pamatovat právě vybrané políčko: to bude buď (x, y)
        ## v logických souřadnicích, nebo pokud políčko ještě hráč nevybral,
        ## tak None.
        self.selected_tile = None
        ## A taky si budeme pamatovat nějaká políčka "navíc": to jsou ty,
        ## které hráč odstranil, takže z pohledu herní logiky už neexistují,
        ## ale ještě u nich neskončila poslední animace.
        ## Tohle bude množina trojic (x, y, tile).
        self.extra_tiles = set()

        ## Teď uděláme ještě jednu věc: na začátku na šachovnici nechceme
        ## mít skupiny 3 a víc stejných zvířátek vedle sebe.
        ## Proto projdeme šachovnici a vždycky, když na takovou skupinu
        ## narazíme, zaměníme dané zvířátko za jiné.
        ## (Pokud čteš komentáře od začátku, doporučuju tenhle cyklus
        ## přeskočit a vrátit se k němu na konci.)
        for x, column in enumerate(self.content):
            for y, tile in enumerate(column):
                ## Vždycky zkusíme políčko změnit pětkrát, pak to vzdáme:
                ## je lepší malá šance na to že šachovnice nebude úplně
                ## "v pořádku", než aby se hra na začátku "zasekla" v nekonečné
                ## smyčce.
                for iteration in range(5):
                    area = self.check_area(x, y)
                    if len(area) >= 3:
                        ## Záměna políčka za nové
                        self.content[x][y] = Tile()
                    else:
                        break

    def draw(self, window):
        """Vykreslí celou šachovnici"""
        ## Nejdřív vykreslíme podklad pro vybrané políčko, pokud tedy
        ## nějaké vybrané je.
        if self.selected_tile is not None:
            ## Nastavíme spritu souřadnice
            logical_x, logical_y = self.selected_tile
            x, y = logical_to_screen(logical_x, logical_y, window)
            bg_sprite.x = x
            bg_sprite.y = y
            ## Nastavíme barvu: tahle trojice je (červená, zelená, modrá),
            ## a pomocí ní se celý obrázek ztmaví.
            ## 0 znamená že daná barva bude úplně chybět; 255 znamená
            ## žádné ztmavení.
            ## Takže (150, 150, 255) trochu ztmaví červenou a zelenou složku,
            ## a zůstane zelená.
            bg_sprite.color = 150, 150, 255
            ## Tak. Nakonec sprite vykreslíme.
            bg_sprite.draw()


        ## Teď projdeme celou šachovnici, a vykreslíme všechna políčka na ní.
        ## Použijeme funkci "enumerate", která bere nějakou sekvenci (např.
        ## seznam, a vrací sekvenci dvojic (index, prvek).
        ## Takže v tomhle cyklu bude "x" souřadnice (0, 1, 2, ...) a "column"
        ## sloupec:
        for x, column in enumerate(self.content):
            ## A v tomhle cyklu bude "y" souřadnice (0, 1, 2, ...) a "tile"
            ## už dané políčko.
            for y, tile in enumerate(column):
                ## Políčko stačí vykreslit.
                tile.draw(x, y, window)

        ## Teď vykreslíme políčko pod kurzorem ještě jednou, s "aktivním"
        ## obrázkem.
        ## (Využíváme toho, že aktivní obrázek úplně překryje ten neaktivní.
        ## Kdyby to tak nebylo, museli bychom v cyklu výše políčko pod kurzorem
        ## vynechat.)
        ## V last_mouse_pos máme logické souřadnice myši:
        x, y = self.last_mouse_pos
        ## Zkontrolujeme že myš je v šachovnici, a ne venku:
        if 0 <= x < COLUMNS and 0 <= y < ROWS:
            ## A pak vezmeme políčko a vykreslíme ho:
            tile = self.content[x][y]
            tile.draw(x, y, window, True)

        ## A nakonec vykreslíme "políčka navíc" z extra_tiles:
        for x, y, tile in self.extra_tiles:
            tile.draw(x, y, window)

    def action(self, x, y):
        """Udělá to, co se má stát po kliknutí na dané místo na šachovnici

        x a y jsou logické souřadnice
        """
        ## Kliknutí má efekt jen pokud hráč klikl dovnitř do šachovnice
        if not (0 <= x < COLUMNS and 0 <= y < ROWS):
            return
        ## Vezměme políčko, na které hráč kliknul
        current_tile = self.content[x][y]
        ## Pokud se tohle políčko právě animuje (padá, nebo se vyměňuje
        ## s jiným), tak kliknutí budeme ignorovat.
        if current_tile.animation:
            return
        ## Co uděláme dál závisí na tom, jestli už je něco vybrané.
        ## A je to specifické pro tuhle hru.
        if self.selected_tile is None:
            ## Když není vybrané nic, tak dané políčko prostě vybereme.
            self.selected_tile = x, y
        elif self.selected_tile == (x, y):
            ## Když je vybrané stejné políčko na jaké hráč kliknul,
            ## tak výběr zrušíme.
            self.selected_tile = None
        else:
            ## Jinak kliknuté a vybrané políčka vyměníme.
            ## Na to budeme potřebovat souřadnice toho druhého políčka:
            other_x, other_y = self.selected_tile
            ## Samotná výměna:
            self.content[x][y], self.content[other_x][other_y] = (
                self.content[other_x][other_y], self.content[x][y])
            ## Zbytek je nastavení animace.
            ## Když vyměňujeme políčka dál od sebe, animace by měla trvat
            ## trochu déle než když jsou těsně vedle sebe.
            ## Tohle není žádný exaktní vzorec – čísla jsou vybrána od oka,
            ## aby to vypadalo hezky.
            duration = ((x - other_x)**2 + (y - other_y)**2) ** 0.2
            ## Když máme dobu trvání animace, tak vyměněným políčkům
            ## přiřadíme nové animační objekty.
            self.content[x][y].animation = MoveAnimation(
                other_x, other_y, duration)
            self.content[other_x][other_y].animation = MoveAnimation(
                x, y, duration)
            ## A nakonec zrušíme výběr.
            self.selected_tile = None

    def update(self, t):
        """Posune animace v celé hře o "t" sekund"""
        ## Projdeme všechna políčka, a posuneme jejich animace:
        for x, column in enumerate(self.content):
            for y, tile in enumerate(column):
                result = tile.update(t)
                ## Když některému políčku animace skončila (update vrátilo
                ## True), nejspíš se dokončila výměna políček nebo obrázek
                ## dopadl zvrchu na místo.
                ## V takovém případě musíme zkontrolovat, jestli se tím
                ## nevytvořil shluk 3 a víc obrázků, a případně takový
                ## shluk odstranit.
                ## To je samozřejmě specifické pro tuhle hru.
                if result:
                    self.check_and_remove_area(x, y)

        ## Nakonec ještě posuneme animace u políček navíc.
        ## Jakmile u některého z nich animace skončí, už ho nebudeme
        ## potřebovat: odstraníme ho z "extra_tiles".
        ## Pozor: tady chci měnit množinu, přes kterou právě iteruji
        ## příkazem "for". To se v Pythonu nesmí – zmátlo by ho to;
        ## nevěděl by přes které prvky už přešel a přes které ne.
        ## Proto uděláme z množiny seznam, a ve "for" použijeme ten:
        ## seznam má na začátku stejné prvky, ale když něco odebereme
        ## z množiny, nezmizí to ze seznamu (a naopak).
        for x, y, tile in list(self.extra_tiles):
            result = tile.update(t)
            if result:
                self.extra_tiles.remove((x, y, tile))

    def check_area(self, x, y):
        """Vrátí shluk sousedních stejných obrázků na souřadnicích (x, y)

        Vrátí množinu souřadnic.
        """
        ## Tahle funkce je složitá; většina her na šachovnici takovouhle
        ## složitou funkci nepotřebuje. Ale je to hezká ukázka algoritmu:

        ## Na začátku si nastavíme shluk na prázdnou množinu; budeme ji
        ## postupně plnit
        area = set()
        ## Potom si uděláme množinu políček, které ještě chceme prozkoumat.
        ## Pro začátek do ní dáme souřadnice startovacího políčka.
        to_check = {(x, y)}
        ## A taky zjistíme, jaké obrázky hledáme: stejné jako má startovací
        ## políčko.
        value = self.content[x][y].value
        ## A pak cyklíme dokud je co prozkoumávat.
        while to_check:
            ## Vybereme souřadnice nějakého ještě neprozkoumaného políčka...
            x, y = to_check.pop()
            ## ... dáme ho do vznikající množiny (protože víme, že
            ## do "to_check" dáváme jen souřadnice políček se stejným
            ## obrázkem)...
            area.add((x, y))
            ## A pak zkontrolujeme políčka vlevo, vpravo, nahoře a dole od
            ## toho políčka.
            for x, y in (x+1, y), (x-1, y), (x, y+1), (x, y-1):
                ## Abychom mohli políčko přidat do shluku, musí:
                ## 1. tam ještě nebýt,
                ## 2. být v šachovnici, ne venku,
                ## 3. mít stejný obrázek jako zbytek shluku, a
                ## 4. nebýt animované (to by znamenalo, že např. ještě padá)
                ## (Poznámka: operátor "and" se nedívá na to, co je za ním,
                ## pokud předchozí podmínka neplatí. Proto potom, co
                ## zkontrolujeme že dané souřadnice jsou v šachovnici,
                ## už můžeme přistupovat k políčku – self.content[x][y].)
                if ((x, y) not in area and
                        0 <= x < COLUMNS and 0 <= y < ROWS and
                        self.content[x][y].value == value and
                        not self.content[x][y].animation):
                    ## Když to všechno platí, zaznamenáme si že se na něj
                    ## máme podívat.
                    to_check.add((x, y))
        ## Když už není co prozkoumávat, asi máme celý shluk! Vraťme ho.
        return area

    def check_and_remove_area(self, x, y):
        """Odstraní shluk na daných souřadnicích, je-li moc velký"""
        ## Tahle funkce je taky celkem složitá, a specifická pro tuhle hru.

        ## Zjistíme, co je ve shluku
        area = self.check_area(x, y)
        ## A je-li moc velký, smažeme ho...
        if len(area) >= 3:
            ## Postupujeme po sloupcích; pro každý sloupec shora dolů.
            for x in range(COLUMNS):
                ## Budeme si pamatovat, o kolika vymazaných políčkách už
                ## víme, nebo-li o kolik políček musí obrázek, který patří
                ## na právě procházené místo, spadnout.
                removed = 0
                ## Navštívíme každé políčko v sloupci, odspodu (od 0) nahoru.
                for y in range(ROWS):
                    ## Dokud je políčko o "removed" nad tím aktuálním ("y"),
                    ## zvyšujeme "removed".
                    ## Na konci tohoto cyklu bude "y + removed" řádek, ze
                    ## kterého spadne obrázek na právě procházené místo "y".
                    while (x, y + removed) in area:
                        removed += 1
                    ## Pokud jsme na políčku, které je smazáváno,
                    ## dáme ho do množiny "extra_tiles" a nastavíme mu
                    ## příslušnou animaci.
                    if (x, y) in area:
                        self.extra_tiles.add((x, y, self.content[x][y]))
                        self.content[x][y].animation = ExplodeAnimation()
                    ## Jinak, pokud na právě procházené místo
                    ## má spadnout jiný obrázek ...
                    if removed:
                        ## ... jsou dvě možnosti. Buď tam posuneme už
                        ## existující:
                        if y + removed < ROWS:
                            self.content[x][y] = self.content[x][y + removed]
                        else:
                            ## Nebo má nový obrázek spadnout z prostoru
                            ## nad šachovnicí, a musíme tedy přidat nový
                            ## obrázek.
                            self.content[x][y] = Tile()
                        ## V každém případě nastavíme "posouvací" animaci.
                        self.content[x][y].animation = MoveAnimation(
                            x, y + removed, duration=removed)


## Nakonec ještě nadefinujme třídy pro animace.

class MoveAnimation:
    """Animace posouvání z jednoho místa na druhé

    Argumenty:
        start_x, start_y: Počáteční souřadnice (logické)
        duration: Délka animace
    """
    def __init__(self, start_x, start_y, duration=1):
        ## Argumenty si překopírujeme do atributů objektu:
        self.start_x = start_x
        self.start_y = start_y
        self.duration = duration
        ## A pak nastavíme "pozici" animace; číslo které udává
        ## jak daleko už animace proběhla. Nula je úplný začátek;
        ## 1 je konec.
        self.pos = 0

    def update(self, t):
        """Posune animaci o "t" sekund dopředu

        Vrací True, pokud animace skončila.
        """
        ## Zvýšíme "pos", průběh animace, o daný počet sekund krát rychlost
        self.pos += t * MOVE_SPEED / self.duration
        ## A když je průběh větší než 1, animace skončila.
        if self.pos > 1:
            return True

    def draw(self, tile, x, y, window):
        """Vykreslí dané políčko s touto animací"""
        ## Spočítáme, kde má políčko být (v logických souřadnicích).
        ## Na začátku (pos=0) to je start_x/start_y, na konci (pos=1) je
        ## to zadaná pozice.
        logical_x = x * self.pos + self.start_x * (1 - self.pos)
        logical_y = y * self.pos + self.start_y * (1 - self.pos)
        ## Převedeme na pixelové souřadnice
        tile.sprite.x, tile.sprite.y = logical_to_screen(logical_x, logical_y,
                                                         window)
        ## A vykreslíme obrázek.
        tile.sprite.draw()


class ExplodeAnimation:
    """Animace zvětšování a zprůhledňování"""
    def __init__(self):
        ## Viz MoveAnimation.__init__
        self.pos = 0

    def update(self, t):
        """Posune animaci o "t" sekund dopředu

        Vrací True, pokud animace skončila.
        """
        self.pos += t * EXPLODE_SPEED
        ## Viz MoveAnimation.update
        if self.pos > 1:
            return True

    def draw(self, tile, x, y, window):
        """Vykreslí dané políčko s touto animací"""
        ## Velikost zvětšíme X-krát, kde X jde od 1 (na začátku animace)
        ## po 3 (na konci animace).
        tile.sprite.scale *= 1 + self.pos * 2
        ## Průhlednost obrázku jde od 255 (neprůhledný) po 0 (průhledný).
        tile.sprite.opacity = 255 * (1 - self.pos)
        ## Všechno je nastaveno, můžeme obrázek vykreslit.
        tile.sprite.draw()


## A teď už zbývá jen vytvořit objekt typu Board (což vytvoří celou
## šachovnici i s obsahem), nějaké to grafické okýnko, a říct Pygletu
## jak to všechno spolu souvisí.

def main():
    """Hlavní funkce programu – celá hra"""
    ## Vytvoříme si hru a okýnko
    board = Board()
    window = pyglet.window.Window()

    ## To, co se má stát když nastane nějaká událost, Pygletu řekneme
    ## pomocí dekorátoru @window.event.
    ## Ten udělá to, že přiřadí funkci k události stejného jména.
    ## Seznam událostí je v dokumentaci Pygletu:
    ## https://pyglet.readthedocs.org/en/pyglet-1.2-maintenance/api/pyglet/window/pyglet.window.Window.html
    ## (sekce Events)

    @window.event
    def on_draw():
        """Zavolá se, když je potřeba překreslit okno"""
        ## Smazat případný předchozí obsah
        window.clear()
        ## Vykreslit šachovnici
        board.draw(window)

    @window.event
    def on_mouse_motion(x, y, dx, dy):
        """Zavolá se, když hráč pohne myší"""
        ## Vezmeme si logické souřadnice
        logical_x, logical_y = screen_to_logical(x, y, window)
        ## Zaokrouhlíme je na celá čísla
        logical_x = round(logical_x)
        logical_y = round(logical_y)
        ## A pak nastavíme poslední známou pozici myši
        board.last_mouse_pos = logical_x, logical_y

    @window.event
    def on_mouse_press(x, y, button, modifiers):
        """Zavolá se, když hráč klikne myší"""
        ## Vezmeme si logické souřadnice
        logical_x, logical_y = screen_to_logical(x, y, window)
        ## Zaokrouhlíme je na celá čísla
        logical_x = round(logical_x)
        logical_y = round(logical_y)
        ## A delegujeme na šachovnici...
        board.action(logical_x, logical_y)

    @window.event
    def on_key_press(key, mod):
        """Zavolá se, když hráč stiskne klávesu"""
        ## To v téhle hře není potřeba, je to tu jen pro ukázku.
        if key == pyglet.window.key.UP:
            print('nahoru')
        elif key == pyglet.window.key.LEFT:
            print('doleva')
        elif key == pyglet.window.key.DOWN:
            print('dolů')
        elif key == pyglet.window.key.RIGHT:
            print('doprava')
        elif key == pyglet.window.key.ENTER:
            print('enter')

    ## Řekneme Pygletu, aby metodu "board.update" volal zhruba
    ## třicetkrát za sekundu
    pyglet.clock.schedule_interval(board.update, 1/30)

    ## A pak řekneme Pygletu, ať čeká na události a volá příslušné
    ## funkce.
    pyglet.app.run()

## 3, 2, 1... Start!
main()
