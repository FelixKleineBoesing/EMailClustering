import pandas as pd


def get_summary(data):
    data.head()




if __name__=="__main__":
    data = pd.read_csv("../computed_Data/e_mails_cleaned.csv")
    get_summary(data)