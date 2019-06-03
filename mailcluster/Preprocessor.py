import abc
import pandas as pd


class Preprocessor(abc.ABC):

    @abc.abstractmethod
    def __init__(self):
        '''
        Preprocessor class that applies preprcoessing on a given dataset
        '''
        pass

    def preprocess(self, raw_data: pd.DataFrame):
        '''
        in case there must be applied general preprocessing for all preprocessors
        :param raw_data: cleaned data as dataframe
        :return:
        '''
        assert type(raw_data) == pd.DataFrame
        preprocessed_data = self._preprocess_core()
        return preprocessed_data

    @abc.abstractmethod
    def _preprocess_core(self):
        pass
