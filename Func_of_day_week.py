"""Функция получает на вход текст вида: “1-й четверг ноября”, “3я среда мая” и т.п. Преобразуйте его в дату в текущем году."""
# Урок 15. Обзор стандартной библиотеки Python
# Первое задание
# Функция получает на вход текст вида: “1-й четверг ноября”, “3я среда мая” и т.п.
#  Преобразуйте его в дату в текущем году.
#  Логируйте ошибки, если текст не соответсвует формату.

#  Добавьте возможность запуска из командной строки.
#  При этом значение любого параметра можно опустить. 
#  В этом случае берётся первый в месяце день недели, текущий день недели и/или текущий месяц.

#  Научите функцию распознавать не только текстовое названия дня недели и месяца, но и числовые, т.е не мая, а 5.

import datetime
import logging
import sys



def get_this_day(string: str, mode = 0) -> datetime:
    """Функция получает на вход текст вида: “1-й четверг ноября”, “3я среда мая” и т.п. Преобразуйте его в дату в текущем году. 
    Если параметр mode != 0 то функция берет данные из командной строки """
    
    week_number = None
    week_day = None
    month_number = None

    month_list = ['января','февраля','марта','апреля','мая','июня','июля','августа','сунтября','октября','ноября','декабря']
    week_list = ['понедельник','вторник','среда','четверг','пятница','суббота','воскресенье']
    syff = ['-й','я','е']
    # Logging
    
    FORMAT = '{levelname:<6} - {asctime}. В модуле "{name}" \
    в строке {lineno:03d} функция "{funcName}()" в {created} секунд записала сообщение: {msg}'
    logging.basicConfig(filename='get_this_day.log' , filemode='w', encoding='utf-8' , format=FORMAT, style='{', level=logging.INFO)
    logger = logging.getLogger('main')
    if mode:
        string =''
        for index , param in enumerate(sys.argv):
            if index != 0:
                string = string + param + ' '
    
    if not string:  # Введенные данные это None 
        logger.error('Внимание! Некорректные данные')
        raise ValueError
    str_list = string.lower().rstrip().split(' ') # разбиваем строку на 3 составляющие номер дня, день недели и месяц

    if len(str_list) != 3:  # Проверяем, что в строке 3 параметра
        logger.error(f'Внимание! Некорректные данные! Колличество аргументов должно быть равно 3м')
        raise ValueError(f'Внимание! Некорректные данные! Колличество аргументов должно быть равно 3м')

    # проверяем что значения - цифровые и сразу присваеваем их
    if str_list[0].isdigit():
        if 0 < int(str_list[0]) < 6:
            week_number = int(str_list[0])
        else:
            logger.error(f'Внимание! Некорректные данные! В месяце может быть только пять пятниц!(это пример) (str_list[0])')
            raise ValueError(f'Внимание! Некорректные данные! В месяце может быть только пять пятниц!(это пример) (str_list[0])')
    if str_list[1].isdigit():
        if 0 < int(str_list[1]) < 8:
            week_day = int(str_list[1]) - 1
        else:
            logger.error(f'Внимание! Некорректные данные! В неделе только 7 дней (str_list[1])')
            raise ValueError(f'Внимание! Некорректные данные! В неделе только 7 дней (str_list[1])')
    if str_list[2].isdigit():
        if 0 < int(str_list[2]) < 13:
            month_number = int(str_list[2])
        else:
            logger.error(f'Внимание! Некорректные данные! В году 12 месяцев ({str_list[2]})')
            raise ValueError(f'Внимание! Некорректные данные! В году 12 месяцев ({str_list[2]})')

    # значения -  строковые проверяем на соответствие данных
    # Проверяем первый элемент строки
    index_num = 0   
    for index_num , syf in enumerate(syff):
        if str_list[0].find(syf) != -1:
            if 0 < int(str_list[0][ 0 : str_list[0].find(syf)]) < 6:
                week_number = int(int(str_list[0][0]))
                break
            else:
                logger.error(f'Внимание! Некорректные данные! В месяце может быть только пять пятниц!(это пример) ({str_list[0]})')
                raise ValueError(f'Внимание! Некорректные данные! В месяце может быть только пять пятниц!(это пример) ({str_list[0]})')
            
    if not week_number:
            logger.error(f'Внимание! Некорректные данные! Первый аргумент должен заканчиваться на \'-й\',\'я\',\'-ое\' ({str_list[0]})')
            raise ValueError(f'Внимание! Некорректные данные! Первый аргумент должен заканчиваться на \'-й\',\'я\',\'-ое\' ({str_list[0]})')
    
    # Проверяем второй элемент строки
    index_week_day = 0
    if str_list[1] not in week_list:
        logger.error(f'Внимание! Некорректные данные! Введите день недели!(понедельник , вторник) ({str_list[1]})')
        raise ValueError(f'Внимание! Некорректные данные! Введите день недели!(понедельник , вторник) ({str_list[1]})')
    else:
        for index_week_day , day_of_week in enumerate(week_list):
            if str_list[1] == day_of_week:
                week_day = index_week_day
                break
    # Проверяем синтаксис аргументов 1 и 2 (1-й четверг 2я пятница 3е воскресенье)
    # ['понедельник','вторник','среда','четверг','пятница','суббота','воскресенье']
    # syff = ['-й','я','е']
    print(f"{index_num = }    {index_week_day = }")
    if index_num == 0:
        if index_week_day not in [0 , 1 , 3]:
            error_str = str_list[0] + ' ' + str_list[1]
            logger.error(f'Внимание! Синтаксическая ошибка !!! (1-й четверг, 2я пятница, 3е воскресенье)  ({error_str}) ')
            raise ValueError(f'Внимание! Синтаксическая ошибка !!! (1-й четверг, 2я пятница, 3е воскресенье)  ({error_str}) ')
    elif index_num == 1:
        if index_week_day not in [2 , 4 , 5]:
            error_str = str_list[0] + ' ' + str_list[1]
            logger.error(f'Внимание! Синтаксическая ошибка !!! (1-й четверг, 2я пятница, 3е воскресенье)  ({error_str}) ')
            raise ValueError(f'Внимание! Синтаксическая ошибка !!! (1-й четверг, 2я пятница, 3е воскресенье)  ({error_str}) ')
    elif index_num == 2:
        if index_week_day != 6:
            error_str = str_list[0] + ' ' + str_list[1]
            logger.error(f'Внимание! Синтаксическая ошибка !!! (1-й четверг, 2я пятница, 3е воскресенье)  ({error_str}) ')
            raise ValueError(f'Внимание! Синтаксическая ошибка !!! (1-й четверг, 2я пятница, 3е воскресенье)  ({error_str}) ')
    else:
        logger.critical(f'Внимание! Внутренний програмный сбой!!! ')
        raise Exception(f'Внимание! Внутренний програмный сбой!!!')
    
    
    # Проверяем третий элемент строки
    if str_list[2] not in month_list:
        logger.error(f'Внимание! Некорректные данные! Введите месяц (январь , февраль ...) ({str_list[2]}) ')
        raise ValueError(f'Внимание! Некорректные данные! Введите месяц (январь , февраль ...) ({str_list[2]}) ')
    else:
        for index , month in enumerate(month_list):
            if str_list[2] == month:
                month_number = index + 1
            
    # Теперь у меня есть данные по дню недели и месяц
    # Определяю какой день недели 1 число указанного месяца
    # Нахожу разницу в днях между днями недели
    # И прибавляю кол-во недель до указанного номера 
    # Провожу общую сборку данных
    Week_ferst_day_of_this_month = datetime.date(year=datetime.datetime.now().year , month=month_number , day=1).weekday() # Определили какой день недели 1 число указанного месяца
    Week_day_of_this_month = week_day - Week_ferst_day_of_this_month + 7 * (week_number - 1) # Определяем разницу в днях
    logger.info(f'Успешное преобразование данных ({sting}) это данная дата: {datetime.date(year=datetime.datetime.now().year , month=month_number , day=1 + Week_day_of_this_month)}')
    return datetime.date(year=datetime.datetime.now().year , month=month_number , day=1 + Week_day_of_this_month)


if __name__ == '__main__':
    mode = 0
    if len(sys.argv) > 1:
        mode = 1
    print()
    sting = '3-й четверг августа'
    print(f' Ваш день это:      {get_this_day(sting, mode)}')

   
    










# Второе задание
#  Возьмите любые 1-3 задачи из прошлых домашних заданий.
#  Добавьте к ним логирование ошибок и полезной информации. 
# Также реализуйте возможность запуска из командной строки с передачей параметров.