'''
功能：将五角星放置在绘图区域的中央
重点：
作者：薛景
最后修改于：2019/05/26
'''

import turtle
import math             # 接下来的程序中需要使用三角函数，补充导入math函数库
t = turtle.Turtle()
t.shape("turtle")
t.color("red")

# 海龟会从某一个尖角上开始绘制五角星，所以先将海龟移动到尖角上，并调整好方向
t.setheading(90)        # 设置海龟的运动方向为正上方
'''
接下来这条语句有几个知识点需要说明一下：
1. 海龟向上移动的距离应该是五角星的外接圆半径
2. 把该外接圆半径和五角星的短边作为三角形的两条边，就可用正弦定理求得该外接圆半径
3. math函数库中，三角函数参数的单位是弧度，故需要使用radians函数将角度转换成弧度
'''
r=100*math.sin(math.radians(126))/math.sin(math.radians(36))
t.forward(r)
t.left(180-18)          # 18度是五角星尖角度数36的一半，请仔细观察绘制过程

# 调整好方向之后，就可以按照老办法绘制五角星了
t.begin_fill()
for i in range(5):
    t.forward(100)
    t.right(72)
    t.forward(100)
    t.left(144)
t.end_fill()