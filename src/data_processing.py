import numpy as np
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
import sys
import os
import pandas as pd

logger = get_logger(__name__)

class DataProcessor:
    def __init__(self):
        self.train_path = TRAIN_DATA_PATH
        self.processed_data_path = PROCESSED_DATA_PATH

    def load_data(self):
        try:
            df = pd.read_csv(self.train_path)

            logger.info(f"Data Read Succesfully{df.shape}")
            return df
        except Exception as e:
            logger.error("Error While Loading the Data")
            raise CustomException("Error While Data Loading", sys)


    def drop_useless_column(self, df, columns):
        try:
            df = df.drop(columns= columns)
            logger.info(f"Columns dropped successfully: {df.shape}")
            return df
        except Exception as e:
            logger.error("Error While Deleting  the Columns")
            raise CustomException("Error While Deleting  the Columns", sys)

    def handle_outliers(self, df,columns):
        try:
            for column in columns:
                Q1 = df[column].quantile(0.25)
                Q3 = df[column].quantile(0.75)
                IQR = Q3 - Q1
        
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                df[column] = df[column].clip(lower=lower_bound, upper=upper_bound)
                
            logger.info(f"Outliers handled successfully: {df.shape}")
            return df
        except Exception as e:
            logger.error("Error While Handling the Outlier")
            raise CustomException("Error While Handling the Outlier", sys)

    def handle_null_values(self, df, columns):
        try:
            df[columns] = df[columns].fillna(df[columns].median())
        
            logger.info(f"Null values handled successfully: {df.shape}")
            return df

        except Exception as e:
            logger.error("Error While Handle Null Value Succesfully")
            raise CustomException("Error Handle Null Value Succesfully", sys) 

    def save_data(self, df):
        try:
            os.makedirs(PROCESSED_DIR, exist_ok=True)
            df.to_csv(self.processed_data_path, index = False)
            logger.info("Processed Data Saved Succesfully")

        except Exception as e:
            logger.error("Error While Saving Processed Data")
            raise CustomException("Error While Saving Processed Data", sys) 

    def run(self):
        try:
            logger.info("data Processing Pipeline Started")
            df = self.load_data()
            df = self.drop_useless_column(df,['MyUnknownColumn','id'])
            df = self.handle_outliers(df, ['Flight Distance','Departure Delay in Minutes','Arrival Delay in Minutes', 'Checkin service'])
            df = self.handle_null_values(df, 'Arrival Delay in Minutes')
            self.save_data(df)
            logger.info("data Processing Pipeline Completed")

        except CustomException as ce:
            logger.error(f"Error While data Processing Pipeline", {str(ce)})

        

if __name__ =="__main__":
    processor = DataProcessor()
    processor.run()

