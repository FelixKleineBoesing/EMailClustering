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

        data["To"] = [item.decode("utf-8") if type(item) == bytes else item for item in data["To"]]
        data["Body"] = [item.decode("utf-8") if type(item) == bytes else item for item in data["Body"]]
        data["Category"] = [item.decode("utf-8") if type(item) == bytes else item for item in data["Category"]]
        data["Date"] = [item.decode("utf-8") if type(item) == bytes else item for item in data["Date"]]
        data["Froom"] = [item.decode("utf-8") if type(item) == bytes else item for item in data["From"]]
        data["ReceivedTime"] = [item.decode("utf-8") if type(item) == bytes else item for item in data["ReceivedTime"]]
        data["subject"] = [item.decode("utf-8") if type(item) == bytes else item for item in data["Subject"]]
        data["CC"] = [item.decode("utf-8") if type(item) == bytes else item for item in data["CC"]]

        data["Date"] = [datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S+00:00") for date in data["Date"]]
        data["ReceivedTime"] = [datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S+00:00") for date in
                                data["ReceivedTime"]]
        return data

    def load_emails(self, data: dict):
        logging.info("Writing cleaned data to file: {0}".format(self.output_path_loaded))
        json.dump(data, self.output_path_loaded)


if __name__ == "__main__":
    etl = ETL(acc_name="felix.boesing@t-online.de",
              use_cache=False)
    etl.run_etl_pipeline()

