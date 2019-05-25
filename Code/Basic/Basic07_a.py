'''
功能：判断三角形的类型
重点：分支结构的复杂嵌套
作者：薛景
最后修改于：2019/05/25
'''

from math import isclose    # 从math函数库中导入单个函数isclose
'''
为什么要导入这个isclose函数呢，这里有一个非常重要的问题，那就是如何输入一个等腰直角三角
形的三条边呢？比如：“1.4142 1.4142 2”这三个数，严格意义上它们并不满足a**2+b**2==c**2，
可是我们已经可以近似地认为这三个数可以组成一个等腰直角三角形了，所以本程序用a**2+b**2是
否足够接近c**2来判定勾股定理是否成立。举例说明：
    isclose(a, b, abs_tol=1e-4)表示a和b之间的差距是否小于10的-4次方
其中，“1e-4”是实数的科学计数法表示，等价于1*10的-4次方，即0.0001
'''

a,b,c = input("请输入三角形的三条边a、b、c，用空格分开：").split()
a,b,c = float(a),float(b),float(c)

# 只有三条边都大于0，且任意两边之和大于第三边才可以构成三角形哟
if min(a,b,c)>0 and a+b>c and a+c>b and b+c>a:
    if a==b==c:     # 等边三角的判断条件
        print("这是一个等边三角形")
    elif isclose(a**2+b**2, c**2, abs_tol=1e-4) or \
            isclose(b**2+c**2, a**2, abs_tol=1e-4) or \
                isclose(a**2+c**2, b**2, abs_tol=1e-4): 
            # 语句太长了可以用续行符“\”进行强制换行，告诉Python这三行其实是一起的
        if a==b or b==c or a==c:  # 等腰三角的判断条件
            print("这是一个等腰直角三角形")
        else: 
            print("这是一个直角三角形")
    elif a==b or b==c or a==c:
        print("这是一个等腰三角形")
    else:
        print("这是一个普通三角形")
else:
    print("您输入的三个数构成不了三角形")