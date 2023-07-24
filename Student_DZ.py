""" Создайте класс студента.
    Используя дескрипторы проверяйте ФИО на первую заглавную букву и наличие только букв.
    Названия предметов должны загружаться из файла CSV при создании экземпляра. Другие предметы в экземпляре недопустимы.
    Для каждого предмета можно хранить оценки (от 2 до 5) и результаты тестов (от 0 до 100).
    Также экземпляр должен сообщать средний балл по тестам для каждого предмета и по оценкам всех предметов вместе взятых."""



import csv
import logging
import os


class ErrorStudent(Exception):
    """Общий класс обработчик ошибок СУБД СТУДЕНТ"""
    pass

class ErrorStudentFileDtaNotFound(ErrorStudent):
    """Класс обработчик ошибок файла данных СУБД СТУДЕНТ"""
    def __init__(self) -> None:
        super().__init__('Ошибка 404!!! фаил базы данных dat.csv ненайден!!!!')

class ErrorStudentValue(ErrorStudent):
    """Класс обработчик ошибок ввода данных СУБД СТУДЕНТ"""
    def __init__(self , string_eror:str) -> None:
        super().__init__('Ошибка входных данных !!! '+ string_eror)
        #return 'Ошибка входных данных :'+ string_eror


class FIO:
    """Класс дескриптор для проверки ФИО на первую заглавную букву и наличие только букв"""

    def __set_name__(self, owner, name):
        self.param_name = 'S' + name

    def __set__(self, instance, value:str):   
        for ch in value:
            if not ch.isalpha():
                self.logger.error(f'Значение ({value}) должно состоять только из букв!')
                raise ErrorStudentValue(f'Значение ({value}) должно состоять только из букв!')
        if not str.istitle(value):
            self.logger.error(f'Значение ({value}) должно начинаться с заглавной буквы!')
            raise ErrorStudentValue(f'Значение ({value}) должно начинаться с заглавной буквы!')
        setattr(instance, self.param_name, value)
        
    def __get__(self, instance, owner):
        return getattr(instance, self.param_name)


class Ocenka:
    def __init__(self , min : int = 0 , max : int = 1) -> None:
        if not min: 
            self.min  = 0
        else:
            self.min = min
        if not max: 
            self.max  = 1 
        else:
            self.max = max

    def __set_name__(self, owner, name):
        self.param_name = 'S' + name

    def __get__(self, instance, owner):
        return getattr(instance, self.param_name)

    def __set__(self, instance, value):
        if not isinstance(value, int):
            self.logger.error(f'Значение {value} должно быть целым числом')
            raise ErrorStudentValue(f'Значение {value} должно быть целым числом')
        if  value < self.min:
            self.logger.error(f'Значение {value} должно быть больше или равно {self.min}')
            raise ErrorStudentValue(f'Значение {value} должно быть больше или равно {self.min}')
        if value > self.max:
            self.logger.error(f'Значение {value} должно быть меньше или равно {self.max}')
            raise ErrorStudentValue(f'Значение {value} должно быть меньше или равно {self.max}')
        setattr(instance, self.param_name, value)


class Student:
    """Класс Учись студент!!! Кто не работает тот ЕСТ"""
    first_name = FIO()
    name = FIO()
    last_name = FIO()
    __student_diary : dict[str, tuple[int , dict[str , int]]] ={}

    def __init__(self, first_name, name, last_name) -> None:
            
        FORMAT = '{levelname:<6} - {asctime}. В модуле "{name}" \
        в строке {lineno:03d} функция "{funcName}()" в {created} секунд записала сообщение: {msg}'
        logging.basicConfig(filename='Student.log' , filemode='w', encoding='utf-8' , format=FORMAT, style='{', level=logging.INFO)
        self.logger = logging.getLogger('main')
        self.first_name = first_name
        self.name = name
        self.last_name = last_name
        if os.path.exists('dat.csv'):
            reader = csv.reader(open('dat.csv' , 'r', newline='' , encoding='utf-8') ,dialect='excel',quoting=csv.QUOTE_ALL)
            count = 0
            list_key = []
            list_val = []
            for row  in reader:
                if not count:
                    list_key = row
                else:
                    if row:
                        list_val = row
                count += 1
            result_list_lav = []
            
            for element in list_val:    #element = "[4, {'test1': 45, 'test2': 100}]"
                worc_str = element[1:-1] #worc_str = "4, {'test1': 45, 'test2': 100}"
                str_lis_of_tests = worc_str[4:-1].split(', ') # str_lis_of_tests = ''test1': 45, 'test2': 100'
                line_dict = {}
                for el in str_lis_of_tests:
                    line_dict[el.split(':')[0][1:-1]] = int(el.split(':')[1][1:]) # line_dict = {'test1': 45, 'test2': 100}  
                result_list_lav.append((int(worc_str[0]), line_dict))# добавили 4 (оценка от 2 - 5) и {'test1': 45, 'test2': 100}
            for (key , value) in zip(list_key, result_list_lav):
                self.__student_diary[key] =  value
        else:
            self.logger.error(f'Ошибка 404!!! фаил базы данных dat.csv ненайден!!!!')
            raise ErrorStudentFileDtaNotFound

    @property            
    def get_full_name(self) -> str:            
        return f'{self.first_name} {self.name} {self.last_name}'       
    #Также экземпляр должен сообщать средний балл по тестам для каждого предмета и по оценкам всех предметов вместе взятых.
    
    @property
    def get_student_diarySTR(self) -> str:
        return f'{self.__student_diary}'
    def __str__(self) -> str:
        return f'Студент : {self.first_name} {self.name} {self.last_name}\n\Предметы: { [(key ,val) for key ,val in self.__student_diary.items()]} '
    @property
    def get_student_diaryDICT(self) -> dict:
        return self.__student_diary


PETIA = Student('Иванов', 'Петр', 'Горлович')
#print(PETIA)

#print(PETIA.get_student_diarySTR)
#IBRAGIM = Student('Гвинодзе', 'Ибрагим', 'Рафикович')
#print(PETIA.__students_diary['математика'][1]['test2'])
# print(PETIA.get_full_name)
#print(IBRAGIM)
print(PETIA.get_student_diaryDICT)