import pandas as pd
import numpy as np
import os
import json
from win32com import client
import logging

from src.Helper import decode_escapes

class ETL:

    def __init__(self, acc_name: str = None,
                 use_cache: bool = True):
        '''
        Class responsible for extraction, transforming and loading
        :param acc_name: name of outlook account
        :param use_cache whether to use cached exctraced data or not
        '''
        self.caching = use_cache
        self.messages = []
        self.cleaned_data = None
        self.output_path_extracted = "../computed_data/e_mails_extracted.txt"
        self.output_path_loaded = "../computed_data/e_mails_cleaned.csv"

    def run_etl_pipeline(self):
        data = None
        if not os.path.isfile(self.output_path_extracted) or not self.caching:
            data = self.extract_mails_from_outlook()
        if data is None:
            with open(self.output_path_extracted, "r") as f:
                data = json.load(f)
        cleaned_data = self.clean_emails(data)
        self.load_emails(cleaned_data)


    def extract_mails_from_outlook(self, acc_name: str = None):
        # init outlook conn
        outlook_instance = client.Dispatch("Outlook.Application").GetNamespace("MAPI")

        inbox = outlook_instance.Folders(acc_name)
        folders = inbox.folders

        for folder in folders:
            if str(folder) == "Posteingang":
                messages = folder.Items
                i = 0
                for message in messages:
                    if i % 50 == 0:
                        print(i)
                    i += 1
                    msg = {"To": str(message.To),
                           "From": str(message.Sender),
                           "Body": str(message.Body),
                           "CC": str(message.CC),
                           "Subject": str(message.Subject),
                           "Date": str(message.SentOn),
                           "Category": str(message.Categories),
                           "ReceivedTime": str(message.ReceivedTime)}
                    self.messages += [msg]
        if len(self.messages) > 0:
            file = open(self.output_path_extracted, "w")
            file.write(json.dumps(self.messages))
            file.close()


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
        return df

    def load_emails(self, data: pd.DataFrame):
        logging.info("Writing cleaned data to file: {0}".format(self.output_path_loaded))
        data.to_csv(self.output_path_loaded)

if __name__=="__main__":
    etl = ETL(acc_name="felix.boesing@t-online.de",
              use_cache =True)
    etl.run_etl_pipeline()

