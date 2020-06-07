import numpy as np
import pandas as pd
import os
import re



class Fmesh(object):
    def __init__(self,filename):
        self.filename = filename
        self._iints = None
        self._jints = None
        self._kints = None
        self._emesh = None
        self._out = None
    #---------------------属性----------------------
    @property
    def iints(self):
        return self._iints
    @property
    def jints(self):
        return self._jints
    @property
    def kints(self):
        return self._kints
    @property
    def emesh(self):
        return self._emesh
    @property
    def out(self):
        return self._out

    #----------------------属性设置--------------------
    @iints.setter
    def iints(self,iints):
        self._iints = iints
    @jints.setter
    def jints(self,iints):
        self._jints = jints
    @kints.setter
    def kints(self,iints):
        self._kints = kints
    @emesh.setter
    def emesh(self,emesh):
        self._emesh = emesh
    @out.setter
    def out(self,out):
        self._out = out
    #----------------------属性删除--------------------
    @iints.deleter
    def iints(self):
        del self._iints
    @jints.deleter
    def jints(self):
        del self._jints
    @kints.deleter
    def kints(self):
        del self._kints
    @emesh.deleter
    def emesh(self):
        del self._emesh
    @out.deleter
    def out(self):
        del self._emesh
    #---------------------------End------------------------

    #---------------------读取信息------------------------------
    def run(self):
        if(self._out=="ij" or self._out=="ik" or self._out=="jk"):
            data = self.read_ijk()
            self.output_csv_ijk(data)
        elif(self._out=="col" or self._out=="cf"):
            data = self.read_col()
            self.output_csv_col(data)
        else:
            print("Errors,Please input correct forms!")


    #--------------------处理列格式Fmesh数据("col" or "cf")--------------
    def read_col(self):
        total_data = []
        with open(self.filename,"r") as f:
            line = f.readline()
            while(line):
                if(re.match("\s*Energy",line)):
                    line = f.readline()
                    while(len(line.split())!=0):
                        data = line.split()
                        new_data = [float(value) for value in data]
                        total_data.append(new_data)
                        line = f.readline()
                line = f.readline()
        # print(total_data)
        return total_data

    #--------------------处理2D矩阵格式Fmesh数据("ij" "ik","jk")---------
    def read_ijk(self):
        total_data=[]
        with open(self.filename,"r") as f:
            line = f.readline()
            while(line):
                if(re.match("Energy Bin",line)):
                    line=f.readline()
                    while(line):
                        for i in range(self._emesh):
                            if(re.match("\s*Tally Results",line)):
                                line=f.readline()
                                line = f.readline()
                                while(len(line.split())!=0):
                                    data = line.split()[1:]
                                    new_data = [float(value) for value in data]
                                    total_data.append(new_data)
                                    line = f.readline()
                        line = f.readline()
                line = f.readline()
        return total_data


    #-------------------输出数据pandas -->csv格式-------------------------
    def output_csv_ijk(self,datas):
        df = pd.DataFrame(datas)
        print(df[0:10])
        xyz_bin = 10
        for i in range(self._emesh):
            ebin = "Ebins"+str(i)
            if not os.path.exists(ebin):
                os.mkdir(ebin)
            for j in range(xyz_bin):
                left  = xyz_bin*self._jints*i+self._jints*j
                right = xyz_bin*self._jints*i+self._jints*(j+1)
                delta_data = df[left:right]
                str_data = "bins_"+str(j)+".csv"
                bin_data = os.path.join(ebin,str_data)
                delta_data.to_csv(bin_data)
        pass
    def output_csv_col(self,data):
        df=pd.DataFrame(data)
        df.to_csv("Fmesh_col.csv")



if __name__ == "__main__":
    # print("Hell Fmesh card!")
    a={'F2':[1],'F4':[4,5]}
    value=4
    for i in a["F4"]:
        if(value==i):
            print("Good")
    print(a["F2"])
    # value=[i for i,j in enumerate(a) if j=='F4']
    # a1={key:value for key,value in a.items() if key=="F4"}
    # print(a1)
    # for i in (None or [5,6,7]):
    #     print(i)
    # for i,j in enumerate(a):
    #     print(i,j)
    # for i,j in a.items():
    #     print(i,j)
    #     for k in j:
    #         print(k)
    #------------------Test---------------------------
    # filename = "F:\Python\PyShielding\openSheild\openSheild\meshtaq"
    # style="ij"
    # f = Fmesh(filename)
    # f.out = "col"
    # f.run()
    # print(f.out)
    # read_mesh(filename,style)