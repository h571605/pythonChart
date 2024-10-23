import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons
import matplotlib.image as mpimg
import matplotlib.patches as mpatches

#Generater random data for a year
# centervals are values average values for each month
# samedata = false, new data each time program is called
import random
from random import randint
def GenereateRandomYearDataList(intencity:float, seed:int=0) -> list[int]:
    """
    :param intencity: Number specifying size, amplitude
    :param seed: If given, same data with seed is generated
    :return:
    """
    if seed != 0:
        random.seed(seed)
    centervals = [200,150,100, 75,75,75, 50, 75, 100, 150, 200, 250, 300]
    centervals = [x * intencity for x in centervals]
    nox = centervals[0]
    inc = True
    noxList = []
    for index in range(1,365):
        if randint(1, 100) > 50:
            inc = not inc
        center = centervals[int(index / 30)]
        dx = min(2.0, max(0.5, nox / center ))
        nox =  nox + randint(1,5) / dx if inc else nox - randint( 1, 5) * dx
        nox = max(10, nox)
        noxList.append(nox)
    return noxList

kron_nox_year = GenereateRandomYearDataList(intencity=1.0, seed = 1)
nord_nox_year = GenereateRandomYearDataList(intencity=.3, seed = 3)


#create figure and 3 axis
fig = plt.figure(figsize=(13, 5))

axNok = fig.add_axes((0.05, 0.05, 0.45, 0.9))
axInterval = fig.add_axes((0.4, 0.5, 0.1, 0.25))
axBergen = fig.add_axes((0.5, 0.05, 0.5, 0.9))

axInterval.patch.set_alpha(0.5)

coordinates_Nordnes = (70,30)
coordinates_Kronstad = (800, 850)
days_interval = (1,365)
marked_point = (0,0)



def on_day_interval(kvartal):
    global days_interval, marked_point
    axNok.cla()
    days_interval = (1,365)
    if kvartal == '2021':
        days_interval = (1,90)
    if kvartal == '2022':
        days_interval = (90, 180)
    if kvartal == '2023':
        days_interval = (180,270)
    if kvartal == '2024':
        days_interval = (270,365)
    marked_point = (0, 0)
    plot_graph()

def on_click(event) :
    global marked_point
    if ax := event.inaxes:
        if ax == axBergen:
            marked_point = (event.xdata, event.ydata)
            plot_graph()

#estimate NOX value based on the two measuring stations
def CalcPointValue(valN, valK):
    distNordnes = math.dist(coordinates_Nordnes, marked_point)
    distKronstad = math.dist(coordinates_Kronstad, marked_point)
    distNordnesKronstad = math.dist(coordinates_Nordnes, coordinates_Kronstad)
    val = (1 - distKronstad /(distKronstad+distNordnes)) * valK  + (1 - distNordnes /(distKronstad+distNordnes))* valN
    val = val * ( distNordnesKronstad / (distNordnes + distKronstad) ) ** 4

    #print (val)

    return val

# Make two circles in Nordnes and Kronstad
def draw_circles_stations():
    #blue circle
    circle = mpatches.Circle(coordinates_Nordnes, 50, color='blue')
    axBergen.add_patch(circle)

    #red circle
    circle = mpatches.Circle(coordinates_Kronstad, 50, color='red')
    axBergen.add_patch(circle)

def draw_label_and_ticks():
    num_labels = 12
    xlabels = ['J' ,'F' ,'M' ,'A' ,'M' ,'J', 'J', 'A', 'S', 'O', 'N', 'D']
    xticks = np.linspace(15, 345, num_labels)
    if days_interval[1] == 90:
        xticks = [15,45,75]
        xlabels = ['Jan', 'Feb', 'Mars']
    if days_interval[1] == 180:
        xticks = [15,45,75]
        xlabels = ['April', 'Mai', 'Juni']
    if days_interval[1] == 270:
        xticks = [15, 45, 75]
        xlabels = ['July', 'Aug', 'Sept']
    if days_interval[0] == 270:
        xticks = [15, 45, 75]
        xlabels = ['Okt', 'Nov', 'Des']
    axNok.set_xticks(xticks)
    axNok.set_xticklabels(xlabels)

def plot_graph():
    axNok.cla()
    axBergen.cla()
    nord_nox = nord_nox_year[days_interval[0]:days_interval[1]]
    kron_nox = kron_nox_year[days_interval[0]:days_interval[1]]
    days = len(nord_nox)
    list_days = np.linspace(1, days, days)


#draw the marked point & the orange graph
    l3 = None
    l4 = None
    # avarage nox values for stats in graph
    avarageNoxNordnes = 30
    avarageNoxKronstad = 90
    avarageNoxMarked = int(0)
    noxDifference = int(0)

    if marked_point != (0,0):
        nox_point = [CalcPointValue(nord_nox[i], kron_nox[i])  for i in range(days)]
        l3, = axNok.plot(list_days, nox_point, 'darkorange')
        l4, = axNok.plot('darkorange')
        circle = mpatches.Circle((marked_point[0], marked_point[1]), 50, color='orange')
        axBergen.add_patch(circle)

        for x in nox_point:
            avarageNoxMarked += x

        for x in nord_nox:
            avarageNoxNordnes += x

        for x in kron_nox:
            avarageNoxKronstad += x

        # avarage calc
        #marked
        avarageNoxMarked = round(avarageNoxMarked / len(nox_point))
        #nordnes
        avarageNoxNordnes = round(avarageNoxNordnes / len(nord_nox))
        #kronstad
        avarageNoxKronstad = round(avarageNoxKronstad / len(kron_nox))

        noxDifference = avarageNoxMarked - avarageNoxKronstad

    l1, = axNok.plot(list_days, nord_nox, 'blue')
    l2, = axNok.plot(list_days, kron_nox, 'red')
    axNok.set_title("NOX verdier")
    axInterval.set_title("År")



    lines = [l1, l2] if l3 is None else [l1,l2, l3, l4]
    axNok.legend(lines, [f"Nordnes {avarageNoxNordnes}%", f"Kronstad {avarageNoxKronstad}%", f"Markert plass {avarageNoxMarked}%", f"Markert plass - kronstad {noxDifference}%"])
    axNok.grid(linestyle='--')
    draw_label_and_ticks()

    #Plot Map of Bergen
    axBergen.axis('off')
    img = mpimg.imread('Bergen.jpg')
    img = axBergen.imshow(img)
    axBergen.set_title("Kart Bergen")
    draw_circles_stations();
    plt.draw()

plot_graph()

# draw radiobutton interval
listFonts = [12] * 5
listColors = ['yellow'] * 5
radio_button = RadioButtons(axInterval, ('2020',
                                          '2021',
                                          '2022',
                                          '2023',
                                          '2024'),
                            label_props={'color': listColors, 'fontsize' : listFonts},
                            radio_props={'facecolor': listColors,  'edgecolor': listColors},
                            )
axInterval.set_facecolor('darkblue')
radio_button.on_clicked(on_day_interval)
# noinspection PyTypeChecker
plt.connect('button_press_event', on_click)

plt.show()

