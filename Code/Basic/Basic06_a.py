'''
功能：计算今天是今年的第几天
重点：获取当前的日期、用列表表示一系列的数、序列元素的表示方法
作者：薛景
最后修改于：2019/05/25
'''

import time             # 导入用于获取当前时间的time函数库

now = time.localtime()  # localtime函数用于获得当前本地的时间
year = now.tm_year      # tm_year表示本地时间的年份
month = now.tm_mon      # tm_mon表示本地时间的月份
day = now.tm_mday       # tm_mday表示本地时间中的日子

# 每个月的天数用数列表示，因为计算机中的序号从0开始，所以第1个数为0，2月为非闰年的天数
days = [0,31,28,31,30,31,30,31,31,30,31,30,31]
# 如果今年是闰年，则修正2月份的天数
if (year%4==0 and year%100!=0) or year%400==0:
    days[2]=29

sumDay = day    # 先把日子放到总天数里面作为初始值
# 接着，使用for循环把当前月之前的每个月的天数都累加起来
for i in range(month):
    sumDay += days[i]

print("今天是今年的第%d天。" % sumDay )