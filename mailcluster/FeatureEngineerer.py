import numpy as np
import pandas as pd


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
        words = data.Body.str.split(" ")
        # TODO throw out links and special vharacters

    def _get_number_images(self, data: dict):
        image_counts = data["Body"].str.count(".png")
        image_counts + data["Body"].str.count(".jpeg")
        image_counts + data["Body"].str.count(".gif")
        self.engineered_features["ImageCounts"] = image_counts

    def _get_number_urls(self, data: dict):
        url_counts = data["Body"].str.count("http://")
        url_counts + data["Body"].str.count("https://")
        self.engineered_features["URLCounts"] = url_counts

    def _get_number_alias(self, data: dict):
        paragraphs_counts = data["Body"].str.count(r"\\n")
        tab_counts = data["Body"].str.count(r"\\t")
        idk_counts = data["Body"].str.count(r"\\")
        self.engineered_features["ParaCounts"] = paragraphs_counts
        self.engineered_features["TabCounts"] = tab_counts
        self.engineered_features["IDKCounts"] = idk_counts

    def _get_length_body(self, data: dict):
        length_body = data["Body"].str.len()
        self.engineered_features["LengthBody"] = length_body

    def _get_length_from(self, data: dict):
        length_body = data["From"].str.len()
        self.engineered_features["LengthFrom"] = length_body


if __name__ == "__main__":
    fe = FeatureEngineerer()
    data = pd.read_csv("../computed_Data/e_mails_cleaned.csv")
    fe.engineer_feature(data)
