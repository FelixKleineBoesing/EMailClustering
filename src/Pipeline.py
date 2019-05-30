from src.ETL import ETL
from src.Preprocessor import Preprocessor
from src.Models import Model


class Pipeline:

    def __init__(self, etl: ETL, preprocessors: list, model: Model):
        '''
        Pipeline class which unites all steps from etl to modelling
        :param etl:
        :param preprocessors:
        :param model:
        '''
        assert isinstance(etl, ETL)
        assert isinstance(preprocessors, list)
        assert(all([isinstance(preprocessor, Preprocessor) for preprocessor in preprocessors]))
        assert isinstance(model, Model)
        pass

    def run_pipeline(self):
        pass
