# coding = utf-8
from numpy import array, inner, linalg


def compare2mz(mz1, mz2, ppm_tol = 20):
    delta = mz2 * ppm_tol / 1000000
    mz2_up = mz2 + delta
    mz2_down = mz2 - delta
    if mz1 > mz2_up:
        return "mz2_up"
    elif mz1 < mz2_down:
        return "mz1_up"
    else:
        return "upup"


# 计算两个向量的cos similarity，使用0.5+0.5cos归一化
def cal_cosin_dis(ints1_list, ints2_list):
    if len(ints1_list) != len(ints2_list):
        print("wrong")
        return 
    else:
        a1 = array(ints1_list)
        a2 = array(ints2_list)
        cos = inner(a1, a2)/linalg.norm(a1)/linalg.norm(a2)
        return 0.5+0.5*cos


def cal_ints_dis(ints1_list, ints2_list):
    if len(ints1_list) != len(ints2_list):
        print("wrong")
        return 
    else:
        max_ints1 = max(ints1_list)
        max_ints2 = max(ints2_list)

        dist = 0
        for i in range(len(ints1_list)):
            int_v = [ints1_list[i]/max_ints1, ints2_list[i]/max_ints2]
            if 0 in int_v:
                dist += sum(int_v)
            else:
                dist += pow((int_v[0]-int_v[1]), 2)
        return dist


# 对齐两张谱图，对于单独存在的谱峰，将增加其mz，但intnsity变为0。等效，但长度变得相同，便于后面操作
def alignTwoSpec(ref_spec, spec2):
    mz1_list = [x[0] for x in ref_spec]
    mz2_list = [x[0] for x in spec2]
    ints1_list = []
    ints2_list = []
    mz_merge_list = []
    idx1 = 0
    idx2 = 0
    while idx1 < len(mz1_list) and idx2 < len(mz2_list):
        state = compare2mz(mz1_list[idx1], mz2_list[idx2])
        if state == 'mz1_up':
            ints1_list.append(ref_spec[idx1][1])
            ints2_list.append(0)
            mz_merge_list.append(mz1_list[idx1])
            idx1 += 1
        elif state == "mz2_up":
            ints2_list.append(spec2[idx2][1])
            ints1_list.append(0)
            mz_merge_list.append(mz2_list[idx2])
            idx2 += 1
        else:
            ints1_list.append(ref_spec[idx1][1])
            ints2_list.append(spec2[idx2][1])
            mz_merge_list.append((mz1_list[idx1] + mz2_list[idx2]) / 2)
            idx1+= 1
            idx2 += 1

    if idx1 == len(mz1_list):
        for i in range(idx2, len(mz2_list)):
            ints2_list.append(spec2[i][1])
            ints1_list.append(0)
            mz_merge_list.append(mz2_list[i])
    elif idx2 == len(mz2_list):
        for i in range(idx1, len(mz1_list)):
            ints1_list.append(ref_spec[i][1])
            ints2_list.append(0)
            mz_merge_list.append(mz1_list[i])
    
    return mz_merge_list, ints1_list, ints2_list



def compare2spec(ref_spec, spec2):
    dist = 0
    mz_m_list, ints1_list, ints2_list = alignTwoSpec(ref_spec, spec2)
    sorted_mz = sorted(mz_m_list)
    if sorted_mz != mz_m_list:
        print("wrong")
    # print(len(mz_m_list), len(ints1_list), len(ints2_list))
    dist = cal_cosin_dis(ints1_list, ints2_list)
    return round(dist, 4)
