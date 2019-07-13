'''
功能：有效的数独
来源：https://leetcode-cn.com/explore/interview/card/top-interview-questions-easy/1/array/30/
重点：使用集合判定是否有重复元素
作者：薛景
最后修改于：2019/07/13
'''

# 该方案战胜 95.94 % 的 python3 提交记录
class Solution:
    def isValidSudoku(self, board: list) -> bool:
        # 判断每行是否有重复
        for i in range(9):
            set1 = set()
            for j in range(9):
                if board[i][j]!='.':
                    if board[i][j] in set1:
                        return False
                    else:
                        set1.add(board[i][j])
        # 判断每列是否有重复
        for i in range(9):
            set2 = set()
            for j in range(9):
                if board[j][i]!='.':
                    if board[j][i] in set2:
                        return False
                    else:
                        set2.add(board[j][i])
        # 定义一个函数，用来验证自x,y坐标开始的那个9宫格内是否有重复       
        def isValid(x,y):
            set3 = set()
            for i in range(x,x+3):
                for j in range(y,y+3):
                    if board[i][j]!='.':
                        if board[i][j] in set3:
                            return False
                        else:
                            set3.add(board[i][j])
            return True
        # 从9个顶点开始验证9个不同的9宫格的数字是否有重复
        start = [(0,0),(0,3),(0,6),(3,0),(3,3),(3,6),(6,0),(6,3),(6,6)]
        for item in start:
            if not isValid(item[0],item[1]):
                return False
        # 如果上述验证过程中，都没有返回False，即没有重复数字，则返回True
        return True

# 以下是本地测试代码，提交时只需复制上面的代码块即可
solution = Solution()
board = [
  ["5","3",".",".","7",".",".",".","."],
  ["6",".",".","1","9","5",".",".","."],
  [".","9","8",".",".",".",".","6","."],
  ["8",".",".",".","6",".",".",".","3"],
  ["4",".",".","8",".","3",".",".","1"],
  ["7",".",".",".","2",".",".",".","6"],
  [".","6",".",".",".",".","2","8","."],
  [".",".",".","4","1","9",".",".","5"],
  [".",".",".",".","8",".",".","7","9"]
]
print(solution.isValidSudoku(board))
board = [
  ["8","3",".",".","7",".",".",".","."],
  ["6",".",".","1","9","5",".",".","."],
  [".","9","8",".",".",".",".","6","."],
  ["8",".",".",".","6",".",".",".","3"],
  ["4",".",".","8",".","3",".",".","1"],
  ["7",".",".",".","2",".",".",".","6"],
  [".","6",".",".",".",".","2","8","."],
  [".",".",".","4","1","9",".",".","5"],
  [".",".",".",".","8",".",".","7","9"]
]
print(solution.isValidSudoku(board))