import os
import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
import sys

logger = get_logger(__name__)

class DataIngestion:
    def __init__(self, raw_data_path, ingested_data_dir):
        self.raw_data_path = raw_data_path
        self.ingested_data_dir = ingested_data_dir
        logger.info("Data Ingestion Started")

    def create_ingested_data_dir(self):
        try:
            os.makedirs(self.ingested_data_dir, exist_ok=True) 
            logger.info("Directory for Ingestion Created")
        except Exception as e:
            raise CustomException("error while creating directory", sys)

    def split_data(self,train_path, test_path, test_size=0.2):
        try:
            data = pd.read_csv(self.raw_data_path)
            logger.info("Data Loaded Succcesfully")

            # X = data.iloc[:, :-1]
            # y = data.iloc[:, -1]
            train_data, test_data = train_test_split(data, test_size=test_size)
            logger.info("Data Splitted Succcesfully")

            train_data.to_csv(train_path, index = False)
            test_data.to_csv(test_path,index =False)
            logger.info("Data Saved Succcesfully")

        except Exception as e:
            raise CustomException("Error While Splitting the Data", sys)

if __name__ =="__main__":
    try:
        ingestion = DataIngestion(raw_data_path=RAW_DATA_PATH, ingested_data_dir=INGESTED_DATA_DIR)
        ingestion.create_ingested_data_dir()
        logger.info("Ingested Dir Created Succcesfully")
        ingestion.split_data(TRAIN_DATA_PATH, TEST_DATA_PATH)
    except CustomException as ce:
        logger.error(str(ce))

            