import matplotlib.pyplot as plt
import numpy as np

# Создаем массив значений X от 0 до 10 с шагом 0.1
x = np.arange(0, 10, 0.1)

# Вычисляем значения функции sin(x)
y = np.sin(x)

# Создаем график
plt.plot(x, y)

# Настраиваем оси координат и заголовок графика
plt.xlabel('X')
plt.ylabel('Y')
plt.title('График синусоиды')

# Отображаем график
plt.show()