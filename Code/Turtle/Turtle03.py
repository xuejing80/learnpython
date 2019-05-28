'''
功能：绘制两个五角星
重点：自定义函数的用法、参数的作用
作者：薛景
最后修改于：2019/05/28
'''
import turtle, math
t = turtle.Turtle()
t.shape("turtle")
t.color("red")

def drawStar(x, y):
    t.up()      # 因为海龟移动过程中会留下痕迹，所以移动之前先提笔up，移动完毕再落笔down
    t.goto(x, y)
    t.down()
    t.setheading(90)
    edge=100*math.sin(math.radians(136))/math.sin(math.radians(126))
    t.forward(100)
    t.left(180-18)
    t.begin_fill()
    for i in range(5):
        t.forward(edge)
        t.right(72)
        t.forward(edge)
        t.left(144)
    t.end_fill()

drawStar(200, 0)
drawStar(-200,0)
'''
思考题：如何给函数加上更多的参数，定义星星的位置、大小、颜色、朝向
'''