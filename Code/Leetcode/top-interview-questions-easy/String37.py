'''
功能：字符串转换整数 (atoi)
来源：https://leetcode-cn.com/explore/featured/card/top-interview-questions-easy/5/strings/37/
重点：正则表达式、星号表达式
作者：薛景
最后修改于：2019/08/04
'''

# 方案一，传统思维方式，思考过程见注释
# 该方案战胜 72.56 % 的 python3 提交记录
class Solution:
    def myAtoi(self, str: str) -> int:
        str = str.lstrip()                      # 去掉左边多余空格
        if str == "":                           # 如果字符串为空，返回0
            return 0
        res,sign = 0,1                          # 结果初值为0，符号位初值为1
        if str[0]=="+" or str[0]=="-":          # 字符串如果以正负号开始，记下符号位
            sign = -1 if str[0]=="-" else 1     
            start = 1                           # 如果有正负号，从下标1开始转换
        else:                                   
            start = 0                           # 如果没有正负号，从下标0开始转换
        for i in range(start,len(str)):
            if str[i].isdigit():
                res = res * 10 + int(str[i])    # 将数字字符的值累加进结果
            else:
                break
        res = res*sign                          # 根据符号位，还原结果的正负
        if res>2**31-1:                         # 这个if是用来返回大小超限的结果
            return 2**31-1
        elif res<-2**31:
            return -2**31
        else:
            return res

# 方案二，使用正则表达式，这玩意儿厉害了！同时，还需要星号表达式来帮忙处理找不到匹配项返回0的问题。
# 该方案
class Solution:
    def myAtoi(self, str: str) -> int:
        """
        对下面语句中的正则表达式做个解释：
        ^：上尖号放在最前面表示所查找的内容必须在字符串的开头，效果是忽略字符串中其他位置的匹配项
        [\+\-]：方括号表示匹配其中的任一字符，效果就是匹配加号或者减号
        ?：问号表示前面匹配的那个字符可有可无，效果就是可能没有符号
        \d：这个是固定用法，表示一个数字
        +：加号表示前面字符的出现次数可以使一个或多个，效果是匹配任意长度的数字
        """
        import re
        # 因为findall函数返回的是一个列表，要将其中的内容取出来必须使用星号表达式(*)
        # 使用星号表达式的好处是：如果没有匹配项，即对于空列表[]使用星号表达式取整，结果为0
        return max(min(int(*re.findall('^[\+\-]?\d+', str.lstrip())), 2**31-1), -2**31)

# 以下是本地测试代码，提交时只需复制上面的代码块即可
solution = Solution()
print(solution.myAtoi("42"))
print(solution.myAtoi("   -42"))
print(solution.myAtoi("4193 with words"))
print(solution.myAtoi("words and 987"))
print(solution.myAtoi("-91283472332"))
print(solution.myAtoi("  0000000000012345678"))