'''
功能：反转字符串
来源：https://leetcode-cn.com/explore/featured/card/top-interview-questions-easy/5/strings/32/
重点：
作者：薛景
最后修改于：2019/07/18
'''

# 这个题目对于Python来说，简直就是没难度呀，哈哈
# 该方案战胜 99.46 % 的 python3 提交记录
class Solution:
    def reverseString(self, s: list) -> None:
        """
        Do not return anything, modify s in-place instead.
        """
        s.reverse()

# 以下是本地测试代码，提交时只需复制上面的代码块即可
solution = Solution()
s = ["H","a","n","n","a","h"]
solution.reverseString(s)
print(s)