'''
功能：字符串中的第一个唯一字符
来源：https://leetcode-cn.com/explore/featured/card/top-interview-questions-easy/5/strings/34/
重点：字符串正向和反向查找
作者：薛景
最后修改于：2019/07/28
'''

# 方案一，传统方案，统计每个字符出现的次数，然后从左向右遍历字符串中的字符，若其
# 只出现一次，就返回它的下标
# 该方案战胜 47.63 % 的 python3 提交记录
class Solution:
    def firstUniqChar(self, s: str) -> int:
        res = -1
        dic = {}
        for c in s:
            dic[c] = dic.get(c,0) + 1
        for i in range(len(s)):
            if dic[s[i]]==1:
                res = i
                break
        return res

# 方案二，优化方案，统计26个字母中只出现一次的最小位置
# 该方案战胜 99.72 % 的 python3 提交记录
class Solution:
    def firstUniqChar(self, s: str) -> int:
        alphabet = [chr(i) for i in range(97,123)]      # 构造字母表
        res = []
        for c in alphabet:                              # 遍历字母表
            i = s.find(c)                       # 找到字母第一次出现的位置
            # 下方的i!=-1表示该字母存在于字符串中，i==s.rfind(c)表示无论从左往右
            # 还是从右往左查询，找到的位置都是一样的，即只出现一次
            if i!=-1 and i==s.rfind(c):
                res.append(i)                   # 将满足条件的字母的位置记下
        if res == []:
            return -1                           # 如果结果为空，则返回-1
        else:
            return min(res)                     # 如果结果不为空，返回最小值
        
# 以下是本地测试代码，提交时只需复制上面的代码块即可
solution = Solution()
s = "loveleetcode"
print(solution.firstUniqChar(s))