import os
import sys
import pandas as pd
from src.exception import CustomException
from src.logger import logging

from sklearn.model_selection import train_test_split
from dataclasses import dataclass   ## used to create class varaibles 

@dataclass
class DataIngestionConfig:
    train_data_path: str=os.path.join("artifacts","train.csv")  ### : str is just for type hinting, it is almost same as str(os.path.join....)
    test_data_path: str=os.path.join("artifacts","test.csv")
    raw_data_path: str=os.path.join("artifacts","raw.csv")

class dataingestion:
    def __init__(self):
        self.ingestion_config=DataIngestionConfig()
    def initiate_data_ingestion(self):
        logging.info("enter the data ingestion method or component")
        try:
            # df=pd.read_csv("C:\\Users\\ASUS\\OneDrive\\Desktop\\MlProject2\\notebook\\1 . EDA STUDENT PERFORMANCE .ipynb")
            df=pd.read_csv("notebook\\data\\StudentsPerformance.csv")
            ### WE CAN CHANGE THE DATA SOURCE TO ANY FILE TYPE LIKE EXCEL,MONGO DB ,API ETC
            logging.info("read the dataset ass dataframe")

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True) 
            
            logging.info("train test split initiated")
            train_set,test_set=train_test_split(df,test_size=0.2,random_state=42)
            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)
            logging.info("data ingestion compleated")

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )

        except Exception as e:
            raise CustomException(e,sys)
        
if __name__=="__main__":
    obj=dataingestion()
    obj.initiate_data_ingestion()