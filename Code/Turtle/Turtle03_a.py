'''
功能：绘制好多五角星
重点：自定义函数的用法、参数的作用
作者：薛景
最后修改于：2019/05/30
'''
import turtle, math, random
t = turtle.Turtle()
t.shape("turtle")

def drawStar(x, y, r, color, heading):
    t.up()      # 因为海龟移动过程中会留下痕迹，所以移动之前先提笔up，移动完毕再落笔down
    t.goto(x, y)
    t.down()
    t.color(color)
    t.setheading(heading)
    edge=r*math.sin(math.radians(36))/math.sin(math.radians(126))
    t.forward(r)
    t.left(180-18)
    t.begin_fill()
    for i in range(5):
        t.forward(edge)
        t.right(72)
        t.forward(edge)
        t.left(144)
    t.end_fill()

t.speed(10)         # 因为星星太多了，所以加个速吧，1-10表示速度，0表示不显示动画
for i in range(20):
    x, y = random.randint(-200, 200), random.randint(-200, 200) # 随机产生坐标
    r = random.randint(10, 50)                                  # 随机产生大小
    color = (random.random(), random.random(), random.random()) # 随机产生颜色
    heading = random.randint(0, 360)                            # 随机产生朝向
    drawStar(x, y, r, color, heading)                           # 函数调用
