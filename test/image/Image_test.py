# encoding: utf-8
"""
@project = Py_learing
@file = Image_test
@author= wanghu
@create_time = 2021/8/6 14:51
"""
import cv2,time

bg_image = cv2.imread(r'./bgimg.png')
tp_image = cv2.imread(r'./huak.png')

# gray_bgimg = cv2.cvtColor(bg_image, cv2.COLOR_BGR2GRAY)
# gray_tpimg = cv2.cvtColor(tp_image, cv2.COLOR_BGR2GRAY)
bg_canny = cv2.Canny(bg_image, 100, 200)
tp_canny = cv2.Canny(tp_image, 100, 200)
res = cv2.matchTemplate(bg_canny, tp_canny, cv2.TM_CCOEFF_NORMED)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
th,tw = tp_image.shape[:2]
tl = max_loc
br = (tl[0]+tw, tl[1]+th) # 右下角点的坐标
cv2.rectangle(bg_image, tl, br, (0, 0, 255), 2)
cv2.imshow('out.jpg', bg_image)

cv2.waitKey(3)
time.sleep(7)

