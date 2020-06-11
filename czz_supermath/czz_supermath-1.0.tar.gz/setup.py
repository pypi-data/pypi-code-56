from distutils.core import setup
setup(
    name='czz_supermath',#对外我们模块的名称
    version='1.0', #版本号
    description='这是一个对外发布的模块，测试哦', #描述
    author='czz',#作者
    author_email='2019271424@qq.com',
    py_modules=['czz_supermath.demo1','czz_supermath.demo2'] #要帆布的模块
)