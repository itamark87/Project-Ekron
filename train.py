from pprint import pprint
import numpy as np
import pandas as pd
from sklearn import metrics
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm

from sklearn.pipeline import Pipeline

from spacy.lang.en import English
import re
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from time import time
import joblib
from utils import predictors, get_tfidf_vector

# parameters for SVM:
parameters = {
    'classifier__C': [1, 10, 100, 1000],
    'classifier__gamma': [0.001, 0.0001]
}

if __name__ == '__main__':
    pd.set_option('display.max_rows', 500)  # To see all rows
    pd.set_option('display.max_columns', 500)  # To see all columns
    pd.set_option('display.width', 1000)

    df_facebook = pd.read_csv("faceebook_data_recent.csv", sep=",")
    print(df_facebook.head())
    print(df_facebook.shape)

    # View data information
    # print(df_facebook.info())

    print(df_facebook.label.value_counts())

    # Load English tokenizer, tagger, parser, Named entity recognition (NER) and word vectors
    parser = English()

    # removing emojies:
    df_facebook['text'] = df_facebook['text'].apply(lambda text: re.sub('\\<.*?\>', ' ', text))
    df_facebook['text'] = df_facebook['text'].apply(lambda x: x.strip())
    df_facebook = df_facebook.loc[df_facebook['text'] != '', :]
    X = df_facebook['text']  # the features we want to analyze
    ylabels = df_facebook['label']  # the labels, or answers, we want to test against

    X_train, X_test, y_train, y_test = train_test_split(X, ylabels, test_size=0.2)

    rows_test = list(set(X.index) - set(X_train.index))
    df_test_indices = pd.DataFrame(data=rows_test, columns=["index_test"])
    df_test_indices.to_csv('test_indices.csv', index = False)

    print("y_train: ", y_train.value_counts())
    print("y_test: ", y_test.value_counts())

    list_of_model_types = ['svm', 'logistic_regression', 'random_forest']

    # for model_name in list_of_model_types:
    # classifier = LogisticRegression()
    classifier = svm.SVC(kernel='linear')  # Linear Kernel
    # classifier = RandomForestClassifier(n_estimators=100)

    # Create pipeline using TFIDF
    pipe = Pipeline([("cleaner", predictors()),
                     ('vectorizer', get_tfidf_vector()),
                     ('classifier', classifier)])

    grid_search = GridSearchCV(pipe, parameters, n_jobs=-1, verbose=1)

    print("Performing grid search...")
    print("pipeline:", [name for name, _ in pipe.steps])
    print("parameters:")
    pprint(parameters)
    t0 = time()
    grid_search.fit(X_train, y_train)
    print("Done in %0.3f Seconds" % (time() - t0))

    print("Best score: %0.3f" % grid_search.best_score_)
    print("Best parameters set:")
    best_parameters = grid_search.best_estimator_.get_params()
    for param_name in sorted(parameters.keys()):
        print("\t%s: %r" % (param_name, best_parameters[param_name]))

    # model generation
    print("Generating model")
    X_train = list(X_train)
    y_train = np.array(y_train)

    print("Model prediction")
    predicted = grid_search.predict(X_test)

    elements_count = np.bincount(predicted)
    elements = np.nonzero(elements_count)[0]
    print(dict(zip(elements, elements_count[elements])))

    print("Confusion matrix: \n", metrics.confusion_matrix(y_test, predicted))

    joblib.dump(grid_search, 'svm.pkl')

    # Model Accuracy
    print("SVM Accuracy:", metrics.accuracy_score(y_test, predicted))
    print("SVM Precision:", metrics.precision_score(y_test, predicted))
    print("SVM Recall:", metrics.recall_score(y_test, predicted))
    # print(predicted)
    # for post in X_test:
    #    print(post)

    #pipe.transform(X_train, y_train)  # here x is your text data, and y is going to be your target


    # Score board:
    # 1) Logistic Regression:
    #    Logistic Regression Accuracy: 0.9644970414201184/0.9475524475524476
    #    Logistic Regression Precision: 1.0/0.75
    #    Logistic Regression Recall: 0.14285714285714285/0.09375
    # 2) SVM :
    # SVM accuracy: 0.9615384615384616/0.972027972027972
    # SVM Precision: 0.7777777777777778/0.9230769230769231
    # SVM Recall: 0.3888888888888889/0.4444444444444444
    # 3) Random Forest :
    # Random Forest accuracy: 0.9349112426035503/0.9702797202797203
    # Random Forest Precision: 1.0/1.0
    # Random Forest Recall: 0.12/0.2608695652173913
    # Using gridSearch:
    # SVM accuracy: 0.9585798816568047/0.9825174825174825
    # SVM Precision: 0.8181818181818182/0.8888888888888888
    # SVM Recall: 0.42857142857142855/0.6666666666666666
    # Logistic Regression  accuracy: 0.9497041420118343/0.9440559440559441
    # Logistic Regression  Precision: 0.0/0.75
    # Logistic Regression  Recall: 0.0/0.08823529411764706
    # Random Forest accuracy: 0.9526627218934911/0.951048951048951
    # Random Forest Precision:  1.0
    # Random Forest Recall: 0.058823529411764705/0.06666666666666667

    #for i in range(10):
    #    print(predicted[i])
    #print(X_test)
