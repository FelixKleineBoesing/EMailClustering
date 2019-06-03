from mailcluster.ETL import ETL


if __name__=="__main__":
    etl = ETL(acc_name="felix.boesing@t-online.de",
              use_cache=True)
    etl.run_etl_pipeline()
