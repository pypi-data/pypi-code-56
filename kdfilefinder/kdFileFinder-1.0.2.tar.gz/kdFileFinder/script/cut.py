'''
剪切脚本
Created on 2019年3月26日

@author: bkd
'''


class cut:
    def execute(self, app, sp):
        # 设置剪切的参数
        sp["pasteType"] = "cut"
        sp["pastePath"] = sp["path"]
        sp["pasteFileList"] = sp["fileList"]
