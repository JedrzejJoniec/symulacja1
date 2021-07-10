import math as np
import schedule
import time
import tkinter

# G = 1000000
# m1 = 0.001
# m2 = 0.001

G = 6.67e-11
m1 = [2.20e30]  # rząd masy słońca
m2 = [5.0e30]

# lista, dwa pierwsze to wspolrzedne x i y pierwszej planety, dwa ostatnie to x i y drugiej planety
xy = [450, 500, 550, 500]
dxy = [0.0, 0.0, 0.0, 0.0]
vxy = [1, 1, -1, -1]

# wartosci start i restart potrzebne do guzikow
start = [0]
restart = [0]

# szerekosc okna
animation_window_width = 1800
# wysokosc okna
animation_window_height = 1000
# promien planety
animation_planet_radius = 5
# opoznienie miedzy klatkami
animation_refresh_seconds = 0.01


# funkcja wyliczajaca polozenie i predkosc
def calculateNewPosition():
    gravconst = G * m1[0] * m2[0]

    dt = 0.1

    rx = xy[2] - xy[0]  # odleglosc pomiedzy planetami w x
    ry = xy[3] - xy[1]  # odleglosc pomiedzy planetami w y
    modr = np.sqrt(rx ** 2 + ry ** 2)  # dl wektora r
    unit_rx = rx / modr  # wektor jednostkowy
    unit_ry = ry / modr  # wektor jednostkowy

    fx = -gravconst / modr ** 2 * unit_rx
    fy = -gravconst / modr ** 2 * unit_ry

    scale = 1e-17  # przeskalowanie zeby miescilo sie na ekranie

    vxy[0] += -fx * dt / m1[0] * scale
    vxy[1] += -fy * dt / m1[0] * scale
    vxy[2] += fx * dt / m2[0] * scale
    vxy[3] += fy * dt / m2[0] * scale

    dxy[0] = vxy[0] * dt
    dxy[1] = vxy[1] * dt
    dxy[2] = vxy[2] * dt
    dxy[3] = vxy[3] * dt

    xy[2] += dxy[2]
    xy[3] += dxy[3]
    xy[0] += dxy[0]
    xy[1] += dxy[1]


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
    canvas.create_window(1720, 45, window=entry_fields2(Window))
    canvas.create_window(1720, 15, window=entry_fields3(Window))
    name_label2 = tkinter.Label(window, text='M1', font=('calibre', 10, 'bold'))
    name_label3 = tkinter.Label(window, text='M2', font=('calibre', 10, 'bold'))
    button = tkinter.Button(window, text='Start', font=('calibre', 12, 'bold'), command=getstart)
    button2 = tkinter.Button(window, text='Stop', font=('calibre', 12, 'bold'), command=getstop)
    canvas.create_window(1630, 45, window=name_label2)
    canvas.create_window(1630, 15, window=name_label3)
    canvas.create_window(1690, 105, window=button)
    canvas.create_window(1750, 105, window=button2)
    return canvas


# funkcje tworzace pola do wpisywania

def entry_fields2(window):
    entry2 = tkinter.Entry(window, textvariable=namem2, font=('calibre', 10, 'normal'))
    return entry2


def entry_fields3(window):
    entry3 = tkinter.Entry(window, textvariable=namem1, font=('calibre', 10, 'normal'))
    return entry3


# funkcja powiazana z przyciskiem start, obsluguje wartosic wpisywane do pól
def getstart():
    name1 = namem1.get()
    name1conv = float(name1)
    m1[0] = name1conv * 1e30
    name2 = namem2.get()
    name2conv = float(name2)
    m2[0] = name2conv * 1e30

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
    planet = canvas.create_oval(xy[0] - animation_planet_radius,
                                xy[1] - animation_planet_radius,
                                xy[0] + animation_planet_radius,
                                xy[1] + animation_planet_radius,
                                fill="blue", tag="planet1", outline="blue", width=4)

    return planet


def animate_planet2(canvas):
    planet = canvas.create_oval(xy[2] - animation_planet_radius,
                                xy[3] - animation_planet_radius,
                                xy[2] + animation_planet_radius,
                                xy[3] + animation_planet_radius,
                                fill="red", tag="planet2", outline="red", width=4)

    return planet


# ustawienie wykonywania co sekunde funkcji obliczajacej pozycje i metody numerycznej
schedule.every(int(animation_refresh_seconds)).seconds.do(calculateNewPosition)
# stworzenie okna, canvas i zmienne przechowujace dane z pol w ktorych mozna pisac
Window = create_animation_window()
namem1 = tkinter.StringVar()
namem2 = tkinter.StringVar()
Canvas1 = create_animation_canvas(Window)

# stworzenie planet
Planet1 = animate_planet(Canvas1)
Planet2 = animate_planet2(Canvas1)
# zmienne przechowujace polozenie planet dzieki ktorym mozna rysowac trajektorie

while True:
    # jesli nie wpisalismy mas i nie kliknelismy start
    if start[0] == 0:
        Window.update()
    # jesli kliknelismy dwa razy start, nastepuje restart
    elif restart[0] == 1:
        Canvas1.delete("planet2")
        Canvas1.delete("planet1")
        xy[2] = 550
        xy[3] = 500

        xy[0] = 450
        xy[1] = 500

        Canvas1.configure(bg="black")
        Planet1 = animate_planet(Canvas1)
        Planet2 = animate_planet2(Canvas1)
        Window.update()
    # anmiacja dziala
    else:
        schedule.run_pending()
        time.sleep(animation_refresh_seconds)
        print(xy[0], xy[1], vxy[0], vxy[1])
        print(xy[2], xy[3], vxy[2], vxy[3])
        print()

        Canvas1.create_oval(xy[2], xy[3], xy[2], xy[3], width=0, fill='red')
        Canvas1.create_oval(xy[0], xy[1], xy[0], xy[1], width=0, fill='blue')

        Canvas1.move(Planet1, dxy[0], dxy[1])
        Canvas1.move(Planet2, dxy[2], dxy[3])
        Window.update()
        time.sleep(animation_refresh_seconds)
