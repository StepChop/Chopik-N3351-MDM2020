# Вариант 7

import sys

# коэффициент звонков до 0:30
BCOST = 4.0 
# коэффициент звонков до 0:30
ACOST = 2.0
# коэффициент СМС
SMSCOST = 1.5

# Время, отноительно которого изменяется коэффциент
TIMECONST = "00:30:00"

# номер из варианта 7
DEFAULT_PHONE = "933156729"

# Считываем данные из файла
mas = []
with open("./data.csv") as cdr:
    for line in cdr:
        mas.append(line[:len(line)-1].split(','))

phone = input("Пожалуйста, введите номер для тарификации:\n")
# если не введен другой номер, используется номер из варианта 7
if not phone.isdigit():
    print("Введенный номер не соответствует формату.\nБудет протарифицирован номер 933156729")
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
            print("Ошибка в call_duration")
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
            print("Ошибка в call_duration")
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

print(round(sum, 2))