'''
功能：移动零
来源：https://leetcode-cn.com/explore/interview/card/top-interview-questions-easy/1/array/28/
重点：指针变量的使用方法
作者：薛景
最后修改于：2019/07/10
'''

# 我们使用指针变量index存放数列中第一个“0”的位置（最开始，先假设位置0上的元素是
# “0”），在整个列表遍历的过程中，只要发现某个元素不为0，就将该位置的元素和index
# 位置上的元素对调，并更新index中的值，上述过程反复执行就可以将所有的“0”后移
# 该方案战胜 93.89 % 的 python3 提交记录
class Solution:
    def moveZeroes(self, nums: list) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        index = 0
        for i in range(len(nums)):
            if nums[i]!=0:
                # 下方这个if语句的目的是减少数列前端非零项产生的对调次数
                if i>index:
                    nums[index],nums[i] = nums[i],nums[index]
                index += 1

# 以下是本地测试代码，提交时只需复制上面的代码块即可
solution = Solution()
nums = [0,1,0,3,12]
solution.moveZeroes(nums)
print(nums)