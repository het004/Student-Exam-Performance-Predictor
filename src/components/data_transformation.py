import sys
import os
import pandas as pd
import numpy as np
from dataclasses import dataclass
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler

from src.exception import CustomException
from src.logger import logging

from src.utils import save_object
#This will give me any inputs path that would be reuired in data transformation
@dataclass
class Datatransformation_config:
    preprocessor_obj_file_path=os.path.join('artifacts','preprocessor.pkl')


class Datatransformation:
    '''
    This Functionn is responsible for data transformation
    '''
    def __init__(self):
        self.data_transformation_config=Datatransformation_config()
    #this will be resposnsible for creating all the pickle files which will be responsible for data transformation
    def get_data_transformer_object(self):
        try:
            numerical_coloumns=['reading_score', 'writing_score']
            categorical_coloumns=[
            'gender',
            'race_ethnicity',
            'parental_level_of_education',
            'lunch',
            'test_preparation_course']
            #we will create pipeline to 1)handle missing values by median 2)doing standard scalar
            num_pipeline=Pipeline(
            steps=[
                ("imputer",SimpleImputer(strategy='median')),
                ("scalar",StandardScaler())
            ])
            cat_pipeline=Pipeline(
            steps=[
                ("imputer",SimpleImputer(strategy="most_frequent")),
                ("one_hot_encoder",OneHotEncoder()),
                ("scaler",StandardScaler(with_mean=False))
            ]
        )
            logging.info("Numerical Columns scaling completed")
            logging.info("Categorical Columns encoding and scaling completed")
        #Now we need to combine two pipeline
            preprocessor=ColumnTransformer(
                [
                ("num_pipeline",num_pipeline,numerical_coloumns),
                ("cat_pipeline",cat_pipeline,categorical_coloumns)
                ]
                )
            return preprocessor      
        except Exception as e:
            raise CustomException(e, sys)
        
    def intiate_data_transformation(self,train_path,test_path):
        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)
            logging.info("Read train and test data")

            logging.info("obtaining preprocessing object")
            preprocessing_obj=self.get_data_transformer_object()

            target_coloumn_name="math_score"
            numerical_coloumns=['reading_score', 'writing_score']

            categorical_coloumns=[
            'gender',
            'race_ethnicity',
            'parental_level_of_education',
            'lunch',
            'test_preparation_course'
            ]

            input_train_feature=train_df.drop(columns=target_coloumn_name,axis=1)
            target_train_feature=train_df[target_coloumn_name] 

            input_test_feature=test_df.drop(columns=target_coloumn_name,axis=1)
            target_test_feature=test_df[target_coloumn_name]

            logging.info("Applying preproccsing object on training and testing dataset")
            input_train_feature_arr=preprocessing_obj.fit_transform(input_train_feature)
            input_test_feature_arr=preprocessing_obj.transform(input_test_feature)     #difference between fit_transform and transform

            train_arr=np.c_[                                            #what is c_?
                input_train_feature_arr,np.array(target_train_feature)
            ]

            test_arr=np.c_[                                            #what is c_?
                input_test_feature_arr,np.array(target_test_feature)
            ]
            logging.info("Saved Preprocessing object")

            save_object(

                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj

            )

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )
        except Exception as e:
            raise CustomException(e,sys)


