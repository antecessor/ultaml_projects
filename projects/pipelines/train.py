"""
command example : ultaml_train -key 123123123123123 -email moremohebian@gmail.cop -local_data_path /home/ultaml/data
"""
import argparse
import os

import requests


from projects.data.DataPreparation import DataPreparation
from projects.data.data_structs.Data import Data
from projects.data.data_structs.Model import Model

host = "http://localhost:5000"

# arg parser
parser = argparse.ArgumentParser(description='Train a model')
parser.add_argument('-key', '--key_id', type=str, help='key id',
                    default="hGd4RqeEiEk81\\/bGv\\/ozsjSDhJ\\/nGqd75y2tOvERnV164mDsZH+BwfOiWMWg7vTQtIP\\/KX0TH5hWtrB7mND6E5uH16eRViMUrwxvMWWKLuR5FJArz6o+t9p+MPx0r\\/oV6cbdKogPjMeafIbTC1XYG3hjaBCuBhDguTxv+MioVYfKZvGttkQ+ShpJx4tFnfj0Vk5R4JA1YdX+Pp0Z1EcsjZy0byL1JrShFHP3TzCzp4o=")
parser.add_argument('-email', '--email', type=str, help='email',
                    default="moremohebian@gmail.com")
parser.add_argument('-local_data_path', '--local_data_path', type=str, help='local data path', required=False)

args = parser.parse_args()
# if local_data_path exist
if "local_data_path" in args and args.local_data_path is not None:
    local_data_path = args.local_data_path
else:
    local_data_path = None

# send a get request to /ml/get_data_model_info
# pass key and email
response = requests.get(host + "/ml/get_data_model_info", params={"training_key": args.key_id, "email": args.email})
if response.status_code == 200:
    data = Data.from_dict_all_string(response.json()['data'])
    model = Model.from_dict_all_string(response.json()['model'])
    access_key_id = response.json()['access_key_id']
    secret_access_key = response.json()['secret_access_key']
    training_config = response.json()['training_config']
else:
    print("Error in getting data and model! Check your email and key!")
    raise Exception("Error in getting data and model! Check your email and key!")


def getDataPath(data, access_key_id, secret_access_key, localDataPath=None):
    if not (data.path == "local"):
        dataPrep = DataPreparation(data.path, access_key_id, admin_secret=secret_access_key)
        downloaded_temp_path = dataPrep.download_data_from_s3()
    else:
        downloaded_temp_path = localDataPath
    return downloaded_temp_path


if model.downstream_task != data.downstream_task:
    raise Exception("Model and data are not compatible")

dataPath = getDataPath(data, access_key_id, secret_access_key, local_data_path)
if model.code_path.__contains__("xgboost"):
    from projects.models.tabular.xgboost.TrainingConfig import TrainingConfig

    training_config = TrainingConfig(**model.training_config)
    training_config.data_path = dataPath
    training_args = training_config.to_arguments()
    # create command
    if model.code_path.__contains__("project"):
        # get current path parent
        current_path = os.path.dirname(os.path.abspath(__file__))
        parent_path = os.path.dirname(os.path.dirname(current_path))
        command = "python " + parent_path + "/" + model.code_path
        command = command + " " + training_args

        print(command)
        os.system(command)

    else:
        # Todo: will be implemented to get third party repo
        pass
