import unittest
from mailcluster.Pipeline import Pipeline


class PipelineTester(unittest.TestCase):

    def test_pipeline(self):
        pipeline = Pipeline()
        pipeline.run_pipeline()
