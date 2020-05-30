import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import accuracy_score

#Upload a data set that contains numerical data.
#dataset = pd.read_csv("C:/Users/Istiak/Desktop/Research/testdata.csv")

#Print the uploaded data set.
#dataset.head()

#Define the independent and dependant variables where x is the independent variable and y is the dependant variable.
#y always depend on x. class_label is the last column of the data set that contains class labels.

#x = dataset.drop('class_label', axis=1)
#y = dataset['class_label']

#Define the Classifiers function. x and y are the parameters of this function.
#The Classifiers function splits the data set into training and testing data sets.
#30% of randomly selected data from the uploaded data set constructs the testing data set and the rest of them construct the training data set.
#The Classifiers function implements a decision tree classifier algorithm for classifying data set and prediction based on classified data.
#This function returns the predicted outcomes and accuracy.

def Classifiers(x, y):
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.30)
    classifier = DecisionTreeClassifier()
    classifier.fit(X_train, y_train)
    y_pred_class = classifier.predict(X_test)
    accuracy_class = accuracy_score(y_test, y_pred_class)
    print('Outcomes of Classifiers model: ', y_pred_class)
    return y_pred_class, accuracy_class

#Define the Regressors function. x and y are the parameters of the function.
#The Regressors function splits the data set into training and testing data sets.
#30% of randomly selected data from the uploaded data set constructs the testing data set and the rest of them construct the training data set.
#The Regressors function implements a decision tree regressor algorithm for classifying data set and prediction based on classified data.
#This function returns the predicted outcomes and accuracy.

def Regressors(x,y):
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.30, random_state=20)
    regressor = DecisionTreeRegressor()
    regressor.fit(X_train, y_train)
    y_pred_reg = regressor.predict(X_test)
    accuracy_reg = accuracy_score(y_test, y_pred_reg, normalize=True)
    y_pred_reg = y_pred_reg.astype(int)
    print('Outcomes of Regressors model: ',y_pred_reg)
    return y_pred_reg, accuracy_reg

#Call the two functions namely Classifiers and Regressors.
#Instantiate the two functions in two different variables such as classifier and regressor.

#classifier = Classifiers(x,y)
#regressor = Regressors(x,y)

#Define the Argumentation with two parameters classifier and regressor.
#The Argumentation function produces the final outcomes.
#It follows a probabilistic argumentation approach.
#The outcomes of Classifiers and Regressors function attack each other based on probability (Accuracy).
#Outcomes with high probability attack the outcomes that hold less probability.
#If the both functions contains similar values in similar index position the will not attack.
#The Argumentation function produces the accepted outcomes set, similar values set, and similar index position set.

def Argumentation(classifier, regressor):
    c1 = classifier[0]
    c2 = classifier[1]
    r1 = regressor[0]
    r2 = regressor[1]

    comp = (c1 == r1)
    ln = c1.size
    lnr = r1.size
    arg_val = []
    att_pos = []
    pos_val = []

    for cmp in comp:
        if cmp == True:
            print('')
        else:
            if c2 > r2:
                for i in range(0, ln, 1):
                    if c1[i] != r1[i]:
                        print(c1[i], 'Attack-->', r1[i])
                        if c2 > 0.5:
                            print('Accepted Argument: ', c1[i])
                            arg_val.insert(i, c1[i])

                        elif c2 < 0.5:
                            print('Unaccepted Argument: ', c1[i])
                            arg_val.insert(i, c1[i])
                        elif c2 == 0.5:
                            print('Undefined Argument: ', c1[i])
                            arg_val.insert(i, c1[i])
                    else:
                        print('No Attack')
                        att_pos.insert(i, i)
                        pos_val.insert(i, c1[i])

                break

            elif r2 > c2:
                for i in range(0, ln, 1):
                    if r1[i] != c1[i]:
                        print(r1[i], 'Attack-->', c1[i])
                        if c2 > 0.5:
                            print('Accepted Argument: ', r1[i])
                            arg_val.insert(i, r1[i])
                        elif c2 < 0.5:
                            print('Unaccepted Argument: ', r1[i])
                            arg_val.insert(i, r1[i])
                        elif c2 == 0.5:
                            print('Undefined Argument: ', r1[i])
                            arg_val.insert(i, r1[i])
                    else:
                        print('No Attack')
                        att_pos.insert(i, i)
                        pos_val.insert(i, r1[i])
                break

            elif c2 == r2:
                for i in range(0, ln, 1):
                    if c1[i] != r1[i]:
                        print(c1[i], 'Attack-->', r1[i])
                        if c2 > 0.5:
                            print('Accepted Argument: ', c1[i])
                            arg_val.insert(i, c1[i])
                        elif c2 < 0.5:
                            print('Unaccepted Argument: ', c1[i])
                            arg_val.insert(i, c1[i])
                        elif c2 == 0.5:
                            print('Undefined Argument: ', c1[i])
                            arg_val.insert(i, c1[i])
                    else:
                        print('No Attack')
                        att_pos.insert(i, i)
                        pos_val.insert(i, c1[i])
                break

    same_val = np.array(pos_val)
    print('Similar Values : ', same_val)
    pos_index = np.array(att_pos)
    print('Similar Positions : ', pos_index)
    arg_paf = np.array(arg_val)
    print('Accepted outcomes of PAF: ', arg_paf)

    return same_val

#Call the Argumentation function with the required parameters e.g.classifier, regressor.
#Instantiate the function in a variable e.g. argument.

#argument = Argumentation(classifier, regressor)

#Define the PlotGraph function with three parameters such as classifier, regressor, and argument.
#PlotGraph function represents the graphical presentation of four graphs.
#It presents the graphical representation of the outcomes of Classifications (class), Regressors (reg), and Argumentation (arg) functions.
#It also shows the graphical representation of Classifications (class), Regressors (reg) functions jointly.

def PlotGraph(classifier, regressor, argument):
    print('----Graphical View----')
    c1 = classifier[0]
    r1 = regressor[0]

    plt.rcParams['figure.figsize'] = (10, 4)

    plt.figure(1)
    plt.plot(c1, "b.", label='class')
    plt.legend(loc='best')
    plt.xlabel('Index Number')
    plt.ylabel('Class Label')

    plt.figure(2)
    plt.plot(r1, "r.", label='reg')
    plt.legend(loc='best')
    plt.xlabel('Index Number')
    plt.ylabel('Class Label')

    plt.figure(3)
    plt.plot(c1, "r.", label='class')
    plt.plot(r1, "c.", label='reg')
    plt.legend(loc='best')
    plt.xlabel('Index Number')
    plt.ylabel('Class Label')

    plt.figure(4)
    plt.plot(argument, "m.", label='arg')
    plt.legend(loc='best')
    plt.xlabel('Index Number')
    plt.ylabel('Class Label')

    return

#Call the function PlotGraph with the required parameters.

#PlotGraph(classifier, regressor, argument)