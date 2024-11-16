
import os, easyocr


def pic_recognition(pic, save_path = "") -> list:
    """
    识别png和jpg
    """
    # 识别
    reader = easyocr.Reader(['en', 'ch_sim'], gpu=False)
    result = reader.readtext(pic)

    # 保存
    if save_path:
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        with open(save_path + os.path.basename(pic) + '_text.txt', 'w', encoding='utf-8') as file:
            for area in result:
                file.write(str(area[1]) + '\n')
                # file.write(str(area[1]))

    return result


def sort_result(result):
    """
    筛选掉结果中的标题和图例
    """
    new_result = result.copy()

    for area in result:

        # 排除标题
        if area[0][0][1] <= 18:
            new_result.remove(area)

        # 排除右上角图例
        elif area[0][3][0] >= 640 and area[0][3][1] <= 60:
            new_result.remove(area)

    return new_result


def pair_result(result):
    pairs = {}
    paired = []

    for i in range(len(result)):

        # 已配对
        if i in paired:
            continue

        # 找配对
        for j in range(len(result)):

            # 已配对
            if j in paired:
                continue

            # 自身
            if i == j:
                continue

            # 配对
            elif result[j][0][0][0]-20 <= result[i][0][0][0] <= result[j][0][0][0]+20:
                pairs[result[j][1]] = result[i][1]
                paired.append(i)
                paired.append(j)

    return pairs

