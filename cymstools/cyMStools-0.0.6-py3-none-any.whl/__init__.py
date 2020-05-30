info='tools for mass spectra data analysis'
print("Successfully import cyMStools")
from .plink2_summary import summary_plink2_report
from .cal_similarity_of2spec import compare2spec


###############通用功能####################
# 读取mgf
def readMGF(mgf_path, scanSet="ALL"):
    print("Reading mgf file", end = "  ")
    print("the mgf path is %s" % mgf_path)
    f = open(mgf_path).readlines()
    scanInfoDic = {}
    i = 0
    while i < len(f):
        if f[i].strip() != "BEGIN IONS":
            i += 1
        else:
            scanTitle = f[i+1].split("=")[1].strip()
            # print(i)
            if scanSet == "ALL":
                isInset = True
            else:
                isInset = scanTitle in scanSet
            
            if isInset:
                scanNum = int(scanTitle.split(".")[1])
                charge = int(f[i+2].split("=")[1][:-2])
                mzPre = float(f[i+4].split("=")[-1].strip())
                specInfo = []
                p = i + 5
                while p < len(f):
                    if f[p].strip() == "END IONS":
                        break
                    else:
                        lineList = f[p].split(" ")
                        mz = float(lineList[0])
                        ints = float(lineList[1].strip())
                        specInfo.append([mz, ints])
                        p += 1
                scanInfoDic[scanNum] = [mzPre, charge, specInfo]
            else:
                p = i + 5
                while p < len(f):
                    if f[p].strip() == "END IONS":
                        break
                    else:
                        p += 1
        i = p + 1
    return scanInfoDic