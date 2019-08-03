'''
功能：验证回文字符串
来源：https://leetcode-cn.com/explore/featured/card/top-interview-questions-easy/5/strings/36/
重点：字符串函数、列表生成式、正则表达式
作者：薛景
最后修改于：2019/08/03
'''

# 方案一，传统方案，将原始字符串中的大写字母全部转换成小写字母，再把字母和数字拿
# 出来构成新字符串，最后只需判断生成的字符串是否是回文即可
# 该方案战胜 71.34 % 的 python3 提交记录
class Solution:
    def isPalindrome(self, s: str) -> bool:
        s = s.lower()
        result = ''.join([x for x in s if x.isalpha() or x.isdigit()])
        return result[::-1]==result

# 方案二，使用正则表达式，关于正则表达式的概念，请自行百度，简单的说，就是使用某
# 个规则对字符串的内容进行匹配，我们使用正则表达式将非字母和数字的字符从字符串中
# 去除掉，这种方法的效率比方案一高很多
# 该方案战胜 97.42 % 的 python3 提交记录
class Solution:
    def isPalindrome(self, s: str) -> bool:
    	import re
    	s = s.lower()
    	result = re.sub('[^0-9a-z]+', '', s)
    	return result[::-1]==result

# 以下是本地测试代码，提交时只需复制上面的代码块即可
solution = Solution()
s = "A man, a plan, a canal: Panama"
print(solution.isPalindrome(s))