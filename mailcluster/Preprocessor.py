import abc
import pandas as pd


class Preprocessor(abc.ABC):

    @abc.abstractmethod
    def __init__(self):
        '''
        Preprocessor class that applies preprcoessing on a given dataset
        '''
        pass

    def preprocess(self, body: list):
        '''
        in case there must be applied general preprocessing for all preprocessors
        :param raw_data: cleaned data as dataframe
        :return:
        '''
        assert isinstance(body, list)
        preprocessed_data = self._preprocess_core(body)
        return preprocessed_data

    @abc.abstractmethod
    def _preprocess_core(self, data: list):
        pass


class Cleaner(Preprocessor):
    
    def __init__(self):
        super().__init__()

    def _preprocess_core(self, data: list):
        body = [mail.split(" ") for mail in data]
        return body
