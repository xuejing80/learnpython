'''
功能：存在重复
来源：https://leetcode-cn.com/explore/featured/card/top-interview-questions-easy/1/array/24/
重点：Python中集合中的元素是没有重复的
作者：薛景
最后修改于：2019/07/06
'''

# 利用集合的去重功能，在将列表转换成集合之后，若两者元素个数相同，即可认为原始列
# 表中无重复元素，是不是超方便呢？
# 该方案战胜 99.44 % 的 python3 提交记录
class Solution:
    def containsDuplicate(self, nums: list) -> bool:
        if len(set(nums)) == len(nums):
            return False
        else:
            return True
        
# 以下是本地测试代码，提交时只需复制上面的代码块即可
solution = Solution()
nums = [1,2,3,1]
print(solution.containsDuplicate(nums))