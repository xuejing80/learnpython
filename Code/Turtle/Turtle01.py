'''
功能：绘制五角星
重点：创建海龟对象、绘制简单图形并填充
作者：薛景
最后修改于：2019/05/26
'''

import turtle           # 导入海龟的功能库
t = turtle.Turtle()     # 创建一只小海龟，我们称作一个对象
t.shape("turtle")       # 增强趣味性，设置海龟的外形
t.color("red")          # 设置这只海龟的颜色为红色

t.begin_fill()          # 设置海龟的当前位置为填充区域起点
for i in range(5):      # 通过循环，绘制五角星的每一个角
    t.forward(100)
    t.right(72)
    t.forward(100)
    t.left(144)
t.end_fill()            # 设置填充区域的结束位置，并填充上颜色

'''
思考题：如何修改代码，将五角星放在绘图区域的正中央呢？
'''