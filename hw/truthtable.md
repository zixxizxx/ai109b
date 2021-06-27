# 真值表

此程式碼是參考陳鍾誠老師的[truthtable.py](https://gitlab.com/ccc109/ai/-/blob/master/03-search/Q3-queen/truthtable.py)，弄懂後並加上註解

### 程式碼
```
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
```

### 結果
```
PS D:\Desktop\110710540\ai\_homework\final> python .\truthtable.py
[0, 0]
[0, 1]   
[1, 0]   
[1, 1]   
[0, 0, 0]
[0, 0, 1]
[0, 1, 0]
[0, 1, 1]
[1, 0, 0]
[1, 0, 1]
[1, 1, 0]
[1, 1, 1]
```

### 畫圖理解
![image](https://user-images.githubusercontent.com/47874924/123546956-646c9700-d791-11eb-98dd-d8216e7bc840.png)
