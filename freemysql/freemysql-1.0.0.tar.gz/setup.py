from distutils.core import setup

setup(
    name = "freemysql",
    version = "1.0.0",
    keywords = ("database", "mysql"),
    description = "help to manipulate mysql more easily",

    author = "liuliuliu0605",
    author_email = "liuliuliu0605@qq.com",

    py_modules = ["Mysql"],
    install_requires = [
        "pymysql==0.9.3"
    ],
)

