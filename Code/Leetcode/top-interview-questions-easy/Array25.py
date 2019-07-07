'''
功能：只出现一次的数字
来源：https://leetcode-cn.com/explore/interview/card/top-interview-questions-easy/1/array/25/
重点：字典的经典用法：统计数据的出现次数
作者：薛景
最后修改于：2019/07/07
'''

# 方案一，传统方案，使用字典记录每个整数出现的次数，然后找到只出现一次的元素
# 该方案战胜 92.56 % 的 python3 提交记录
class Solution:
    def singleNumber(self, nums: list) -> int:
        d = {}
        for i in nums:
            d[i] = d.get(i, 0) + 1
        for k in d.keys():
            if d[k]==1:
                return k

# 方案二，优化方案，利用集合特性得到原列表中所有不重复的元素，求它们的和，然后乘
# 以2得到所有整数和的2倍，用这个数减去原来列表中的所有元素的和，得到的差就是那个
# 只出现一次的元素
# 该方案战胜 97.07 % 的 python3 提交记录
class Solution:
    def singleNumber(self, nums: list) -> int:
        return sum(set(nums))*2 - sum(nums)

# 以下是本地测试代码，提交时只需复制上面的代码块即可
solution = Solution()
nums = [4,1,2,1,2]
print(solution.singleNumber(nums))