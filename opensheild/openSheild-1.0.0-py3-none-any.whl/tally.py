import numpy as np
import pandas as pd
import re
import os
from collections import defaultdict
import sys


class Tally(object):
    def __init__(self,filename,mode=None):
        self.filename = filename
        self.mode = mode
        self._ftally = None
        self._cell = None
        self._surface = None
        self._energy_bin=1           #能量间隔数
        self.fdatas=self.total_tallies()  #文件中包含的所要处理的计数卡中的cell或surface

    def __repr__(self):
        return "MCNP Tally processing..."
    
    #------------------Basic property---------
    @property
    def ftally(self):
        return self._ftally
    @property
    def cell(self):
        return self._cell
    @property
    def surface(self):
        return self._surface
    @property
    def energy_bin(self):
        return self._energy_bin
    
    #----------Setting the property value------------
    @ftally.setter
    def ftally(self,ftally):
        self._ftally = ftally
    @cell.setter
    def cell(self,cell):
        if(self._ftally==None):
            sys.stderr.write("Tally card error:Please check F tally card input!")
            raise SystemExit(1)
        elif(self.bool_tally(cell)):
            sys.stderr.write("Tally card error:Please check cell card id!")
            raise SystemExit(1)
        else:
            self._cell=cell

    @surface.setter
    def surface(self,surface):
        if(self._ftally==None and self.bool_tally(surface)):
            sys.stderr.write("Tally card error:Please check F tally card input or correct surface!!!")
            raise SystemExit(1)
        elif(self.bool_tally(surface)):
            sys.stderr.write("Tally card error:Please check surface card id!")
            raise SystemExit(1)
        else:
            self._surface=surface

    @energy_bin.setter
    def energy_bin(self,energy_bin):
        self._energy_bin = energy_bin
    
    def bool_tally(self,value):
        for index in self.fdatas[self._ftally]:
            if(index==value):
                return 0
            return 1

    #--------------------属性删除---------------------------
    @ftally.deleter
    def ftally(self):
        del self._ftally
    @cell.deleter
    def cell(self):
        del self._cell
    @surface.deleter
    def deleter(self):
        del self.cell_surface
    @energy_bin.deleter
    def energy_bin(self):
        del self._energy_bin
    #------------------End------------------------------------

    #-------------------------End-------------------------

    #------------------------------处理并运行函数----------------------
    # 第一种情况：tally不输出默认为全部输出
    # 第二种情况：cell or surface未指定，则输出tally的全部曲面或栅元对应的数据
    # 第三种情况：特定的tally对应的特定的cell or surface
    # 第四种情况：异常处理
    #
    #---------------------------------End------------------------------
    def run(self):
        #-------------------条件判断-------------------------------
        try:
            if(self._ftally==None):
                fdatas=self.fdatas
                self.run_batch()   #默认全部输出
                # print(fdatas)
            elif(self._cell==None):
                if(self._surface==None):
                    fdatas={key:value for key,value in self.fdatas.items() if key==self._ftally}
                    self.run_batch(fdatas)
                    # print(fdatas)
            else:
                fdatas=defaultdict(list)
                for cell in (self._cell or self._surface):
                    fdatas[self._ftally].append(cell)
                self.run_batch(fdatas)
                # print(fdatas)
        except ValueError as err:
            print("Value Error:{0}".format(err))
        #------------------End------------------------------------
        
        #---------------------开始提取------------------------------
        #
        #----------------------End---------------------------------
        # fdatas={"F16":[4011,4012],"F2":[38]}
        # for ft,cs in fdatas.items():
        #     if not os.path.exists(ft):
        #         os.mkdir(ft)
        #     for cell in cs:
        #         datas = self.extract_data(ft,cell)
        #         self.export_data(datas,ft,cell)
        #         print(ft,cell)
        print("Finished run Ftally")

    def run_batch(self,fdatas):
        for ft,cs in fdatas.items():
            if not os.path.exists(ft):
                os.mkdir(ft)
            for cell in cs:
                datas= self.extract_data(ft,cell)
                self.export_data(datas,ft,cell)

    #----------------Mode one[normal]--------------------------------
    """
    材料辐照损伤计算MCNP输出文件的后处理数据，模式FQN为缺省
    
    """
    def radiation_mode(self):
        pass



    #----------------Mode two[special]----------------------------
    """
    反应堆屏蔽计算MCNP后处理函数，模式为：FQ0 E S F
    """
    def sheilding_mode(self):
        bins=4         #能量间隔数目
        flag=1         #作用为匹配是否找到了cell/surface
        with open(self.filename,'r') as f:
            line = f.readline()
            str_tally="1tally\s*"+self._ftally.strip('F')+"\s*nps"
            while(line):
                if(re.match(str_tally,line)):     # 找到记录数据的开始tally+cell/surface
                    print(f.tell())
                    while(bins!=0):
                        if(re.match('\senergy bin',line)):
                            line = f.readline()
                            while(flag):
                                if(re.match('\s*cell:',line)):
                                    cells_number = line.split()
                                    for index,number in enumerate(cells_number):
                                        if(str(self._cell)==number):
                                            flag=0
                                            print(index,number)
                                line=f.readline()
                            flag=1
                            line = f.readline()
                            bins = bins-1
                        line = f.readline()
                line = f.readline()
        pass
    #------------------------------提取函数-----------------------------
    # 输入参数：单个曲面或栅元  或者元组(12,13,15)
    #
    # 输出参数：一系列曲面或栅元对应的数据
    #--------------------------------End------------------------------
    def extract_data(self,tally,cell_surface):
        bins=self._energy_bin
        seg,fdata = [],[]
        flag=1                            #作用为匹配是否找到了cell/surface
        with open(self.filename,'r') as f:
            line = f.readline()
            str_tally="1tally\s*"+tally.strip('F')+"\s*nps"
            while(line):
                if(re.match(str_tally,line)):
                    while(bins!=0):
                        if(re.match("\senergy bin",line)):
                            line = f.readline()
                            while(flag):
                                if(re.match("\s*(cell|surface):",line)):
                                    cells_number = line.split()
                                    for index,number in enumerate(cells_number):
                                        if(str(cell_surface)==number):
                                            flag=0
                                            layers=len(cells_number)-1  #找到了特定的那个cell或者surface所在的列
                                            #----------------------读取数据--------------------------
                                            line=f.readline()
                                            line=f.readline()
                                            while(len(line.split())==2*layers+1):
                                                data = line.split()
                                                seg.append(float(data[0]))
                                                fdata.append(float(data[2*(index-1)+1]))
                                                line=f.readline()
                                            #---------------------End---------------------------
                                line=f.readline()
                            flag=1
                            line=f.readline()
                            line=f.readline()
                            bins=bins-1
                        line = f.readline()
                line=f.readline()
        seg_fdata=np.array([seg,fdata])
        return seg_fdata


    #---------------Export your data in the dirs----------------
    def export_data(self,data,tally,cell):
        bins=self._energy_bin
        m,n = data.shape
        segments=int(n/bins)
        seg=data[0,:][0:segments].reshape(1,segments)
        fta = data[1,:].reshape(bins,segments)
        result = np.vstack((seg,fta)).T
        result_pd=pd.DataFrame(result)
        str_result=tally+'_'+str(cell)+".csv"
        path=os.path.join(tally,str_result)
        result_pd.to_csv(path)

    #-------------------------End------------------------------

    #------------------------提取所有栅元----------------------
    def total_tallies(self):
        fdatas = defaultdict(list)
        with open(self.filename,'r') as f:
            line = f.readline()
            while(line):
                if(re.match('\s*[0-9]*-\s*F[0-9]+:',line)):
                    fdata = line.split()
                    f_tally = fdata[1][:-2]
                    f_cell_surface=fdata[2:]
                    for index in f_cell_surface:
                        fdatas[f_tally].append(int(index))
                line=f.readline()
        return fdatas
    #-------------------------End----------------------------


    

if __name__=="__main__":
    print("MCNP post-processing....")
    t = Tally("F:\Python\PyShielding\openSheild\openSheild\inp.out")
    t.ftally="F302"
    t.cell = [36]
    # t.run()
    # t.total_tallies()
    print(type(t.ftally),type(t.cell))
