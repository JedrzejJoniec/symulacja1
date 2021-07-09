import math as np
import schedule
import time
import tkinter

# lista, dwa pierwsze to polozenie, dwa ostatnie to predkosc
u = [1.0, 0.0, 0.0, 0.0]
# masy
m1 = [0.1]
m2 = [0.1]
m12 = m1[0] + m2[0]
# mimośród
eccentricity = [0.1]
# lista, dwa pierwsze to wspolrzedne x i y pierwszej planety, dwa ostatnie to x i y drugiej planety
xy = [0.0, 0.0, 0.0, 0.0]
# stosunek mas i wartosci start i restart potrzebne do guzikow
q = m2[0] / m1[0]
start = [0]
restart = [0]
# szerekosc okna
animation_window_width = 1800
# wysokosc okna
animation_window_height = 1000
# x planety
animation_planet_start_xpos = 150
# y planety
animation_planet_start_ypos = 500
# promien planety
animation_planet_radius = 30
# szybkosc poruszania sie
animation_planet_min_movement = 5
# opoznienie miedzy klatkami
animation_refresh_seconds = 0.01


# poczatkowa predkosc
def initialVelocity():
    return np.sqrt((1 + q) * (1 + eccentricity[0]))


# funkcja zamieniajaca rownanie rozniczkowe drugiego stopnia do pierwszego stopnia
def derivative():
    du = [0.0, 0.0, 0.0, 0.0]
    r = u[0:2]
    rr = np.sqrt(np.pow(r[0], 2) + np.pow(r[1], 2))

    for i in range(0, 2):
        du[i] = u[i + 2]
        du[i + 2] = -(1 + q) * r[i] / (np.pow(rr, 3))

    return du


# metoda numeryczna obliczajaca polozenie i predkosc
def rungeKutta(h):
    a = [h / 2, h / 2, h, 0]
    b = [h / 6, h / 3, h / 3, h / 6]
    u0 = [0.0, 0.0, 0.0, 0.0]
    ut = [0.0, 0.0, 0.0, 0.0]
    dimension = 4
    for i in range(0, dimension):
        u0[i] = u[i]
        ut[i] = 0

    for j in range(0, dimension):
        du = derivative()
        for i in range(0, dimension):
            u[i] = u0[i] + a[j] * du[i]
            ut[i] = ut[i] + b[j] * du[i]

    for i in range(0, dimension):
        u[i] = u0[i] + ut[i]


# funkcja wyliczajaca polozenie na podstawie u[]
def calculateNewPosition():
    r = np.sqrt(np.pow(u[0], 2) + np.pow(u[1], 2))
   # r = 1
    a1 = (m2[0] / m12) * r
    a2 = (m1[0] / m12) * r

    x1 = -a2 * u[0]
    y1 = -a2 * u[1]
    x2 = a1 * u[0]
    y2 = a1 * u[1]
    print("-------------")
    print(x1)
    print(y1)
    print(x2)
    print(y2)
    print("-------------")
    xy[0] = x1
    xy[1] = y1
    xy[2] = x2
    xy[3] = y2


# funkcja tworzaca okno
def create_animation_window():
    window = tkinter.Tk()
    window.title("Animation")
    window.geometry(f'{animation_window_width}x{animation_window_height}')
    return window


# funkcja tworzaca canvas, przyciski i pola do wpisywania wartosci. Wstawia wszystko do okna
def create_animation_canvas(window):
    canvas = tkinter.Canvas(window)
    canvas.configure(bg="black")
    canvas.pack(fill="both", expand=True)
    canvas.create_window(1720, 75, window=entry_fields1(Window))
    canvas.create_window(1720, 45, window=entry_fields2(Window))
    canvas.create_window(1720, 15, window=entry_fields3(Window))
    name_label1 = tkinter.Label(window, text='eccentricity', font=('calibre', 10, 'bold'))
    name_label2 = tkinter.Label(window, text='M1', font=('calibre', 10, 'bold'))
    name_label3 = tkinter.Label(window, text='M2', font=('calibre', 10, 'bold'))
    button = tkinter.Button(window, text='Start', font=('calibre', 12, 'bold'), command=getstart)
    button2 = tkinter.Button(window, text='Stop', font=('calibre', 12, 'bold'), command=getstop)
    canvas.create_window(1602, 15, window=name_label1)
    canvas.create_window(1630, 75, window=name_label2)
    canvas.create_window(1630, 45, window=name_label3)
    canvas.create_window(1690, 105, window=button)
    canvas.create_window(1750, 105, window=button2)
    return canvas


# funkcje tworzace pola do wpisywania
def entry_fields1(window):
    entry1 = tkinter.Entry(window, text='Username', textvariable=namem1, font=('calibre', 10, 'normal'))
    return entry1


def entry_fields2(window):
    entry2 = tkinter.Entry(window, text='Username', textvariable=namem2, font=('calibre', 10, 'normal'))
    return entry2


def entry_fields3(window):
    entry3 = tkinter.Entry(window, text='Username', textvariable=nameecce, font=('calibre', 10, 'normal'))
    return entry3


# funkcja powiazana z przyciskiem start, obsluguje wartosic wpisywane do pól
def getstart():
    name1 = namem1.get()
    name1conv = float(name1)
    m1[0] = name1conv / 10

    name2 = namem2.get()
    name2conv = float(name2)
    m2[0] = name2conv / 10
    e = nameecce.get()

    name3conv = float(e)
    eccentricity[0] = name3conv

    if start[0] == 1:
        if restart[0] == 1:
            restart[0] = 0
        else:
            restart[0] = 1
        start[0] = 1
    else:
        start[0] = 1


# funkcja powiazana z przyciskiem stop, zatrzymuje dzialanie programu, z mozliwoscia wznowienia
def getstop():
    start[0] = 0


# funkcje tworzace planety
def animate_planet(canvas):
    planet = canvas.create_oval(450 - animation_planet_radius,
                                500 - animation_planet_radius,
                                450 + animation_planet_radius,
                                500 + animation_planet_radius,
                                fill="blue", tag="planet1", outline="blue", width=4)

    return planet


def animate_planet2(canvas):
    planet = canvas.create_oval(550 - animation_planet_radius,
                                500 - animation_planet_radius,
                                550 + animation_planet_radius,
                                500 + animation_planet_radius,
                                fill="red",tag="planet2", outline="red", width=4)

    return planet


# funkcja ktora jeszcze nie wiem co robi
def separationBetweenObjects():
    return 10 / (1 - eccentricity[0] - 0.0001)


# zainicjowanie predkosci
u[3] = initialVelocity()
# ustawienie wykonywania co sekunde funkcji obliczajacej pozycje i metody numerycznej
schedule.every(1).seconds.do(calculateNewPosition)
schedule.every(1).seconds.do(rungeKutta, 0.15)
# stworzenie okna, canvas i zmienne przechowujace dane z pol w ktorych mozna pisac
Window = create_animation_window()
namem1 = tkinter.StringVar()
namem2 = tkinter.StringVar()
nameecce = tkinter.StringVar()
Canvas1 = create_animation_canvas(Window)

# stworzenie planet
Planet1 = animate_planet(Canvas1)
Planet2 = animate_planet2(Canvas1)
# zmienne przechowujace polozenie planet dzieki ktorym mozna rysowac trajektorie
eloo1 = 550
eloo2 = 500
eloo3 = 550
eloo4 = 500
eloo5 = 450
eloo6 = 500
eloo7 = 450
eloo8 = 500
while True:
    if start[0] == 0:
        Window.update()
    elif restart[0] == 1:
        Canvas1.delete("planet2")
        Canvas1.delete("planet1")
        eloo1 = 550
        eloo2 = 500
        eloo3 = 550
        eloo4 = 500
        eloo5 = 450
        eloo6 = 500
        eloo7 = 450
        eloo8 = 500
        Canvas1.configure(bg="black")
        Planet1 = animate_planet(Canvas1)
        Planet2 = animate_planet2(Canvas1)
        u = [1.0, 0.0, 0.0, 0.0]
        u[3] = initialVelocity()
        xy = [0.0, 0.0, 0.0, 0.0]
        Window.update()
    else:
        schedule.run_pending()
        time.sleep(animation_refresh_seconds)
        eloo1 += xy[2]
        eloo2 += xy[3]
        eloo3 += xy[2]
        eloo4 += xy[3]
        eloo5 += xy[0]
        eloo6 += xy[1]
        eloo7 += xy[0]
        eloo8 += xy[1]
        Canvas1.create_oval(eloo1, eloo2, eloo3, eloo4, width=0, fill='red')
        Canvas1.create_oval(eloo5, eloo6, eloo7, eloo8, width=0, fill='blue')
        Canvas1.move(Planet1, xy[0], xy[1])
        Canvas1.move(Planet2, xy[2], xy[3])
        Window.update()
        time.sleep(animation_refresh_seconds)
