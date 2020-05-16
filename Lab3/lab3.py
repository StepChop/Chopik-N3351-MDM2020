from openpyxl import Workbook, load_workbook
from ru_number_to_text import *
import random
import datetime
from settings_2 import bill_settings, traffic_settings, mobile_settings
import os
import pdfkit
from jinja2 import Template

path_wkhtmltopdf = r'C:\\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

month = ['','января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
         'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']

def traffic(settings):
    data = []
    input_file = settings["input_filename"]
    with open(input_file, "r") as file:
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
            traffic += int(ibyt)

    traffic /= 1024*1024

    return round(traffic * k, 2)

def mobile(settings):
    BCOST = settings["BCOST"] 
    # коэффициент звонков до 0:30
    ACOST = settings["ACOST"]
    # коэффициент СМС
    SMSCOST = settings["SMSCOST"]

    # Время, отноительно которого изменяется коэффциент
    TIMECONST = settings["TIMECONST"]

    # номер из варианта 7
    DEFAULT_PHONE = settings["DEFAULT_PHONE"]

    input_filename = settings["input_filename"]
    # Считываем данные из файла
    mas = []
    with open(input_filename) as cdr:
        for line in cdr:
            mas.append(line[:len(line)-1].split(','))

    phone = DEFAULT_PHONE
    # если не введен другой номер, используется номер из варианта 7
    if not phone.isdigit():
        # print("Введенный номер не соответствует формату.\nБудет протарифицирован номер 933156729")
        phone = DEFAULT_PHONE
    sum = 0
    calls_sum = 0
    for line in mas:
        # Тарифицируем исходящие звонки и СМС для номера
        if line[1] == phone:
            
            datetime = line[0]
            time = datetime[datetime.find(":")-2:]
            
            try:
                duration = float(line[3])
                # print("Ошибка в call_duration")
            except:
                sys.exit()

        
            sms = int(line[-1])
            
            if time < TIMECONST:
                time = float(datetime[datetime.find(":")+1:datetime.rfind(":")]) + float(datetime[datetime.rfind(":")+1:])/60
                # Сколько осталось до 0:30
                ost = 30.0 - time
                # Если человек начал говорить раньше 0:30, а закончил позже, 
                # то находим соответствующие промежутки до(ost) и после(after)
                if duration > ost:
                    after = duration - ost
                    # Считаем стоимость промежутков по соответствующим коэффициентам
                    calls_sum = ost * BCOST + after * ACOST
                else:
                    # Иначе считаем по коэффициенту до 0:30
                    calls_sum = duration * BCOST
            else:
                # Если звонок начался после 0:30, то тарифицируем по коэффициенту после 0:30
                calls_sum = duration * ACOST
            sum += calls_sum
            sms_sum = sms * SMSCOST
            sum += sms_sum
        elif line[2] == phone:
            datetime = line[0]
            time = datetime[datetime.find(":")-2:]

            try:
                duration = float(line[3])
            except:
                # print("Ошибка в call_duration")
                sys.exit()

            if time < TIMECONST:
                time = float(datetime[datetime.find(":")+1:datetime.rfind(":")]) + float(datetime[datetime.rfind(":")+1:])/60
                # Сколько осталось до 0:30
                ost = 30.0 - time
                # Если человек начал говорить раньше 0:30, а закончил позже, 
                # то находим соответствующие промежутки до(ost) и после(after)
                if duration > ost:
                    after = duration - ost
                    # Считаем стоимость промежутков по соответствующим коэффициентам
                    calls_sum = ost * BCOST + after * ACOST
                else:
                    # Иначе считаем по коэффициенту до 0:30
                    calls_sum = duration * BCOST
            else:
                # Если звонок начался после 0:30, то тарифицируем по коэффициенту после 0:30
                calls_sum = duration * ACOST
            sum += calls_sum

    return round(sum, 2)

# Файл с шаблоном, временный файл, файл с результатом
input_filename = "G:\Stepa\Учёба\УМУ\Лаб 3\invoice.html"
temp_output = "G:\Stepa\Учёба\УМУ\Лаб 3\Счет.html"
output_filename = "G:\Stepa\Учёба\УМУ\Лаб 3\Счет.pdf"

# открываем на чтение файл с шаблоном и считываем содержимое
with open(input_filename, 'r', encoding='utf-8') as f:
    html = f.read()

# Рассчитываем стоимости услуг
traffic_cost = traffic(traffic_settings)
mobile_cost = mobile(mobile_settings)
total = traffic_cost + mobile_cost
total_rub = int(total//1)

# Выбираем правильные окончания рублей и копеек
rublei = "руб"
if total_rub % 100 in range(10, 20):
    rublei += "лей"
elif total_rub % 10 in [2,3,4]:
    rublei += "ля"
elif total_rub % 10 in [0, 5, 6, 7, 8, 9]:
    rublei += "лей"
elif total_rub % 10 == 1:
    rublei += "ль"

total_santi = int(round(total%1, 2)*100)
santi = "копе"
if total_rub % 100 in range(10, 20):
    santi += "ек"
elif total_rub % 10 in [2,3,4]:
    santi += "ки"
elif total_rub % 10 in [0, 5, 6, 7, 8, 9]:
    santi += "ек"
elif total_rub % 10 == 1:
    santi += "йка"

# переводим сумму в текст
total_text = num2text(total_rub)
total_text = total_text[:1].upper() + total_text[1:]

# формируем заголовок счета
today = datetime.datetime.now()
day = today.day
month = month[today.month]
year = today.year
bill_name = f"Счет на оплату № {random.randint(1, 1000)} от {day} {month} {year} г."


# настройки для pdf файла
options = {
    'page-size': 'A5',
    'margin-top': '2cm',
    'margin-left': '3cm',
    'margin-right': '2cm'
}

# Словарь для шаблонизатора
context = {
    "main_director":bill_settings["руководитель"]["значение"],
    "main_counter":bill_settings["бухгалтер"]["значение"],
    "bill_title":bill_name,
    "INN":bill_settings["ИНН"]["значение"],
    "KPP":bill_settings["КПП"]["значение"],
    "bank_account":bill_settings["счет банка"]["значение"],
    "bank_name":bill_settings["Банк получателя"]["значение"],
    "BIK":bill_settings["БИК"]["значение"],
    "total_text":total_text,
    "rublei":rublei,
    "total_santi":total_santi,
    "santi":santi,
    "total":total,
    "tovar_name_1":bill_settings["товары_1"]["значение"],
    "cost_1":traffic_cost,
    "tovar_name_2":bill_settings["товары_2"]["значение"],
    "cost_2":mobile_cost,
    "client_snp":bill_settings["покупатель"]["значение"],
    "seller":bill_settings["поставщик"]["значение"],
    "seller_account":bill_settings["счет поставщика"]["значение"]
}

template = Template(html)
output = template.render(context=context)

# temp_output - путь до временного файла с расширением html
# output_filename - путь до pdf 
with open(temp_output, 'wb') as f:
    f.write(output.encode('utf-8'))

pdfkit.from_file(temp_output, output_filename, options=options, configuration = config)
os.remove(temp_output)
print("Готово")