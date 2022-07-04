import random

"""
Функция возращает рандомную запись из словаря
"""
def classifier(str):
    category =  {1: 'консультация', 
             2: 'лечение', 
             3: 'стационар', 
             4: 'диагностика', 
             5: 'лаборатория'}
    get_key = random.choice(list(category.keys())) #Получаем рандомный ключ
    return  {'service_class': get_key, 'service_name': category[get_key]}


if __name__ == '__main__':
    print(classifier('test'))
