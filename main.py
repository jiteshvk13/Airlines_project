from src.data_ingestion import DataIngestion
from src.data_processing import DataProcessor
from src.feature_engineering import FeatureEngineer
from src.model_training import ModelTraining

from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *

logger = get_logger(__name__)

if __name__ =="__main__":
    try:
        #Data Ingestion
        ingestion = DataIngestion(raw_data_path=RAW_DATA_PATH, ingested_data_dir=INGESTED_DATA_DIR)
        ingestion.create_ingested_data_dir()
        logger.info("Ingested Dir Created Succcesfully")
        ingestion.split_data(TRAIN_DATA_PATH, TEST_DATA_PATH)

        #Data Processing
        processor = DataProcessor()
        processor.run()

        ##Feature Engineering
        feature_engineer = FeatureEngineer()
        feature_engineer.run()

        #Model Training
        model_trainer = ModelTraining(data_path=ENGINEERED_DATA_PATH , params_path=PARAMS_PATH ,  model_save_path=MODEL_SAVE_PATH)
        model_trainer.run()

    except CustomException as ce:
            logger.error(str(ce))
    
                