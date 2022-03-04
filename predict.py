import joblib
import pandas as pd
import train


def predict(text):
    my_model = joblib.load('svm.pkl')
    res = my_model.predict([text])
    return res[0]


if __name__ == '__main__':
    print(predict("i lost my dog"))

