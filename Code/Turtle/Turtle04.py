'''
功能：绘制五星红旗
重点：三角函数的使用、角度和弧度的换算
作者：薛景
最后修改于：2019/05/30
'''
import turtle, math
t = turtle.Turtle()
t.shape("turtle")

def drawStar(x, y, r, color, heading):
    t.up()
    t.goto(x, y)
    t.down()
    t.color(color)
    t.setheading(heading)
    edge=r*math.sin(math.radians(136))/math.sin(math.radians(126))
    t.forward(r)
    t.left(180-18)
    t.begin_fill()
    for i in range(5):
        t.forward(edge)
        t.right(72)
        t.forward(edge)
        t.left(144)
    t.end_fill()

# 画五星红旗的背景，把整个国旗看作600*400大小，左上角的坐标就是(-300,200)
t.color("red")
t.goto(-300,200)
t.begin_fill()
t.forward(600)
t.right(90)
t.forward(400)
t.right(90)
t.forward(600)
t.right(90)
t.forward(400)
t.end_fill()

# 画大星星
drawStar(-200, 100, 60, "yellow", 90)

# 画小星星，最难的就是求每个小星星的朝向，利用小星星和大星星中心点构成的直角三角形可求
# math函数库中反正切函数结果的单位是弧度，务必先用degrees先换算成角度
# 又因为反正切函数的值域在(-90,90)上，所有记得要加180度哟
drawStar(-100, 160, 20, "yellow", math.degrees(math.atan(-60/-100))+180)
drawStar(-60, 120, 20, "yellow", math.degrees(math.atan(-20/-140))+180)
drawStar(-60, 60, 20, "yellow", math.degrees(math.atan(40/-140))+180)
drawStar(-100, 20, 20, "yellow", math.degrees(math.atan(80/-100))+180)

t.hideturtle()