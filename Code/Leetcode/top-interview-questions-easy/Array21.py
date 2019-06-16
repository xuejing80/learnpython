'''
功能：从排序数组中删除重复项
来源：https://leetcode-cn.com/explore/featured/card/top-interview-questions-easy/1/array/21/
重点：我把存放位置信息的变量叫做指针变量
作者：薛景
最后修改于：2019/06/16
'''

# 方案一：传统算法，设置一个指针变量指向不重复的最后一个元素，在遍历过程中，忽略
# 相同元素，当遇到新的数值时，指针向后移动一个位置，然后用新的数值替换原来的数值
# 该方案战胜 82.40 % 的 python3 提交记录
class Solution:
    def removeDuplicates(self, nums: list) -> int:
        p = 0
        for i in range(1, len(nums)):
            if nums[p] != nums[i]:
                p = p + 1
                nums[p] = nums[i]
        nums[p+1:] = []
        return len(nums)

# 方案二：Python思维，因为集合数据类型不允许有重复的元素，所以将列表转换成集合便
# 可以去掉列表中的重复元素，然后对其排序便可以得到新的不重复的有序列表
# 该方案战胜 98.40 % 的 python3 提交记录
class Solution:
    def removeDuplicates(self, nums: list) -> int:
        result = sorted(set(nums))
        nums[:] = result[:]     # 不能直接赋值，必须用切片运算操作原列表
        return len(nums)

# 以下是本地测试代码，提交时只需复制上面的代码块即可
solution = Solution()
nums = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]
solution.removeDuplicates(nums)
print(nums)