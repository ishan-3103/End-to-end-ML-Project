import os
import sys
import dill

from src.logger import logging

import numpy as np
import pandas as pd

from src.exception import CustomException

# def save_object(file_path,obj):
#     try:
#         dir_path=os.path.dirname(file_path)

#         os.makedirs(dir_path,exist_ok=True)

#         with open(file_path, "wb") as file_obj:
#             dill.dump(obj,file_obj)

#         # logging.info("object saved succcessfully")
#     except Exception as e:
#         raise CustomException(e,sys)

def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)

        logging.info("Object saved successfully")

    except Exception as e:
        raise CustomException(e, sys)

from sklearn.metrics import r2_score

def evaluate_model(X_train, Y_train, X_test, Y_test, models, params):
    try:
        report={}

        for i in range(len(list(models))):
            model=list(models.values())[i]
            model.fit(X_train,Y_train)

            Y_train_pred=model.predict(X_train)
            Y_test_pred=model.predict(X_test)

            test_model_score=r2_score(Y_test,Y_test_pred)
            train_model_score=r2_score(Y_train,Y_train_pred)

            report[list(models.keys())[i]] = test_model_score

        return report

    except Exception as e:
        raise CustomException(e,sys)
