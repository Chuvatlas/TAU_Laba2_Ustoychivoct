import matplotlib.pyplot as pyplot
import control.matlab as matlab
import numpy as numpy
from sympy import *
import math
import colorama as color


def graph(name):
    pyplot.subplot()
    pyplot.grid(True)
    if name == 'Переходная характеристика':
        [y, x] = matlab.step(W)
        pyplot.plot(x, y, 'red')
        pyplot.title(name)
        pyplot.ylabel('Magnitude')
        pyplot.xlabel('Time (s)')
    elif name == 'Годограф Найквиста':
        pyplot.plot()
        pyplot.title(name)
        W_ny = matlab.nyquist(W_raz)
    elif name == 'Годограф Михайлова':
        # x = [U.subs({w: q}) for q in numpy.arange(0, 0.75, 0.01)]
        # y = [V.subs({w: q}) for q in numpy.arange(0, 0.75, 0.01)]
        x = [U.subs({w: q}) for q in numpy.arange(0, 0.2, 0.01)]
        y = [V.subs({w: q}) for q in numpy.arange(0, 0.2, 0.01)]
        print('Начальная точка M(%s, %s)'%(U.subs({w: 0}), V.subs({w: 0})))
        pyplot.plot(x, y, 'green')
        pyplot.title(name)
        pyplot.ylabel('V(w)')
        pyplot.xlabel('U(w)')
    elif name == 'ЛАЧХ и ЛФЧХ':
        pyplot.plot()
        pyplot.title(name)
        mag, phase, omega = matlab.bode(W_raz, dB=True)
    pyplot.show()

Step_Response = 'Переходная характеристика'
Nyquist_Hodograph = 'Годограф Найквиста'
Michailov_Hodograph = 'Годограф Михайлова'
Log_Freq_Characteristics = 'ЛАЧХ и ЛФЧХ'

needNewChoice = True

while needNewChoice:
    userInput = input('Введите номер команды: \n'
                      '1 - ' + Step_Response + ';\n'
                      '2 - ' + Nyquist_Hodograph + ';\n'
                      '3 - ' + Michailov_Hodograph + ';\n'
                      '4 - ' + Log_Freq_Characteristics + ';\n')
    if userInput.isdigit():
        needNewChoice = False
        userInput = int(userInput)
        if userInput == 1:
            name = 'Переходная характеристика'
            W = matlab.tf([21], [200, 105, 40/21, 1])
            print('Передаточная функция САУ : \n %s' % W)
            print("Полюса: \n %s" % matlab.pole(W))
            graph('Переходная характеристика')
        elif userInput == 2:
            name = 'Годограф Найквиста'
            W_raz = matlab.tf([42, 0], [200, 105, 18, 1])
            # W_raz = matlab.tf([-338/21, 0], [200, 105, 18, 1])
            print('Передаточная функция разомкнутой САУ : \n %s' % W_raz)
            graph('Годограф Найквиста')
        elif userInput == 3:
            name = 'Годограф Михайлова'
            w = symbols('w', real=True)
            # s_замк = factor((8 * I * w + 1) * (5 * I * w + 1) ** 2 + 42 * I * w)
            s_замк = factor((8 * I * w + 1) * (5 * I * w + 1) ** 2 - (338/21) * I * w)
            print('Характеристическое уравнение замкнутой системы -\n%s' % s_замк)
            U = re(s_замк)
            V = im(s_замк)
            print('Действительная часть U(w)= %s' % U)
            print('Мнимая часть V(w)= %s' % V)
            graph('Годограф Михайлова')
        elif userInput == 4:
            name = 'ЛАЧХ и ЛФЧХ'
            W_raz = matlab.tf([42, 0], [200, 105, 18, 1])
            # W_raz = matlab.tf([-338/21, 0], [200, 105, 18, 1])
            graph('ЛАЧХ и ЛФЧХ')

        else:
            print(color.Fore.RED + '\nНедопустимое числовое значение!')
            needNewChoice = True

    else:
        print(color.Fore.RED + '\nПожалуйста, введите числовое значение!')
        needNewChoice = True