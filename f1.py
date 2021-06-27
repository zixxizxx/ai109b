import sys
import time


#  棋盤物件
class Board:

    def __init__(self, rMax, cMax):
        self.m = [None] * rMax
        self.rMax = rMax
        self.cMax = cMax
        for r in range(rMax):
            self.m[r] = [None] * cMax
            for c in range(cMax):
                self.m[r][c] = '-'

    #  將棋盤格式化成字串
    def __str__(self):
        b = []
        b.append('  0 1 2 3 4 5 6 7 8 9 a b c d e f')
        for r in range(self.rMax):
            b.append('{:x} {:s} {:x}'.format(r, ' '.join(self.m[r]), r))

        b.append('  0 1 2 3 4 5 6 7 8 9 a b c d e f')
        return '\n'.join(b)

    #  顯示棋盤
    def show(self):
        print(str(self))

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

#  以下為遊戲相關資料與函數
#  zero = [ 0, 0, 0, 0, 0]
#  inc  = [-2,-1, 0, 1, 2]
#  dec  = [ 2, 1, 0,-1,-2]
z9 = [0, 0, 0, 0, 0, 0, 0, 0, 0]
i9 = [-4, -3, -2, -1, 0, 1, 2, 3, 4]
d9 = [4, 3, 2, 1, 0, -1, -2, -3, -4]
z5 = [0, 0, 0, 0, 0]
i2 = i9[2:-2]
d2 = d9[2:-2]

#  檢查在 (r, c) 這一格，規則樣式 (dr, dc) 是否被滿足
#  dr, dc 的組合可用來代表「垂直 | , 水準 - , 下斜 \ , 上斜 /」。
def patternCheck(board, turn, r, c, dr, dc):
    for i in range(len(dr)):
        tr = round(r + dr[i])
        tc = round(c + dc[i])
        if tr < 0 or tr >= board.rMax or tc < 0 or tc >= board.cMax:
            return False
        v = board.m[tr][tc]
        if (v != turn):
            return False
    
    return True

#  檢查是否下 turn 這個子的人贏了。
def winCheck(board, turn):
    win = False
    tie = True
    for r in range(board.rMax):
        for c in range(board.cMax):
            tie = False if board.m[r][c] == '-' else tie
            win = True if patternCheck(board, turn, r, c, z5, i2) else win #  水準 -
            win = True if patternCheck(board, turn, r, c, i2, z5) else win #  垂直 |
            win = True if patternCheck(board, turn, r, c, i2, i2) else win #  下斜 \
            win = True if patternCheck(board, turn, r, c, i2, d2) else win #  上斜 /
    if (win):
        print('{} 贏了！'.format(turn))  #  如果贏了就印出贏了
        sys.exit() #  然後離開。

    if (tie):
        print('平手')
        sys.exit(0) #  然後離開。

    return win

def peopleTurn(board, turn):
    global list3
    try:
        xy = input('將 {} 下在: '.format(turn))
        r = int(xy[0], 16) #  取得下子的列 r (row)
        c = int(xy[1], 16) #  取得下子的行 c (column)
        if r < 0 or r > board.rMax or c < 0 or c > board.cMax: #  檢查是否超出範圍
            raise Exception('(row, col) 超出範圍!') #  若超出範圍就丟出例外，下一輪重新輸入。
        if board.m[r][c] != '-': #  檢查該位置是否已被佔據
            raise Exception('({}{}) 已經被佔領了!'.format(xy[0], xy[1])) #  若被佔據就丟出例外，下一輪重新輸入。
        board.m[r][c] = turn #  否則、將子下在使用者輸入的 (r,c) 位置
        list2.append((r, c))
        list3.append((r, c))
    except Exception as error:
        print(error)
        peopleTurn(board, turn)

def computerTurn(board, turn):
    step = ai()
    board.m[step[0]][step[1]] = turn
    list3.append(step)
    list1.append(step)

        


def chess(o, x):
    b = Board(16, 16) #  建立棋盤
    b.show()            #  顯示棋盤
    while (True):
        if o.upper()=='P':
            peopleTurn(b, 'o')
        else:
            computerTurn(b, 'o')
        b.show()         #  顯示棋盤現況
        winCheck(b, 'o') #  檢查下了這子之後是否贏了！
        time.sleep(2)
        if x.upper()=='P':
            peopleTurn(b, 'x')
        else:
            computerTurn(b, 'x')
        b.show()
        winCheck(b, 'x')
        time.sleep(2)



print("c=computer, p=person")
player1= input("enter: c or p, player1: ")
player2= input("enter: c or p, player2: ")
o, x = player1, player2
print(f"player1 : {player1}, player2 : {player2}")

chess(o, x)
