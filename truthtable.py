def truthTable(n): # 列出 n 個變數的所有可能
    p = [] # 剛開始是空的，存入0或1
    return tableNext(n, p) # 呼叫函數排出所有可能

def tableNext(n, p): 
    i = len(p) # 已填入的長度
    if i == n: # 如果全都排好
        print(p) #印出排列
        return 
    for x in [0, 1]: # x選擇0或1
        p.append(x) # 將 x 放入 p[] 裡
        tableNext(n, p) # 繼續遞迴執行 tableNext
        p.pop() # 把 x 移出表

truthTable(2) # 印出 2 個變數的真值表
truthTable(3) # 印出 3 個變數的真值表