'''
功能：旋转数组
来源：https://leetcode-cn.com/explore/featured/card/top-interview-questions-easy/1/array/23/
重点：切片运算
作者：薛景
最后修改于：2019/07/04
'''

# 使用列表的切片操作，可以轻松完成列表元素的后移操作
# 该方案战胜 99.41 % 的 python3 提交记录
class Solution:
    def rotate(self, nums: list, k: int) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        # 这个题目有个恶心的测试用例，就是k非常大，大过了数列长度，所以我们要想
        # 到如果k等于数列长度，就等价于数列没有发生移动，所以我们对k做一个求余
        # 数的运算。举例：数列长度为2，移动5位，那么其实等价于移动1位的效果
        k = k % len(nums)
        # 另外，如果k为0，即不做任何移动
        if k>0:
            nums[k:] = nums         # 从第k位开始存放原来的数列，即后移操作
            nums[:k] = nums[-k:]    # 把最后几个超出原数列长度的数据复制到数列的开头
            nums[-k:] = []          # 复制完成后，删除超出原长度的数据

# 以下是本地测试代码，提交时只需复制上面的代码块即可
solution = Solution()
nums = [1,2,3,4,5,6,7]
solution.rotate(nums, 3)
print(nums)