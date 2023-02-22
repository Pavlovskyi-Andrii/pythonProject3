
from PIL import Image, ImageDraw
import numpy as np

# Загружаем изображение и преобразуем его в массив NumPy
img = Image.open("111.png")
img_data = np.array(img)

# Получаем размер изображения и вычисляем его центр
width, height = img.size
center_x, center_y = int(width/2), int(height/2)

# Определяем координаты каждого гвоздика на круглом фоне
radius = min(center_x, center_y) - 10
num_points = 100 # Количество гвоздиков
points = []
for i in range(num_points):
    angle = i * (2*np.pi/num_points)
    x = int(center_x + radius * np.cos(angle))
    y = int(center_y + radius * np.sin(angle))
    points.append((x,y))

# Создаем список координат для нити на круглом фоне
thread_coords = points.copy()

# Создаем изображение и объект ImageDraw
result_img = Image.new('RGB', img.size, color='white')
draw = ImageDraw.Draw(result_img)

# Рисуем гвоздики и добавляем их координаты в список thread_coords
for point in points:
    draw.ellipse((point[0]-2, point[1]-2, point[0]+2, point[1]+2), fill='black')
    thread_coords.append(point)

# Рисуем нить
draw.line(thread_coords, fill='black', width=1)

# Выводим изображение
result_img.show()
