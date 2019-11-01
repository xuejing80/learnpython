'''
功能：实现 strStr()
来源：https://leetcode-cn.com/explore/featured/card/top-interview-questions-easy/5/strings/38/
重点：循环与else语句的搭配使用
作者：薛景
最后修改于：2019/08/24
'''

# 方案一，传统方案，用两重循环解决此题，第一重循环是待查找的母字符串，第二重循环
# 是欲找到的字符串，这个程序用到了大量的循环与else语句的搭配使用
# 该方案战胜 77.99 % 的 python3 提交记录
class Solution:
    def strStr(self, haystack: str, needle: str) -> int:
        if len(needle)==0:
            return 0
        else:
            for i in range(0,len(haystack)-len(needle)+1):
                for j in range(len(needle)):
                    if haystack[i+j]!=needle[j]:
                        break
                else:
                    return i
            else:
                return -1

# 方案二，Python思维，在Python中有一个非常有用的运算符in，用来判断某数据是否在另
# 外的数据集中，在字符串的运算中，可以用来判断某个字符串是否在另一个字符串中
# 该方案战胜 61.70 % 的 python3 提交记录
class Solution:
    def strStr(self, haystack: str, needle: str) -> int:
        if len(needle)==0:
            return 0
        else:
            if needle in haystack:
                return haystack.index(needle)
            else:
                return -1

# 方案三，在方案一的基础上进一步提高效率，不再是一个一个字符的比较，而是使用切片
# 操作，直接做字符串的比较
# 该方案战胜 91.25 % 的 python3 提交记录
class Solution:
    def strStr(self, haystack: str, needle: str) -> int:
        if len(needle)==0:
            return 0
        else:
            len_needle = len(needle)
            for i in range(0,len(haystack)-len_needle+1):
                if haystack[i:i+len_needle] == needle:
                    return i
            else:
                return -1

# 以下是本地测试代码，提交时只需复制上面的代码块即可
solution = Solution()
haystack = "hello"
needle = "ll"
print(solution.strStr(haystack, needle))

haystack = "aaaaa"
needle = "bba"
print(solution.strStr(haystack, needle))

haystack = "a"
needle = "a"
print(solution.strStr(haystack, needle))