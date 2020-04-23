import sys
import matplotlib
import matplotlib.pyplot as plot
import matplotlib.dates as dts
import datetime
import matplotlib.patches as patchs
from settings import SETTINGS as settings

def diagram(x_data, y_data, x_label="", y_label="", title=""):
    # создаем холст
    figure, axis = plot.subplots()

    axis.plot(x_data, y_data, lw = 1, color = '#01281A', alpha = 1)

    axis.set_title(title)
    axis.set_xlabel(x_label)
    axis.set_ylabel(y_label)
    # сохраняем диаграмму 
    figure.savefig('diagram.png')

def statistics(data):
    # функция изобразит график разброса зависимости траффика  от времени 
    # и диаграмму зависимости траффика  от времени

    # обновляем параметры полотна
    plot.rcParams.update({"figure.titlesize": 16})
    plot.rcParams.update({"figure.figsize": (16,10)})
    plot.rcParams.update({"axes.labelsize": 16})
    plot.rcParams.update({"axes.titlesize":16})
    plot.rcParams.update({"legend.fontsize":16})
    plot.rcParams.update({"xtick.labelsize":12})
    plot.rcParams.update({"ytick.labelsize":16})

    # коэффициент 1/1024 для указания объема трафика
    coef = 0.000976563
    
    x = []
    y = []

    # сортируем время по возрастанию
    data_keys = list(data.keys())
    data_keys.sort()
    traffic = 0

    # формируем данные для координатных осей
    for i in data_keys:
        traffic += data[i]
        x.append(datetime.datetime.strptime(i,"%Y-%m-%d %H:%M:%S"))
        y.append(traffic*coef)
    
    # вызова функции для отрисовки диаграммы
    diagram(x,y,"Time","Traffic (Kb)","Traffic over time")
    
    dn = dts.date2num(x)

    # создаём фигуру
    plot.figure(figsize=(16,10), dpi= 80, facecolor='w', edgecolor='k')

    # задаём настройки график разброса
    plot.xticks(rotation = 14)
    axis = plot.gca()
    axis.set(xlabel = "Time", ylabel = "Traffic(Kb)")
    fmt = dts.DateFormatter('%Y-%m-%d %H:%M:%S')
    axis.xaxis.set_major_formatter(fmt)
    axis.xaxis.set_major_locator(dts.MinuteLocator(interval=10))
    plot.scatter(dn, y, s=20, c='tab:blue', label="Traffic, Kb")
    plot.title("Traffic over time", fontsize = 27)
    plot.legend(fontsize=16)
    # сохраняем график разброса 
    plot.savefig("scatter.png", bbox_inches="tight")

data = []

with open("traffic.csv", "r") as file:
    for line in file:
        data.append(line.split(","))

# IP-адрес из условия Вра
IP = settings["IP"]
k = settings["COST"]
traffic = 0
trafic_range = []
data_mas = {}
for i in range(len(data)-3):
    line = data[i]
    ts = line[0]
    sa = line[3]
    da = line[4]
    ibyt = line[12]
    if sa == IP or da == IP:
        if not ts in data_mas:
            data_mas[ts] = int(ibyt)
        else:
            data_mas[ts] = data_mas[ts] + int(ibyt)
        
        traffic += int(ibyt)

statistics(data_mas)

traffic /= 1024*1024

print(round(traffic * k, 2))



