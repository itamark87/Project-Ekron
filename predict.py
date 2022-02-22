import joblib
import pandas as pd
import train


def predict(text):
    my_model = joblib.load('svm.pkl')
    # test_indices = pd.read_csv('test_indices.csv')
    # data = pd.read_csv('faceebook_data_recent.csv')
    # test_data = data.loc[test_indices["index_test"].values, "text"]
    res = my_model.predict([text])
    return res[0]


if __name__ == '__main__':
    print(predict("i lost my dog"))

