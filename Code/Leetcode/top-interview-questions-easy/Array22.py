'''
功能：买卖股票的最佳时机 II
来源：https://leetcode-cn.com/explore/featured/card/top-interview-questions-easy/1/array/22/
重点：使用True和False存储在变量中表示某种事情是否发生
作者：薛景
最后修改于：2019/06/18
'''
# 方案一，传统方案，使用isBought变量记录当前是否有买入股票，依次遍历价格中的数据
# ，如果股票涨了且没有买入，就以前一天的价格购买，如果股票跌了且已经买入，就以前
# 一天的价格卖出，并将获利计入利润总和profit中，最后需要考虑特殊情况即虽然股票在
# 涨且持有股票，但是已经是最后一个交易日，所以必须将股票卖出并计算利润
# 该方案战胜 47.58 % 的 python3 提交记录
class Solution:
    def maxProfit(self, prices: list) -> int:
        isBought = False    # 初值为False，表示一开始没有持有股票
        profit = 0          # 总利润
        for i in range(1,len(prices)):
            if prices[i]>prices[i-1]:
                if not isBought:
                    boughtPrice = prices[i-1]
                    isBought = True     # 表示已买入股票
            elif prices[i]<prices[i-1]:
                if isBought:
                    profit += prices[i-1] - boughtPrice
                    isBought = False    # 表示已卖出股票
        if isBought:
            profit += prices[-1] - boughtPrice
        return profit

# 方案二，算法优化，通过观察方案一，我们可以看出利润总和其实就是在连续递增的数列
# 中，后一个元素减去前一个元素的差值的总和
# 该方案战胜 92.88 % 的 python3 提交记录
class Solution:
    def maxProfit(self, prices: list) -> int:
        profit = 0
        for i in range(1,len(prices)):
            if prices[i]>prices[i-1]:
                profit += prices[i]-prices[i-1]
        return profit

# 以下是本地测试代码，提交时只需复制上面的代码块即可
solution = Solution()
prices = [7,1,5,3,6,4]
print(solution.maxProfit(prices))