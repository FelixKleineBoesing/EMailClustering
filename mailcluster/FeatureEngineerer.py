import numpy as np
import pandas as pd


class FeatureEngineerer:

    def __init__(self):
        self.engineered_features = {}

    def engineer_feature(self, data: pd.DataFrame):
        self._parse_suffixe_from_mail(data)

    def _parse_suffixe_from_mail(self, data: pd.DataFrame):
        suffix = []








if __name__ == "__main__":
    fe = FeatureEngineerer()
    data = pd.read_csv("../computed_Data/e_mails_cleaned.csv")
    fe.engineer_feature(data)