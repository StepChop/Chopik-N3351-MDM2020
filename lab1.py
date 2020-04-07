import sys
BCOST = 4.0
ACOST = 2.0
SMSCOST = 1.5
TIMECONST = "00:30:00"

DEFAULT_PHONE = "933156729"

mas = []
with open("./data.csv") as cdr:
    for line in cdr:
        mas.append(line[:len(line)-1].split(','))

phone = input("Пожалуйста, введите номер для тарификации:\n")
if not phone.isdigit():
    print("Введенный номер не соответствует формату.\nБудет протарифицирован номер 933156729")
    phone = DEFAULT_PHONE
sum = 0
calls_sum = 0
for line in mas:
    if line[1] == "933156729":
        # print("OUTPUT")
        datetime = line[0]
        time = datetime[datetime.find(":")-2:]
        # print(time)
        try:
            duration = float(line[3])
        except:
            # print("Ошибка в call_duration")
            sys.exit()

        # print("DURATION:", duration)
        sms = int(line[-1])
        # print("SMS_C:",sms)
        if time < TIMECONST:
            time = float(datetime[datetime.find(":")+1:datetime.rfind(":")]) + float(datetime[datetime.rfind(":")+1:])/60
            ost = 30.0 - time
            # print("OST:", ost)
            if duration > ost:
                after = duration - ost
                # print("AFTER:", after)
                calls_sum = ost * BCOST + after * ACOST
            else:
                calls_sum = duration * BCOST
        else:
            calls_sum = duration * ACOST
            # print("OUT_CALLS:", calls_sum)
        sum += calls_sum
        sms_sum = sms * SMSCOST
        # print("SMS_SUM:", sms_sum)
        sum += sms_sum
    elif line[2] == "933156729":
        # print("INPUT")
        datetime = line[0]
        time = datetime[datetime.find(":")-2:]
        # print(time)
        try:
            duration = float(line[3])
        except:
            # print("Ошибка в call_duration")
            sys.exit()

        # print("DURATION:", duration)
        if time < TIMECONST:
            time = float(datetime[datetime.find(":")+1:datetime.rfind(":")]) + float(datetime[datetime.rfind(":")+1:])/60
            ost = 30.0 - time
            # print("OST:", ost)
            if duration > ost:
                after = duration - ost
                # print("AFTER:", after)
                calls_sum = ost * BCOST + after * ACOST
            else:
                calls_sum = duration * BCOST
        else:
            calls_sum = duration * ACOST
        # print("IN_CALLS:", calls_sum)
        sum += calls_sum

print("TOTAL_SUM:", round(sum, 2))