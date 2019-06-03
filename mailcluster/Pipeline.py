from mailcluster.ETL import ETL
from mailcluster.Preprocessor import Preprocessor
from mailcluster.Models import Model
from mailcluster.FeatureEngineerer import FeatureEngineerer


class Pipeline:

    def __init__(self, etl: ETL, feature_engineerer: FeatureEngineerer, preprocessors: list, model: Model):
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
