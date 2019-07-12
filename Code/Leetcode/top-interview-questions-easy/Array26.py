'''
功能：两个数组的交集 II
来源：https://leetcode-cn.com/explore/interview/card/top-interview-questions-easy/1/array/26/
重点：学会找到影响程序执行效率的语句
作者：薛景
最后修改于：2019/07/12
'''

# 方案一，传统方案，先通过比较两个列表中的元素数，把元素少的放在nums1里面，这样
# 做的目的是尽量减少运算次数，然后对nums1里面的元素进行逐个遍历，如果该元素也在
# nums2里面的话，就把它从nums2中移除，并添加到结果列表result中
# 该方案战胜 57.55 % 的 python3 提交记录
class Solution:
    def intersect(self, nums1: list, nums2: list) -> list:
        if len(nums1)>len(nums2):
            nums1,nums2 = nums2,nums1
        result = []
        for item in nums1:
            if item in nums2:
                nums2.remove(item)
                result.append(item)
        return result

# 这里我们做个实验，看一下remove操作和append操作哪一个是费时的原因
import time
result = []
time1 = time.process_time()
for i in range(100000):
    result.append(i)
time2 = time.process_time()
for i in range(100000):
    result.remove(i)
time3 = time.process_time()
print("100000次append共消耗{:.0f}毫秒".format((time2-time1)*1000))
print("100000次remove共消耗{:.0f}毫秒".format((time3-time2)*1000))

# 方案二，优化方案，从上面的实验，我们已经可以看出remove操作是费时的主要原因，所
# 以我们可以对列表nums2中的所有元素进行计数，然后遍历nums1中的元素，通过对元素的
# 出现次数进行操作，达到与方案一同样的功能，同时避免使用remove操作
# 该方案战胜 99.76 % 的 python3 提交记录
class Solution:
    def intersect(self, nums1: list, nums2: list) -> list:
        # 第一步，保证nums1中存放的是较少元素的列表
        if len(nums1)>len(nums2):
            nums1,nums2 = nums2,nums1
        # 第二步，统计nums2中所有元素出现的次数
        counter = {}
        for i in nums2:
            counter[i] = counter.get(i,0) + 1
        # 第三步，遍历nums1中的元素，如果其在nums2中出现次数大于0，则计入结果列
        # 表，并且将它的出现次数减1
        result = []
        for i in nums1:
            if counter.get(i,0)>0:
                result.append(i)
                counter[i] -= 1
        return result

# 以下是本地测试代码，提交时只需复制上面的代码块即可
solution = Solution()
nums1 = [1,2,2,1]
nums2 = [2,2]
print(solution.intersect(nums1, nums2))