from numpy import array,linspace
from sympy import Symbol,log,E,solve,symbols
from matplotlib.pyplot import plot,show,ylabel,xlabel,scatter

class FunctionError(Exception):
    def __str__(self):
        return '暂不支持该拟合函数的计算。。。'

def __exponential_function(x,y):
    x2 = x ** 2
    a,b = 0,0
    d = len(y)
    e,f = 0,0
    for i in range(len(y)):
        a += x2[i]
        b += x[i]
        e += x[i] * log(y[i],10)
        f += log(y[i],10)
    c = b
    D = a * d - c * b
    D1 = e * d - f * b
    D2 = a * f - c * e
    return ((D1 / D) / log(E,10)),(10 ** (D2 / D))

EXPONENTIAL_FUNCTION = __exponential_function

def __quadratic_function(x,y):
    x4 = x ** 4
    x3 = x ** 3
    x2 = x ** 2
    a,b = 0,0
    c = 0
    f = 0
    i = len(y)
    j,k = 0,0
    l = 0
    for i in range(len(y)):
        a += x4[i]
        b += x3[i]
        c += x2[i]
        f += x[i]
        j += (x2[i] * y[i])
        k += (y[i] * x[i])
        l += y[i]
    g,e = c,c
    h = f
    d = b
    x,y,z = symbols('x y z')
    f1 = a*x+b*y+c*z-j
    f2 = d*x+e*y+f*z-k
    f3 = g*x+h*y+i*z-l
    solution = solve([f1,f2,f3],[x,y,z])
    return solution[x],solution[y],solution[z]

QUADRATIC_FUNCTION = __quadratic_function

class Least_squares:
    '''
    该类用于曲线拟合
    参数x：x轴坐标
    参数y：y轴坐标
    参数n：拟合函数类型，包括None（一阶线性方程），EXPONENTIAL_FUNCTION（指数方程），QUADRATIC_FUNCTION（二次方程）
    '''
    def __init__(self,x,y,n=None):
        self.x = array(x)
        self.y = array(y)
        self.n = n
        if self.n == None:
            self.__z1 = self.x ** 2
            self.__a = 0
            self.__b = 0
            self.__c = 0
            self.__d = 0
            self.__e,self.__f = 0,0
            for i in range(len(y)):
                self.__a += self.__z1[i]
                self.__b += self.x[i]
                self.__e += (self.x[i] * self.y[i])
                self.__f += self.y[i]
            self.__c = self.__b
            self.__d = int(len(y))
            self.__D = ((self.__a * self.__d) - (self.__c * self.__b))
            self.__D1 = ((self.__e * self.__d) - (self.__f * self.__b))
            self.A = self.__D1 / self.__D
            self.__D2 = ((self.__a * self.__f) - (self.__c * self.__e))
            self.B = self.__D2 / self.__D
        elif self.n == EXPONENTIAL_FUNCTION:
            self.M,self.K = self.n(self.x,self.y)
        elif self.n == QUADRATIC_FUNCTION:
            self.A,self.B,self.C = self.n(self.x,self.y)
        else:
            raise FunctionError

    def show(self):
        '''
        绘制图像
        '''
        self.__X = linspace((self.x[0] - 3),(self.x[-1] + 3),1000)
        if self.n == None:
            self.__Y = (self.A * self.__X) + self.B
        elif self.n == EXPONENTIAL_FUNCTION:
            self.__Y = self.K * (E ** (self.M * self.__X))
        elif self.n == QUADRATIC_FUNCTION:
            self.__Y = self.A * (self.__X ** 2) + self.B * self.__X + self.C
        scatter(self.x,self.y,s=50)
        plot(self.__X,self.__Y)
        ylabel('Y')
        xlabel('X')
        show()

    def get_function(self):
        '''
        :return: 返回拟合函数
        '''
        self.__variable = Symbol('x')
        if self.n == None:
            return self.A * self.__variable + self.B
        elif self.n == EXPONENTIAL_FUNCTION:
            return self.K * (E ** (self.M * self.__variable))
        elif self.n == QUADRATIC_FUNCTION:
            return self.A * (self.__variable ** 2) + self.B * self.__variable + self.C

    def get_mean_square_error(self):
        '''
        :return: 返回均方误差
        '''
        self.__M = 0
        if self.n == None:
            for i in range(len(self.y)):
                self.__M += ((self.y[i] - (self.A * self.x[i] + self.B)) ** 2)
            return self.__M ** 0.5
        elif self.n == EXPONENTIAL_FUNCTION:
            for i in range(len(self.y)):
                self.__M += (self.y[i] - (self.K * (E ** (self.M * self.x[i])))) ** 2
            return self.__M ** 0.5
        elif self.n == QUADRATIC_FUNCTION:
            for i in range(len(self.y)):
                self.__M += (self.y[i] - (self.A * (self.x[i] ** 2) + self.B * self.x[i] + self.C)) ** 2
            return self.__M ** 0.5

if __name__ == '__main__':
    l = Least_squares([3,6,9,12,15,18,21,24],[57.6,41.9,31,22.7,16.6,12.2,8.9,6.5],n=QUADRATIC_FUNCTION)
    print(f'{l.get_function()}\n{l.get_mean_square_error()}')
    l.show()