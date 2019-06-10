import numpy as np
import pandas as pd
from functools import reduce


class FeatureEngineerer:

    def __init__(self):
        self.engineered_features = {}

    def engineer_feature(self, data: dict):
        self._get_number_images(data)
        self._get_length_body(data)
        self._get_length_from(data)
        self._get_number_alias(data)
        self._get_number_urls(data)
        self._get_number_words(data) 
        
    def _get_number_words(self, data: dict):
        return [len(body.split(" ")) for body in data["Body"]]

    def _get_number_images(self, data: dict):
        image_counts = [body.count(".png") + body.count(".jpeg") + body.count(".gif") for body in data["Body"]]
        self.engineered_features["ImageCounts"] = image_counts

    def _get_number_urls(self, data: dict):
        url_counts = [body.count("http://") + body.count("https://") for body in data["Body"]]
        self.engineered_features["URLCounts"] = url_counts

    def _get_number_alias(self, data: dict):
        paragraphs_counts = [body.count(r"\\n") for body in data["Body"]]
        tab_counts = [body.count(r"\\t") for body in data["Body"]]
        idk_counts = [body.count(r"\\r") for body in data["Body"]]
        self.engineered_features["ParaCounts"] = paragraphs_counts
        self.engineered_features["TabCounts"] = tab_counts
        self.engineered_features["IDKCounts"] = idk_counts

    def _get_length_body(self, data: dict):
        length_body = [len(body) for body in data["Body"]]
        self.engineered_features["LengthBody"] = length_body

    def _get_length_from(self, data: dict):
        length_from = [len(body) for body in data["From"]]
        self.engineered_features["LengthFrom"] = length_from


if __name__ == "__main__":
    fe = FeatureEngineerer()
    data = pd.read_csv("../computed_Data/e_mails_cleaned.csv")
    fe.engineer_feature(data)
