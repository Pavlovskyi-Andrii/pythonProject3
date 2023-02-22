from PIL import Image
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

# Создаем список цветов каждого гвоздика на круглом фоне
colors = []
for point in points:
    x,y = point
    color = img_data[y,x]
    colors.append(color)

# Определяем количество проходов нити в зависимости от цвета на каждой точке
num_passes = []
for color in colors:
    if np.all(color == [0,0,0]): # черный цвет
        num_passes.append(10)
    elif np.all(color == [128,128,128]): # серый цвет
        num_passes.append(5)
    else: # белый цвет
        num_passes.append(1)

# Создаем список координат для нити на круглом фоне
thread_coords = []
current_point = points[0]
moves = []
for i in range(len(points)):
    start_point = current_point
    end_point = points[(i+1) % num_points]
    passes = num_passes[i]
    move = f"{i + 1}. {points.index(tuple([int(coord) for coord in start_point]))}-{points.index(tuple([int(coord) for coord in end_point]))}"

    moves.append(move)
    for j in range(passes):
        # Рассчитываем координаты точек на нити между двумя гвоздиками
        x_coords = np.linspace(start_point[0], end_point[0], num=passes + 1)
        y_coords = np.linspace(start_point[1], end_point[1], num=passes + 1)
        points_on_thread = list(zip(x_coords, y_coords))
        thread_coords.extend(points_on_thread)
        current_point = points_on_thread



# Выводим информацию о ходах нити
print("Нить начинается на точке {}".format(points[0]))
for i in range(len(points)):
    start_point = points[i]
    end_point = points[(i+1) % num_points]
    passes = num_passes[i]
    for j in range(passes):
        start_index = i * (max(num_passes)+1) + j
        end_index = start_index + 1
        print("Виток {} от точки {} до точки {}".format(j+1, start_point, end_point))
        print("Координаты: от {} до {}".format(thread_coords[start_index], thread_coords[end_index]))

result_img = img.copy()
draw = ImageDraw.Draw(result_img)
draw.line(thread_coords, fill='black', width=1)

result_img.show(block=True)
