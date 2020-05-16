bill_settings = {

    'Банк получателя':
                        {
                            'значение':'БАНК СЕВЕРО-ВОСТОЧНЫЙ БАНК ПАО СБЕРБАНК Г. САНКТ - ПЕТЕРБУРГ', 
                            'ячейка':'bank_name'
                        }, 
    'БИК':
            {
                'значение':'044030653', 
                'ячейка':'BIK'
            }, 
    'счет банка':
                {
                    'значение':'30101810500000000653', 
                    'ячейка':'bank_account'
                }, 
    'счет поставщика':
                {
                    'значение':'40702810855000100555', 
                    'ячейка':'seller_account'
                }, 
    'ИНН':
            {
                'значение':'7707049388', 
                'ячейка':'INN'
            },
    'КПП':
            {
                'значение':'784243002', 
                'ячейка':'KPP'
            },
    'поставщик':
                    {
                        'значение':'Макрорегиональный филиал "Северо - Запад" ПАО "УТИПУТИ"', 
                        'ячейка':'client_snp'
                    },
    'покупатель':
                    {
                        'значение':'Чопик Степан Николаевич', 
                        'ячейка':'client_snp'
                    },

    'товары_1': 
                {
                    'значение':'Домашний интернет', 
                    'ячейка':'tovar_name_1'
                },
    'товары_2': 
                {
                    'значение':'Мобильная связь', 
                    'ячейка':'tovar_name_2'
                }, 

    'руководитель':
                    {
                        'значение':'Абрамчук М.В.', 
                        'ячейка':'main_director'
                    },
    'бухгалтер':
                    {
                        'значение':'Яковлева М.Н.', 
                        'ячейка':'main_counter'
                    }
}

traffic_settings = {
    "IP":"87.245.198.147",
    "COST":2,
    "input_filename":"G:\Stepa\Учёба\УМУ\Лаб 3\\traffic.csv"
}

mobile_settings = {
    "input_filename":"G:\Stepa\Учёба\УМУ\Лаб 3\data.csv",
    "BCOST": 4.0,
    "ACOST": 2.0,
    "SMSCOST": 1.5,
    "TIMECONST": "00:30:00",
    "DEFAULT_PHONE":"933156729"
}