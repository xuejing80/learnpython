'''
功能：有效的字母异位词
来源：https://leetcode-cn.com/explore/featured/card/top-interview-questions-easy/5/strings/35/
重点：调用collections中的Counter方法对集合元素计数
作者：薛景
最后修改于：2019/07/29
'''

# collections函数库中的Counter方法会对集合中的元素进行计数，只要计数结果相同，我
# 们就认为这两个字符串是有效的字母异位词
# 该方案战胜 92.13 % 的 python3 提交记录
class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        from collections import Counter
        return Counter(s)==Counter(t)
        
        
# 以下是本地测试代码，提交时只需复制上面的代码块即可
solution = Solution()
s = "anagram"
t = "nagaram"
print(solution.isAnagram(s,t))