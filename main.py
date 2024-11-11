from PIL import ImageGrab
import numpy as np
import time
import pyautogui
import cv2

button_positions = {  # 每个输入数的坐标
    0: (333, 734),
    1: (273, 819),
    2: (384, 816),
    3: (483, 818),
    4: (591, 826),
    5: (703, 821),
    6: (339, 898),
    7: (445, 898),
    8: (545, 898),
    9: (656, 898),
}

def capture_and_process_region(bbox):
    # 截取屏幕区域
    screenshot = ImageGrab.grab(bbox=bbox)

    # 将图像转换为灰度
    gray_image = screenshot.convert("L")

    # 二值化处理
    threshold = 128
    binary_image = gray_image.point(lambda p: 1 if p > threshold else 0)
    return binary_image

def count_zero_union(matrix_a, matrix_b):
    zeros_a = {(i, j) for i in range(matrix_a.shape[0]) for j in range(matrix_a.shape[1]) if matrix_a[i, j] == 0}
    zeros_b = {(i, j) for i in range(matrix_b.shape[0]) for j in range(matrix_b.shape[1]) if matrix_b[i, j] == 0}
    zero_union = zeros_a.union(zeros_b)
    return len(zero_union)

def resize_to_5x5(binary_image): # 将二值图像调整为5x5的大小
    resized_image = binary_image.resize((5, 5), 0)
    return np.array(resized_image)

def capture_region(bbox):
    return ImageGrab.grab(bbox=bbox)

def image_found(template_path):
    bbox = (400, 558, 577, 613)
    screenshot = capture_region(bbox)
    screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    template = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)
    result = cv2.matchTemplate(screenshot_cv, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(result >= threshold)
    return len(loc[0]) > 0

def fill_input_in_app(zero_count):
    time.sleep(2)
    for digit in str(zero_count):
        digit = int(digit)
        if digit in button_positions:
            x, y = button_positions[digit]
            pyautogui.click(x, y)

# 初始化计数器
counter = 0

def main():
    global counter  # 使用全局计数器变量

    bbox_up = (328, 203, 494, 373)
    bbox_down = (319, 416, 490, 584)

    binary_image_up = capture_and_process_region(bbox_up)
    binary_image_down = capture_and_process_region(bbox_down)

    resized_matrix_up = resize_to_5x5(binary_image_up)
    resized_matrix_down = resize_to_5x5(binary_image_down)

    matrix_up = resized_matrix_up.astype(int)
    matrix_down = resized_matrix_down.astype(int)

    #print("调整后的5x5矩阵:")
    print("Matrix Up:")
    for row in matrix_up:
        print(row)
    print("Matrix Down:")
    for row in matrix_down:
        print(row)

    counter += 1  # 递增计数器
    print(f"当前是第 {counter} 次")

    zero_count = count_zero_union(matrix_up, matrix_down)
    print(f"并集中0元素的数量: {zero_count}\n")

    fill_input_in_app(zero_count)

if __name__ == "__main__":
    while True:
        if image_found('C:/Users/Liu/Desktop/pythonProject/judge.png'): # 更改这里的路径
            time.sleep(4)
            main()
