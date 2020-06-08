import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import copy
from  matplotlib import  cm
import meteva

def bar(array,name_list_dict = None,x = None,legend = None,y = None,save_path = None,show = False,dpi = 300,title = None):

    sup_fontsize = 10
    shape = array.shape
    if shape.size ==1:
        xlabel = list(name_list_dict.keys())[0]
        xticks = name_list_dict[xlabel]
        width = meteva.base.plot_tools.caculate_axis_width(xticks, sup_fontsize)
        if width > 10:
            for i in range(len(xticks)):
                if i % 2 == 1:
                    xticks[i] = "|\n" + xticks[i]
            width = 10
        elif width < 5:
            width = 5
        height = width / 2
        fig = plt.figure(figsize=(width, height), dpi=dpi)
        x = np.arange(array.size)
        plt.bar(x,array)
        plt.xticks(x,xticks,fontsize = sup_fontsize * 0.8)
        plt.yticks(fontsize=sup_fontsize * 0.8)
        plt.xlabel(xlabel,fontdict=sup_fontsize * 0.9)
        plt.ylabel()

    elif shape.size ==2:
        pass
    elif shape.size ==3:
        pass
    else:
        print("array不能超过3维")
        return
        xticks = []
        for index in index_list:
            if not type(index) == str:
                index = str(index)
            xticks.append(index)


    p_ob = np.array(ob_num_list) / total_num
    p_fo = np.array(fo_num_list) / total_num
    p_fo_list.append(p_fo)
    x = np.arange(len(index_list))

    if line == 0:
        x1 = x - 0.1 + (line + 1.5) * 0.16
        plt.bar(x1, p_ob, width=0.15, label=label[line])
    x1 = x - 0.1 + (line + 1 + 1.5) * 0.16
    plt.bar(x1, p_fo, width=0.15, label=label[line + 1])
    plt.legend(fontsize = sup_fontsize *0.9)
    plt.xlabel("类别", fontsize=sup_fontsize *0.9)

    plt.xticks(x, xticks, fontsize=sup_fontsize *0.8)
    plt.yticks(fontsize=sup_fontsize *0.8)
    plt.ylabel("样本占比", fontsize= sup_fontsize *0.9)
    plt.title(title, fontsize=sup_fontsize)
    p_fo = np.array(p_fo_list)
    ymax = max(np.max(p_ob), np.max(p_fo)) * 1.4
    plt.ylim(0.0, ymax)
    if save_path is None:
        show = True
    else:
        plt.savefig(save_path,bbox_inches='tight')
        print("检验结果已以图片形式保存至" + save_path)
    if show:
        plt.show()
    plt.close()



def frequency_histogram(ob, fo, member_list=None, grade_list=None, save_path=None,show = False,dpi = 300, title="频率统计图"):
    '''
    frequency_histogram 对比测试数据和实况数据的发生的频率
    :param ob: 实况数据 任意维numpy数组
    :param fo: 预测数据 任意维numpy数组,Fo.shape 和Ob.shape一致
    :param grade_list: 如果该参数为None，观测或预报值出现过的值都作为分类标记.
    如果该参数不为None，它必须是一个从小到大排列的实数，以其中列出的数值划分出的多个区间作为分类标签。
    对于预报和观测值不为整数的情况，grade_list 不能设置为None。
    :param save_path: 保存地址
    :return: 无
    '''
    total_num = ob.size
    Fo_shape = fo.shape
    Ob_shape = ob.shape
    Ob_shpe_list = list(Ob_shape)
    size = len(Ob_shpe_list)
    ind = -size
    Fo_Ob_index = list(Fo_shape[ind:])
    p_fo_list = []
    if Fo_Ob_index != Ob_shpe_list:
        print('实况数据和观测数据维度不匹配')
        return
    Ob_shpe_list.insert(0, -1)
    new_Fo_shape = tuple(Ob_shpe_list)

    legend = ['观测']
    if member_list is None:
        if new_Fo_shape[0] == 1:
            legend.append('预报')
        else:
            for i in range(new_Fo_shape[0]):
                legend.append('预报' + str(i + 1))
    else:
        legend.extend(member_list)

    result_array = meteva.method.frequency_table(ob, fo, grade_list=grade_list)
    if grade_list is not None:
        axis = ["<" + str(grade_list[0])]
        for index in range(len(grade_list) - 1):
            axis.append("[" + str(grade_list[index]) + "," + str(grade_list[index + 1]) + ")")
            axis.append(">=" + str(grade_list[-1]))
    else:
        new_fo = copy.deepcopy(fo).flatten()
        new_ob = copy.deepcopy(ob).flatten()
        fo_list = list(set(new_fo.tolist()))
        fo_list.extend(list(set(new_ob.tolist())))
        axis = list(set(fo_list))
    name_list_list = [legend,axis]
    bar(result_array,name_list_list,save_path = save_path,dpi = dpi,title=title)







def frequency_histogram1(ob, fo,grade_list = None, save_path=None,title = "频率统计图"):
    '''
    frequency_histogram 对比测试数据和实况数据的发生的频率
    :param ob: 实况数据 任意维numpy数组
    :param fo: 预测数据 任意维numpy数组,Fo.shape 和Ob.shape一致
    :param grade_list: 如果该参数为None，观测或预报值出现过的值都作为分类标记.
    如果该参数不为None，它必须是一个从小到大排列的实数，以其中列出的数值划分出的多个区间作为分类标签。
    对于预报和观测值不为整数的情况，grade_list 不能设置为None。
    :param save_path: 保存地址
    :return: 无
    '''
    total_num = ob.size

    if grade_list is not None:

        shape = ob.shape
        new_ob = np.zeros(shape)
        new_fo = np.zeros(shape)
        index_list =["<" + str(grade_list[0])]
        ob_index_list = np.where(ob<grade_list[0])
        ob_num_list = [len(ob_index_list[0])]
        fo_index_list = np.where(fo < grade_list[0])
        fo_num_list = [len(fo_index_list[0])]
        for index in range(len(grade_list) - 1):
            ob_index_list = np.where((grade_list[index] <= ob) & (ob < grade_list[index + 1]))
            ob_num_list.append(len(ob_index_list[0]))
            fo_index_list = np.where((grade_list[index] <= fo) & (fo < grade_list[index + 1]))
            fo_num_list.append(len(fo_index_list[0]))
            index_list.append("["+str(grade_list[index]) + "," + str(grade_list[index+1]) + ")")
        ob_index_list = np.where(grade_list[-1] <= ob)
        ob_num_list.append(len(ob_index_list[0]))
        fo_index_list = np.where(grade_list[-1] <= fo)
        fo_num_list.append(len(fo_index_list[0]))
        index_list.append(">=" + str(grade_list[-1]))

    else:
        new_fo = copy.deepcopy(fo).flatten()
        new_ob = copy.deepcopy(ob).flatten()
        index_list = list(set(np.hstack((new_ob, new_fo))))
        ob_num_list = []
        fo_num_list = []
        for i in range(len(index_list)):
            ob_index_list = np.where(ob == index_list[i])
            ob_num_list.append(len(ob_index_list[0]))
            fo_index_list = np.where(fo == index_list[i])
            fo_num_list.append(len(fo_index_list[0]))

    #计算最大的横坐标字符串
    max_str_len = 1
    for index in index_list:
        if not type(index) ==str:
            index = str(index)
        if max_str_len <len(index):
            max_str_len = len(index)

    #print(max_str_len)
    width = 0.5 + (1+ max_str_len)* 0.1 * len(index_list)
    if width < 6:
        width = 6
    height = 6
    fig = plt.figure(figsize=(width, height))

    p_ob = np.array(ob_num_list)/total_num
    p_fo = np.array(fo_num_list)/total_num
    x = np.arange(len(index_list))
    plt.bar(x - 0.1, p_ob, width=0.2, facecolor="r", label="观测")
    plt.bar(x + 0.1, p_fo, width=0.2, facecolor="b", label="预报")
    plt.legend()
    plt.xlabel("类别", fontsize=14)



    plt.xticks(x,index_list,fontsize = 12)
    plt.yticks(fontsize = 14)
    plt.ylabel("样本占比", fontsize=14)
    plt.title(title,fontsize = 14)
    ymax = max(np.max(p_ob),np.max(p_fo))* 1.4
    plt.ylim(0.0, ymax)
    if save_path is None:
        plt.show()
    else:
        plt.savefig(save_path)
        print("检验结果已以图片形式保存至" + save_path)
    plt.close()


