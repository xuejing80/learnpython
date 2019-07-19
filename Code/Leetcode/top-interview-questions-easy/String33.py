'''
功能：整数反转
来源：https://leetcode-cn.com/explore/featured/card/top-interview-questions-easy/5/strings/33/
重点：整数逆序算法
作者：薛景
最后修改于：2019/07/19
'''

# 本题需要分成正数和负数两种情况讨论，所以我们用sign存下该数的符号，然后对其求绝
# 对值，再统一进行正整数的逆序算法，以化简问题难度
# 该方案战胜 88.27 % 的 python3 提交记录
class Solution:
    def reverse(self, x: int) -> int:
        sign = 1 if x>=0 else -1    # 符号位
        res = 0
        x = abs(x)                  # 求绝对值
        while x>0:
            res = res*10 + x%10     # 求余数计算原数的最后一位，并计入结果
            x = x // 10             # 通过整除，去掉原数的最后一位
        res = sign * res
        # 下方的代码是为了满足题目对结果范围的限定而编写的
        if -2**31 <= res <= 2**31-1:
            return res
        else:
            return 0

# 以下是本地测试代码，提交时只需复制上面的代码块即可
solution = Solution()
print(solution.reverse(-123))