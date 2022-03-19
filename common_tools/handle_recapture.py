import time
import cv2
from selenium.webdriver import ActionChains

def get_validate_param(backgroundImg, validateImg):
    """
    :param backgroundImg:背景图片本地路径
    :param validateImg:滑动图片本地路径
    :return: tracks:移动轨迹
    """
    bg_img = cv2.imread(backgroundImg)
    tp_img = cv2.imread(validateImg)
    bg_canny = cv2.Canny(bg_img, 600, 600)
    tp_canny = cv2.Canny(tp_img, 600, 600)
    cv2.imwrite('bg_img_canny.png', bg_canny)
    # 匹配缺口
    bg_gray = cv2.cvtColor(bg_canny, cv2.COLOR_GRAY2RGB)
    tp_gray = cv2.cvtColor(tp_canny, cv2.COLOR_GRAY2RGB)
    res = cv2.matchTemplate(bg_gray, tp_gray, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    th, tw = tp_img.shape[:2]
    tl = max_loc  # 左上角点的坐标
    br = (tl[0] + tw, tl[1] + th)  # 右下角点的坐标
    cv2.rectangle(bg_img, tl, br, (0, 0, 255), 2)  # 绘制矩形
    cv2.imwrite('find_location.png', bg_img)  # 保存在本地
    # print(max_loc[0])
    # x = (max_loc[0] // 1.623529)
    x = max_loc[0] - 5
    # tracks = get_tracks(x)
    return x
    # return tracks

def get_tracks(distance):
    '''
    :param distance:缺口图片左上角坐标(x,y)
    :return:
    '''
    print(distance)
    tracks = []     # 移动轨迹
    current = 0     # 当前位移
    mid = int(distance * 4 / 6)      # 减速阈值
    t = 1        # 计算间隔
    v = 10        # 初速度
    while current < distance:
        if current < mid:
            a = 10       # 加速度为正2
        else:
            a = -3      # 加速度为负3
        v0 = v      # 初速度v0
        v = v0 + a * t      # 当前速度
        move = v0 * t + 1 / 2 * a * t * t       # 移动距离
        current += move     # 当前位移
        if current > distance:
            move = distance - (current - move)
        tracks.append(round(move))      # 加入轨迹
    return tracks

def move_to_gap(driver, slider, tracks):
    '''
    :param driver:chromedriver对象
    :param slider:滑块对象
    :param tracks:鼠标移动轨迹(列表对象:每个元素为移动距离)
    :return:
    '''
    action = ActionChains(driver)
    action.click_and_hold(slider).perform()
    for i in tracks:
        # action会自动累加位移，除非reset这个action
        action.move_by_offset(xoffset=i, yoffset=0).perform()
        action = ActionChains(driver)
    # action.move_by_offset(xoffset=tracks, yoffset=0).perform()
    action = ActionChains(driver)
    time.sleep(0.5)
    action.release().perform()


def generate_tracks(S):
    """
    :param S: 缺口距离Px
    :return:
    """
    S += 20
    v = 0
    t = 0.2
    forward_tracks = []
    current = 0
    mid = S * 3 / 5  # 减速阀值
    while current < S:
        if current < mid:
            a = 2  # 加速度为+2
        else:
            a = -3  # 加速度-3
        s = v * t + 0.5 * a * (t ** 2)
        v = v + a * t
        current += s
        forward_tracks.append(round(s))

    back_tracks = [-3, -3, -2, -2, -2, -2, -2, -1, -1, -1]
    # return {'forward_tracks': forward_tracks, 'back_tracks': back_tracks}
    return forward_tracks


if __name__ == '__main__':
    backpic = r''
    valipic = r''
    tracks = get_validate_param(backpic, valipic)
    move_to_gap()