# 人工智慧期末專案 五子棋
- 本程式修改自[陳鍾誠老師](https://gitlab.com/ccc109/ai/-/blob/master/11-chess/01-gomoku/gomoku.py)github專案

### 授權聲明
- 本專案中的程式採用[LICENSE](https://github.com/zixxizxx/ai109b/pull/1/commits/6979f658a74c6042dfe458f82019a2714cf3c2c8)
- 部分圖片及內容採用維基百科:[CC BY-SA 3.0協議文本](https://zh.wikipedia.org/wiki/Wikipedia:CC_BY-SA_3.0%E5%8D%8F%E8%AE%AE%E6%96%87%E6%9C%AC)

### 極小化極大演算法
- 是一種找出失敗的最大可能性中的最小值的演算法
- 演算法是一個零總和演算法，即一方要在可選的選項中選擇將其優勢最大化的選擇，另一方則選擇令對手優勢最小化的方法


### Alpha-beta剪枝演算法
- 用以減少極小化極大演算法（Minimax演算法）搜尋樹的節點數
- 優點是減少搜尋樹的分枝，將搜尋時間用在「更有希望」的子樹上，繼而提升搜尋深度


#### 程式
主要在老師的基礎上改變
```
#分數評估
shape_score = [(50, (0, 1, 1, 0, 0)),
                   (50, (0, 0, 1, 1, 0)),
                   (200, (1, 1, 0, 1, 0)),
                   (500, (0, 0, 1, 1, 1)),
                   (500, (1, 1, 1, 0, 0)),
                   (5000, (0, 1, 1, 1, 0)),
                   (5000, (0, 1, 0, 1, 1, 0)),
                   (5000, (0, 1, 1, 0, 1, 0)),
                   (5000, (1, 1, 1, 0, 1)),
                   (5000, (1, 1, 0, 1, 1)),
                   (5000, (1, 0, 1, 1, 1)),
                   (5000, (1, 1, 1, 1, 0)),
                   (5000, (0, 1, 1, 1, 1)),
                   (50000, (0, 1, 1, 1, 1, 0)),
                   (99999999, (1, 1, 1, 1, 1))]

list1 = []  # AI
list2 = []  # human
list3 = []  # all
list_all = []  # 整個棋盤的點
next_point = [0, 0]  # AI下一步最應該下的位置


DEPTH=3

for i in range(16):
    for j in range(16):
        list_all.append((i, j))


    

def ai():
    """
    AI計算落子位置
    """

    fs = (8, 8) #電腦的第一步下在8-8

    if not list3: 
        list3.append(fs)
        list1.append(fs)
        return fs[0],fs[1]

    else:
        maxmin(True, DEPTH, -99999999, 99999999)
        return next_point[0], next_point[1]

def maxmin(is_ai, depth, alpha, beta):
    """
    負值極大演算法搜索 alpha + beta剪枝
    """
    # 遊戲是否結束 | | 探索的遞迴深度是否到邊界
    if depth == 0:
        return evaluation(is_ai)
 
    blank_list = list(set(list_all).difference(set(list3)))
    order(blank_list)  # 搜索順序排序  提高剪枝效率
    # 遍歷每一個候選步
    for next_step in blank_list:

 
        # 如果要評估的位置沒有相鄰的子， 則不去評估  減少計算
        if not has_neightnor(next_step):
            continue

        if is_ai:
            list1.append(next_step)
        else:
            list2.append(next_step)
        list3.append(next_step)
 
        value = -maxmin(not is_ai, depth - 1, -beta, -alpha)
        if is_ai:
            list1.remove(next_step)
        else:
            list2.remove(next_step)
        list3.remove(next_step)
 
        if value > alpha:
            if depth == DEPTH:
                next_point[0] = next_step[0]
                next_point[1] = next_step[1]
            # alpha + beta剪枝點
            if value >= beta:
                return beta
            alpha = value
    return alpha

def order(blank_list):
    """
    離最後落子的鄰居位置最有可能是最優點
    計算最後落子點的8個方向鄰居節點
    若未落子，則插入到blank列表的最前端
    :param blank_list: 未落子節點集合
    :return: blank_list
    """
    last_pt = list3[-1]
    for item in blank_list:
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if (last_pt[0] + i, last_pt[1] + j) in blank_list:
                    blank_list.remove((last_pt[0] + i, last_pt[1] + j))
                    blank_list.insert(0, (last_pt[0] + i, last_pt[1] + j))
 
 
def has_neightnor(pt):
    """
    判斷是否有鄰居節點
    :param pt: 待評測節點
    :return:
    """
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            if (pt[0] + i, pt[1] + j) in list3:
                return True
    return False

def evaluation(is_ai):
    """
    評估函數
    """
    total_score = 0
    if is_ai:
        my_list = list1
        enemy_list = list2
    else:
        my_list = list2
        enemy_list = list1
    # 算自己的得分
    score_all_arr = []  # 得分形狀的位置 用於計算如果有相交 得分翻倍
    my_score = 0
    for pt in my_list:
        m = pt[0]
        n = pt[1]
        my_score += cal_score(m, n, 0, 1, enemy_list, my_list, score_all_arr)
        my_score += cal_score(m, n, 1, 0, enemy_list, my_list, score_all_arr)
        my_score += cal_score(m, n, 1, 1, enemy_list, my_list, score_all_arr)
        my_score += cal_score(m, n, -1, 1, enemy_list, my_list, score_all_arr)
    #  算敵人的得分， 並減去
    score_all_arr_enemy = []
    enemy_score = 0
    for pt in enemy_list:
        m = pt[0]
        n = pt[1]
        enemy_score += cal_score(m, n, 0, 1, my_list, enemy_list, score_all_arr_enemy)
        enemy_score += cal_score(m, n, 1, 0, my_list, enemy_list, score_all_arr_enemy)
        enemy_score += cal_score(m, n, 1, 1, my_list, enemy_list, score_all_arr_enemy)
        enemy_score += cal_score(m, n, -1, 1, my_list, enemy_list, score_all_arr_enemy)
 
    total_score = my_score - enemy_score * 0.1
    return total_score

def cal_score(m, n, x_decrict, y_derice, enemy_list, my_list, score_all_arr):
    """
    每個方向上的分值計算
    :param m:
    :param n:
    :param x_decrict:
    :param y_derice:
    :param enemy_list:
    :param my_list:
    :param score_all_arr:
    :return:
    """
    add_score = 0  # 加分項
    # 在一個方向上， 只取最大的得分項
    max_score_shape = (0, None)
 
    # 如果此方向上，該點已經有得分形狀，不重複計算
    for item in score_all_arr:
        for pt in item[1]:
            if m == pt[0] and n == pt[1] and x_decrict == item[2][0] and y_derice == item[2][1]:
                return 0
 
    # 在落子點 左右方向上迴圈查找得分形狀
    for offset in range(-5, 1):
        pos = []
        for i in range(0, 6):
            if (m + (i + offset) * x_decrict, n + (i + offset) * y_derice) in enemy_list:
                pos.append(2)
            elif (m + (i + offset) * x_decrict, n + (i + offset) * y_derice) in my_list:
                pos.append(1)
            else:
                pos.append(0)
        tmp_shap5 = (pos[0], pos[1], pos[2], pos[3], pos[4])
        tmp_shap6 = (pos[0], pos[1], pos[2], pos[3], pos[4], pos[5])
 
        for (score, shape) in shape_score:
            if tmp_shap5 == shape or tmp_shap6 == shape:
                if score > max_score_shape[0]:
                    max_score_shape = (score, ((m + (0 + offset) * x_decrict, n + (0 + offset) * y_derice),
                                               (m + (1 + offset) * x_decrict, n + (1 + offset) * y_derice),
                                               (m + (2 + offset) * x_decrict, n + (2 + offset) * y_derice),
                                               (m + (3 + offset) * x_decrict, n + (3 + offset) * y_derice),
                                               (m + (4 + offset) * x_decrict, n + (4 + offset) * y_derice)),
                                       (x_decrict, y_derice))
 
    # 計算兩個形狀相交， 如兩個3活 相交， 得分增加 一個子的除外
    if max_score_shape[1] is not None:
        for item in score_all_arr:
            for pt1 in item[1]:
                for pt2 in max_score_shape[1]:
                    if pt1 == pt2 and max_score_shape[0] > 10 and item[0] > 10:
                        add_score += item[0] + max_score_shape[0]
 
        score_all_arr.append(max_score_shape)
 
    return add_score + max_score_shape[0]
```

#### 結果
```
PS D:\Desktop\110710540\ai\_homework\final> python f1.py
c=computer, p=person
enter: c or p, player1: p
enter: c or p, player2: c
player1 : p, player2 : c
  0 1 2 3 4 5 6 7 8 9 a b c d e f
0 - - - - - - - - - - - - - - - - 0
1 - - - - - - - - - - - - - - - - 1
2 - - - - - - - - - - - - - - - - 2
3 - - - - - - - - - - - - - - - - 3
4 - - - - - - - - - - - - - - - - 4
5 - - - - - - - - - - - - - - - - 5
6 - - - - - - - - - - - - - - - - 6
7 - - - - - - - - - - - - - - - - 7
8 - - - - - - - - - - - - - - - - 8
9 - - - - - - - - - - - - - - - - 9
a - - - - - - - - - - - - - - - - a
b - - - - - - - - - - - - - - - - b
c - - - - - - - - - - - - - - - - c
d - - - - - - - - - - - - - - - - d
e - - - - - - - - - - - - - - - - e
f - - - - - - - - - - - - - - - - f
  0 1 2 3 4 5 6 7 8 9 a b c d e f
將 o 下在: 99
  0 1 2 3 4 5 6 7 8 9 a b c d e f
0 - - - - - - - - - - - - - - - - 0
1 - - - - - - - - - - - - - - - - 1
2 - - - - - - - - - - - - - - - - 2
3 - - - - - - - - - - - - - - - - 3
4 - - - - - - - - - - - - - - - - 4
5 - - - - - - - - - - - - - - - - 5
6 - - - - - - - - - - - - - - - - 6
7 - - - - - - - - - - - - - - - - 7
8 - - - - - - - - - - - - - - - - 8
9 - - - - - - - - - o - - - - - - 9
a - - - - - - - - - - - - - - - - a
b - - - - - - - - - - - - - - - - b
c - - - - - - - - - - - - - - - - c
d - - - - - - - - - - - - - - - - d
e - - - - - - - - - - - - - - - - e
f - - - - - - - - - - - - - - - - f
  0 1 2 3 4 5 6 7 8 9 a b c d e f
  0 1 2 3 4 5 6 7 8 9 a b c d e f
0 - - - - - - - - - - - - - - - - 0
1 - - - - - - - - - - - - - - - - 1
2 - - - - - - - - - - - - - - - - 2
3 - - - - - - - - - - - - - - - - 3
4 - - - - - - - - - - - - - - - - 4
5 - - - - - - - - - - - - - - - - 5
6 - - - - - - - - - - - - - - - - 6
7 - - - - - - - - - - - - - - - - 7
8 - - - - - - - - - - - - - - - - 8
9 - - - - - - - - - o - - - - - - 9
a - - - - - - - - - - x - - - - - a
b - - - - - - - - - - - - - - - - b
c - - - - - - - - - - - - - - - - c
d - - - - - - - - - - - - - - - - d
e - - - - - - - - - - - - - - - - e
f - - - - - - - - - - - - - - - - f
  0 1 2 3 4 5 6 7 8 9 a b c d e f
將 o 下在: 88
```

### 參考資料
- [Code](https://gitlab.com/ccc109/ai/-/blob/master/11-chess/01-gomoku/gomoku.py)
- [Minimax演算法](https://zh.wikipedia.org/wiki/%E6%9E%81%E5%B0%8F%E5%8C%96%E6%9E%81%E5%A4%A7%E7%AE%97%E6%B3%95)
- [Alpha-beta剪枝](https://zh.wikipedia.org/wiki/Alpha-beta%E5%89%AA%E6%9E%9D)
- [MiniMax算法优化:Alpha-Beta剪枝算法](https://miketech.it/alpha-beta-pruning)
- [colingogogo](https://github.com/colingogogo/gobang_AI/blob/master/gobang_AI.py)
- [自制五子棋](https://ewind.us/2015/js-gomoku-2/)

