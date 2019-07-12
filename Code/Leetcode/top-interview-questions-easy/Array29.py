'''
功能：两数之和
来源：https://leetcode-cn.com/explore/interview/card/top-interview-questions-easy/1/array/29/
重点：异常处理的使用方法
作者：薛景
最后修改于：2019/07/12
'''

# 方案一，Python思维，完全按照题意进行编码，但是效率很差。方案中使用了try和exc-
# ept构成的异常处理机制，之所以要使用异常处理包含程序代码，是因为index函数在找不
# 到指定元素的时候会产生报错信息并中断程序的执行，而异常处理机制能够让程序在遇到
# 错误的时候去执行指定的代码，此处我们使用了pass语句，表示啥都不做
# 该方案战胜 40.48 % 的 python3 提交记录
class Solution:
    def twoSum(self, nums: list, target: int) -> list:
        for i in range(len(nums)):
            # index的功能是从指定的位置之后找到另一个数，并返回其下标，如果找不
            # 到该数，则会返回报错信息，并停止程序的运行
            try:
                return [i,nums.index(target-nums[i],i+1)]
            except:
                pass

# 方案二，优化方案，上例中index函数的工作机制应该是通过遍历操作返回查找结果，效
# 率比较差。为了提高本题的执行效率，必须想办法取代遍历查找的过程，因此，我们建立
# 一个字典用以存放所有查看过的数字及其下标信息，然后只需在遍历过程中在字典中找另
# 一个数即可，因为使用键值定位字典元素的工作原理与index遍历的工作原理并不相同，
# 所以可以有效提高查找速度，从而提升代码的执行效率
# 该方案战胜 93.54 % 的 python3 提交记录
class Solution:
    def twoSum(self, nums: list, target: int) -> list:
        dic = {}
        for i in range(len(nums)):
            j = target - nums[i]
            if dic.get(j,None)!=None:
                return [dic[j],i]
            else:
                dic[nums[i]]=i

# 以下是本地测试代码，提交时只需复制上面的代码块即可
solution = Solution()
nums = [2, 7, 11, 15]
target = 9
print(solution.twoSum(nums, target))