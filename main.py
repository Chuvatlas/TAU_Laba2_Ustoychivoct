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
        [y, x] = matlab.step(w_closed)
        pyplot.plot(x, y, 'red')
        pyplot.title(name)
        pyplot.ylabel('Magnitude')
        pyplot.xlabel('Time (s)')
        pyplot.savefig('Step_response.png')
    elif name == 'Годограф Найквиста':
        pyplot.plot()
        pyplot.title(name)
        nyquist = matlab.nyquist(w_opened)
        pyplot.savefig('Nyquist.png')
    elif name == 'Годограф Михайлова':
        pyplot.title(name)
        pyplot.ylabel('V(w)')
        pyplot.xlabel('U(w)')
        pyplot.savefig('Michailov.png')
    elif name == 'Диаграмма Боде':
        pyplot.title(name)
        mag, phase, omega = matlab.bode(w_opened, dB=True)
        pyplot.savefig('Bode.png')
    pyplot.show()

def step_response(w_closed):
    name = 'Переходная характеристика'
    print('Передаточная функция САУ : \n %s' % w_closed)
    pyplot.subplot()
    pyplot.grid(True)
    graph(name)


def roots_equation(w_closed):
    name = 'Корни Х.У.'
    print('Передаточная функция САУ : \n %s' % w_closed)
    h = matlab.pzmap(w_closed)
    pyplot.grid(True)
    pyplot.show()
    pyplot.savefig('roots.png')
    print("Полюса: \n %s" % matlab.pole(w_closed))


def nyquist_plot(w_opened):
    name = 'Годограф Найквиста'
    print('Передаточная функция разомкнутой САУ : \n %s' % w_opened)
    graph(name)


def michailov_plot(w_closed):
    name = 'Годограф Михайлова'
    print('Передаточная функция САУ : \n %s' % w_closed)
    w = symbols('w', real=True)
    k_den = matlab.tfdata(w_closed)[1][0][0]
    n = len(k_den)
    D_jw = 0
    for a_n in k_den:
        n -= 1
        D_n = (a_n * (I * w) ** n)
        D_jw += D_n
    print('Характеристическое уравнение замкнутой системы -\n%s' % D_jw)
    U = re(D_jw)
    V = im(D_jw)
    print('Действительная часть U(w)= %s' % U)
    print('Мнимая часть V(w)= %s' % V)
    # x = [U.subs({w: q}) for q in numpy.arange(0, 0.75, 0.01)]
    # y = [V.subs({w: q}) for q in numpy.arange(0, 0.75, 0.01)]
    x = [U.subs({w: q}) for q in numpy.arange(0, 0.2, 0.01)]
    y = [V.subs({w: q}) for q in numpy.arange(0, 0.2, 0.01)]
    print('Начальная точка M(%s, %s)' % (U.subs({w: 0}), V.subs({w: 0})))
    pyplot.plot(x, y, 'green')
    graph(name)


def bode_diagram(w_opened):
    name = 'Диаграмма Боде'
    print('Передаточная функция разомкнутой САУ : \n %s' % w_opened)
    gm, pm, wg, wp = matlab.margin(w_opened)
    print('Запас устойчиовости по амплитуде:', gm, ';\n',
          'Запас устойчивости по фазе:', pm, ';\n',
          'Критическая частота составляет:', wg, ';\n',
          'Частота среза составляет:', wp, '.\n')
    graph(name)


def get_matrix_hurwitz(w_closed):
    k_den = matlab.tfdata(w_closed)[1][0][0]
    print(k_den)
    print(type(k_den))

    h = numpy.zeros((len(k_den) - 1, len(k_den) - 1), "float64")

    num_rows, num_cols = h.shape

    n = 0
    flg = True
    for j in range(num_rows):
        if (j % 2) == 0:
            for i in range(len(k_den)):
                if (i % 2) == 1:
                    numpy.put(h[j], [n], k_den[i])
                    if flg == True:
                        n += 1
                        flg = False
        flg = True

    n = 0
    flg = True
    for j in range(num_rows):
        if (j % 2) == 1:
            for i in range(len(k_den)):
                if (i % 2) == 0:
                    numpy.put(h[j], [n], k_den[i])
                    if flg == True:
                        n += 1
                        flg = False
        flg = True
    return h


def wave_limit_stability(w_closed):
    print('Передаточная функция САУ : \n %s' % w_closed)
    h = get_matrix_hurwitz(w_closed)
    print(h)
    det_h = numpy.linalg.det(h)
    print(det_h)
    k_fb = 2
    delta = 0.00000001
    step = 1
    while abs(det_h) > delta:
        if det_h < 0:
            k_fb += step
            step = step / 2
        else:
            k_fb -= step
        w1 = matlab.tf([k_fb, 0], [1])
        w_closed = matlab.feedback(w2 * w3 * w4, w1)
        w_opened = w1 * w2 * w3 * w4
        h = get_matrix_hurwitz(w_closed)
        det_h = numpy.linalg.det(h)
    print(w_closed, w_opened)
    return w_closed, w_opened

# Начало кода здесь
k_fb = int(input('Введите значение k_о.с.= '))

w1 = matlab.tf([k_fb, 0], [1])
w2 = matlab.tf([1], [8, 1])
w3 = matlab.tf([1], [5, 1])
w4 = matlab.tf([21], [5, 1])

w_closed = matlab.feedback(w2 * w3 * w4, w1)
w_opened = w1 * w2 * w3 * w4
userInput = input('Введите номер характеристики : \n'
                  '1 - Переходная характеристика' + ';\n'
                  '2 - Корни Х.У.' + ';\n'
                  '3 - Годограф Найквиста ' + ';\n'
                  '4 - Годограф Михайлова' + ';\n'
                  '5 - Диаграмма Боде' + ';\n'
                  '6 - Колебательная граница устойчивости' + '.\n')
if userInput.isdigit():
    userInput = int(userInput)
    if userInput == 1:
        step_plot = step_response(w_closed)
    elif userInput == 2:
        roots_equation = roots_equation(w_closed)
    elif userInput == 3:
        nyquist_plot = nyquist_plot(w_opened)
    elif userInput == 4:
        michailov_plot = michailov_plot(w_closed)
    elif userInput == 5:
        bode_diagram = bode_diagram(w_opened)
    elif userInput == 6:
        w_closed, w_opened = wave_limit_stability(w_closed)
        userInput = input('Введите номер характеристики : \n'
                  '1 - Переходная характеристика' + ';\n'
                  '2 - Корни Х.У.' + ';\n'
                  '3 - Годограф Найквиста ' + ';\n'
                  '4 - Годограф Михайлова' + ';\n'
                  '5 - Диаграмма Боде' + ';\n'
                  '6 - Колебательная граница устойчивости' + '.\n')

        if userInput.isdigit():
            userInput = int(userInput)
            if userInput == 1:
                step_plot = step_response(w_closed)
            elif userInput == 2:
                roots_equation = roots_equation(w_closed)
            elif userInput == 3:
                nyquist_plot = nyquist_plot(w_opened)
            elif userInput == 4:
                michailov_plot = michailov_plot(w_closed)
            elif userInput == 5:
                bode_diagram = bode_diagram(w_opened)

    else:
        print(color.Fore.RED + '\nНедопустимое числовое значение!')
else:
    print(color.Fore.RED + '\nПожалуйста, введите числовое значение!')
