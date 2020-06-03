import subprocess
import pandas as pd
from sklearn.model_selection import train_test_split
from LASExplanation.SHAP import *
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MinMaxScaler
import pkg_resources


def main():
    file = pkg_resources.resource_filename('LASExplanation', 'camel-1.2.csv')
    #file = os.path.join(os.getcwd(), 'camel-1.2.csv')
    df = pd.read_csv(file)
    # demo using a software defect prediction dataset
    for i in range(0, df.shape[0]):
        if df.iloc[i, -1] > 0:
            df.iloc[i, -1] = 1
        else:
            df.iloc[i, -1] = 0
    X=df.iloc[:,:-1]
    y=df.iloc[:,-1]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.05)
    sc = MinMaxScaler()
    X_train = pd.DataFrame(sc.fit_transform(X_train), columns=X_train.columns).copy()
    X_test = pd.DataFrame(sc.fit_transform(X_test), columns=X_train.columns).copy()
    clf= RandomForestClassifier()
    # print(subprocess.Popen("echo pkw", shell=True, stdout=subprocess.PIPE).stdout.read())
    # ps = subprocess.Popen("type lime_fi.txt", shell=True,stdout=subprocess.PIPE)
    # print('Text copied.')
    # subprocess.Popen("sk.py --text 30 --latex True --higher True", shell=True,stdin=ps.stdout)
    # print('sk.py called')
    clf.fit(X_train,y_train)
    shap = SHAP(clf=clf,X_test=X_test,X_train=X_train)
    # leave sensitive as none if the data has no fairness concerns
    for i in range(len(X_train.columns)):
        print('Index',i,':',X_train.columns[i])
    shap_values = shap.explain()
    shap.summary_plot()
    return True


if __name__ == "__main__":
    main()
