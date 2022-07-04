from random import random

"""Функция получает на вход строку, а на выходе 
рандомное число с плавающей точкой"""
def detector(str):
    return round(random(), 1)


if __name__ == '__main__':
    print(detector('test1'))
