import pandas as pd
import numpy as np
import os
import json
from win32com import client
import logging
import datetime

from mailcluster.Helper import decode_escapes


class ETL:

    def __init__(self, acc_name: str = None,
                 use_cache: bool = True):
        '''
        Class responsible for extraction, transforming and loading
        :param acc_name: name of outlook account
        :param use_cache whether to use cached exctraced data or not
        '''
        self.caching = use_cache
        self.cleaned_data = None
        self.output_path_extracted = "../computed_data/e_mails_extracted.txt"
        self.output_path_loaded = "../computed_data/e_mails_cleaned.csv"
        self.acc_name = acc_name

    def run_etl_pipeline(self):
        data = None
        if not os.path.isfile(self.output_path_extracted) or not self.caching:
            self.extract_mails_from_outlook()
        if data is None:
            with open(self.output_path_extracted, "r") as f:
                data = json.load(f)
        cleaned_data = self.clean_emails(data)
        self.load_emails(cleaned_data)

    def extract_mails_from_outlook(self):
        pass

    def clean_emails(self, data: dict):
        dropped_mails = 0
        for index, mail in enumerate(data):
            print("Handling mail with index {0}".format(index))
            for key in mail.keys():
                try:
                    decoded = decode_escapes(mail[key]).encode("UTF-8")
                    mail[key] = decoded
                except:
                    dropped_mails += 1
                    del data[index]

        logging.warning("{0} mails were dropped because of unconvertible encoding!".format(dropped_mails))

        # convert cp in the right format
        # engineer some features
        df = pd.DataFrame(data)

        tos, bodies, categories, dates, froms, received_times, subjects, ccs = [], [], [], [], [], [], [], []
        for i in range(df.shape[0]):
            tos.append(df.loc[i, "To"].decode("utf-8") if type(df.loc[i, "To"]) == bytes else df.loc[i, "To"])
            bodies.append(df.loc[i, "Body"].decode("utf-8") if type(df.loc[i, "Body"]) == bytes else df.loc[i, "Body"])
            categories.append(df.loc[i, "Category"].decode("utf-8") if type(df.loc[i, "Category"]) == bytes
                            else df.loc[i, "Category"])
            dates.append(df.loc[i, "Date"].decode("utf-8") if type(df.loc[i, "Date"]) == bytes else df.loc[i, "Date"])
            froms.append(df.loc[i, "From"].decode("utf-8") if type(df.loc[i, "From"]) == bytes else df.loc[i, "From"])
            received_times.append(df.loc[i, "ReceivedTime"].decode("utf-8") if type(df.loc[i, "ReceivedTime"]) == bytes
                                  else df.loc[i, "ReceivedTime"])
            subjects.append(df.loc[i, "Subject"].decode("utf-8") if type(df.loc[i, "Subject"]) == bytes
                           else df.loc[i, "Subject"])
            ccs.append(df.loc[i, "CC"].decode("utf-8") if type(df.loc[i, "CC"]) == bytes else df.loc[i, "CC"])

        df.To = tos
        df.Body = bodies
        df.Category = categories
        df.Date = [datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S+00:00") for date in dates]
        df.From = froms
        df.ReceivedTime = [datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S+00:00") for date in received_times]
        df.Subject = subjects
        df.CC = ccs
        return df

    def load_emails(self, data: pd.DataFrame):
        logging.info("Writing cleaned data to file: {0}".format(self.output_path_loaded))
        data.to_csv(self.output_path_loaded)


if __name__ == "__main__":
    etl = ETL(acc_name="felix.boesing@t-online.de",
              use_cache=False)
    etl.run_etl_pipeline()

