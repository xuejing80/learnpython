'''
功能：加一
来源：https://leetcode-cn.com/explore/interview/card/top-interview-questions-easy/1/array/27/
重点：使用range函数构建倒序循环、循环结构中else分支的使用方法
作者：薛景
最后修改于：2019/07/09
'''

# 方案一，传统方案，把数列中的每一个元素取出来构成一个整数，再将这个整数+1，然后
# 利用求余数的操作将结果从后向前逐位取出，添加到列表中
# 该方案战胜 51.51 % 的 python3 提交记录
class Solution:
    def plusOne(self, digits: list) -> list:
        n = 0
        for i in digits:
            n = n * 10 + i
        n = n + 1
        res = []
        while n>0:
            # insert方法的第一个参数表示位置（下标），第二个参数表示要插入的数据
            res.insert(0, n%10)
            n = n//10
        return res

# 方案二，优化方案，通过观察，我们发现只有数字9，在+1的时候会产生进位，所以我们
# 只需对原始列表，从后向前进行遍历，将连续的值为9的元素替换成0，再将这些连续的9
# 之前的那个元素+1，就可以得到答案了
# 该方案战胜 98.17 % 的 python3 提交记录
class Solution:
    def plusOne(self, digits: list) -> list:
        # 这里必须认真观察range函数的三个参数，它们分别表示起始值、终止值（这个
        # 值是取不到的）、步进值（递增或递减值）
        for index in range(len(digits)-1,-1,-1):
            if digits[index]==9:
                digits[index] = 0   # 如果该位是9，则替换成0
            else:
                digits[index] += 1  # 若不为9，则+1，结束循环
                break
        # 这个else分支用来处理每一位都是9的情况，即需要在这个数列最前方插入元素1
        else:
            digits.insert(0,1)
        return digits

# 以下是本地测试代码，提交时只需复制上面的代码块即可
solution = Solution()
digits = [9,9]
print(solution.plusOne(digits))