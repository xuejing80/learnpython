'''
功能：旋转图像
来源：https://leetcode-cn.com/explore/interview/card/top-interview-questions-easy/1/array/31/
重点：使用元组作为字典的键存放数据
作者：薛景
最后修改于：2019/07/14
'''

# 这个题目的难度，不在编程，而在数学建模的环节，也就是说，我们为了找到旋转列表元
# 素的规律，必须在白纸上把原来的坐标和新坐标写下来，并找出其中的对应关系
# 该方案战胜 98.97 % 的 python3 提交记录
class Solution:
    def rotate(self, matrix: list) -> None:
        """
        Do not return anything, modify matrix in-place instead.
        """
        n = len(matrix[0])
        newPosition = {}
        for i in range(n):
            for j in range(n):
                # 把新坐标作为字典的键，存储原来二维列表中的元素
                newPosition[(j,n-i-1)] = matrix[i][j]
        # 遍历字典，按照新坐标，将数据挨个放回去
        for pos,value in newPosition.items():
            matrix[pos[0]][pos[1]] = value

# 以下是本地测试代码，提交时只需复制上面的代码块即可
solution = Solution()
matrix = [
  [1,2,3],
  [4,5,6],
  [7,8,9]
]
solution.rotate(matrix)
print(matrix)
matrix = [
  [ 5, 1, 9,11],
  [ 2, 4, 8,10],
  [13, 3, 6, 7],
  [15,14,12,16]
]
solution.rotate(matrix)
print(matrix)