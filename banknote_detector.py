import cv2
import numpy as np

img = cv2.imread('testowe15.jpg', 0)
img_color = cv2.imread('testowe15.jpg')

extended = np.zeros((len(img) * 2, len(img[0]) * 2))
extended = np.uint8(extended)
canny = cv2.Canny(img, 80, 80)

for i in range(len(img)):
    for j in range(len(img[0])):
        extended[len(img) // 2 + i][len(img[0]) // 2 + j] = canny[i][j]

kernel = np.ones((2, 2), np.uint8)
extended = cv2.morphologyEx(extended, cv2.MORPH_GRADIENT, kernel)
extended = cv2.dilate(extended, kernel, iterations=15)
extended = cv2.erode(extended, kernel, iterations=25)
extended = cv2.dilate(extended, kernel, iterations=70)
extended = cv2.erode(extended, kernel, iterations=60)
temp = cv2.erode(extended, kernel, iterations=30)

for i in range(len(extended)):
    for j in range(len(extended[0])):
        temp[i][j] = 0
        if extended[i][j] == 255:
            if i - 85 >= 0 and j - 85 >= 0:
                temp[i - 85][j - 85] = 255

extended = cv2.Canny(temp, 10, 10)

exit = False
points = []
while True:
    for i in range(len(img)):
        for j in range(len(img[0])):
            if (extended[i + len(img) // 2][j + len(img[0]) // 2] == 255 and
                    (extended[i + len(img) // 2 + 1][j + len(img[0]) // 2] == 255 or extended[i + len(img) // 2 + 1][
                        j + len(img[0]) // 2 - 1] == 255) and
                    (extended[i + len(img) // 2][j + len(img[0]) // 2 + 1] == 255 or extended[i + len(img) // 2 - 1][
                        j + len(img[0]) // 2 + 1] == 255)):
                current_i = i + len(img) // 2
                current_j = j + len(img[0]) // 2
                min_i = i + len(img) // 2
                min_j = j + len(img[0]) // 2
                max_i = i + len(img) // 2
                max_j = j + len(img[0]) // 2
                exit = True
            if exit:
                break
        if exit:
            break

    if not exit:
        break

    while True:
        exit = False
        extended[current_i][current_j] = 0
        min_i = min(min_i, current_i)
        min_j = min(min_j, current_j)
        max_i = max(max_i, current_i)
        max_j = max(max_j, current_j)
        if extended[current_i + 1][current_j] == 255:
            current_i += 1
        elif extended[current_i - 1][current_j] == 255:
            current_i -= 1
        elif extended[current_i][current_j + 1] == 255:
            current_j += 1
        elif extended[current_i][current_j - 1] == 255:
            current_j -= 1
        elif extended[current_i + 1][current_j + 1] == 255:
            current_i += 1
            current_j += 1
        elif extended[current_i + 1][current_j - 1] == 255:
            current_i += 1
            current_j -= 1
        elif extended[current_i - 1][current_j + 1] == 255:
            current_i -= 1
            current_j += 1
        elif extended[current_i - 1][current_j - 1] == 255:
            current_i -= 1
            current_j -= 1
        else:
            min_i -= len(img) // 2
            min_j -= len(img[0]) // 2
            max_i -= len(img) // 2
            max_j -= len(img[0]) // 2
            if min_i < 0:
                min_i = 0
            if min_j < 0:
                min_j = 0
            if max_i > len(img) - 1:
                max_i = len(img) - 1
            if max_j > len(img[0]) - 1:
                max_j = len(img[0]) - 1
            points.insert(0, min_i)
            points.insert(0, min_j)
            points.insert(0, max_i)
            points.insert(0, max_j)
            break

points.reverse()
cv2.imshow("Banknoty", img_color[points[0]:points[2], points[1]:points[3]])
while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
