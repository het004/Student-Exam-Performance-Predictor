import os
import sys      #reason for importing this is becausse we are using exception
from src.exception import CustomException
from src.logger import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass        #this is basically used to create classs variables

@dataclass
class DataingestionConfig:
    train_data_path:str=os.path.join('artifacts','train.csv')
    test_data_path:str=os.path.join('artifacts','test.csv')
    raw_data_path:str=os.path.join('artifacts','raw.csv')

class Dataingestion:
    def __init__(self):
        self.ingestion_config=DataingestionConfig()

    def intiatedataingestion(self):
        logging.info("Entered the data ingestion method or component")
        try:
            df=pd.read_csv('notebook\data\stud.csv')
            logging.info("Read the datasets as dataframe")

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)  #used ??
            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)   #save the raw data
            logging.info("Train Test Split intiated")
            train_set,test_set=train_test_split(df,test_size=0.2,random_state=32)
            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)  #save the train data
            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)  #save the test data

            logging.info("Ingestion of data is completed")

            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
                # will return the path of train and test as it would be required for data transformation
            )
        except Exception as e:
            raise CustomException(e,sys)


if __name__=="__main__":
    obj=Dataingestion()
    obj.intiatedataingestion()