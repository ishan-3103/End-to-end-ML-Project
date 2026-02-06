##### IN THIS WE ARE HANDELLING THE CATEGORICAL AND NUMERICAL VALUES 

import sys
import pandas as pd
import os
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler

from src.exception import CustomException
from src.logger  import logging

from src.utils import save_object


class DataTransformationConfig:
    preprocessor_obj_file_path=os.path.join("artifacts","preprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()

    def get_data_transformer_object(self):
        try:
            numerical_columns=["reading score","writing score"]
            categorical_columns=["gender","race/ethnicity","parental level of education","lunch","test preparation course"]
            
            numpipeline=Pipeline(                   #### FOR NUMERICAL COLUMNS
                steps=[
                    ("imputer",SimpleImputer(strategy='median')),      ## handelling the missing values
                    ("scalar",StandardScaler())     ## standard scalling
                    ]
                )
            
            catpipeline=Pipeline(           #### FOR CATEGORICAL COLUMNS
                steps=[
                    ("imputer",SimpleImputer(strategy='most_frequent')),
                    ("one_hot_encoder",OneHotEncoder()),
                    ("scalar",StandardScaler(with_mean=False))
                    ]
            )
            logging.info("numerical column standard scalling completed")
            logging.info("categorical column encoding completed")

            preprocessor=ColumnTransformer(transformers=[
                ("num",numpipeline,numerical_columns),
                ("cat",catpipeline,categorical_columns)
            ])

            return preprocessor
        
        except Exception as e:
            raise CustomException(e,sys)
       
    def initiate_data_transform(self,train_path,test_path):

        try:
            train_df=pd.read_csv("artifacts\\train.csv")
            test_df=pd.read_csv("artifacts\\test.csv")

            logging.info("read train and test data")
            logging.info("obtaining preprocessing object")

            preprocessing_obj=self.get_data_transformer_object()

            target_column_name="math score"

            input_feature_train_df=train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df=train_df[target_column_name]

            input_feature_test_df=test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df=test_df[target_column_name]
            logging.info("applying preprocessing on training and testing dataframe")

            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)
            
            train_arr=np.c_[
                input_feature_train_arr, np.array(input_feature_train_df)
            ]
            test_arr=np.c_[
                input_feature_test_arr, np.array(input_feature_test_df)
            ]

            logging.info("saving preprocessing obj")

            save_object(                ### BASICALLY WE ARE SAVING OUR OBJECT
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
        