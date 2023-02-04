import os
import tempfile
import shutil
from tempfile import mkdtemp
import glob

from projects.data.data_structs.DataType import DataType
from projects.data.multimodal.TabularData import TabularData
from projects.utils.StorageAdapter import StorageAdapter


class DataPreparation:
    def __init__(self, path, admin_accessId=None, admin_secret=None,
                 bucket_name="ultaml-data") -> None:
        super().__init__()
        self.admin_accessId = admin_accessId
        self.admin_secret = admin_secret
        self.bucket_name = bucket_name
        self.SA = StorageAdapter(self.admin_accessId, self.admin_secret)

        self.path = path

    def download_data_from_s3(self, downloaded_temp_path=None):
        # download data from path to local temp folder
        if downloaded_temp_path is None:
            # create temp folder in temp directory irrespective of operative system windows or linux
            downloaded_temp_path = os.path.join(tempfile.gettempdir(), "data.zip")
        self.SA.download(self.bucket_name, self.path, downloaded_temp_path)
        # unzip data
        directory_to_extract_to = mkdtemp()
        shutil.unpack_archive(downloaded_temp_path, directory_to_extract_to)
        print("data is in ", directory_to_extract_to)
        # remove zip file
        os.remove(downloaded_temp_path)
        # return path to local temp folder
        return directory_to_extract_to

    @staticmethod
    def load_data(local_data_path, dataType: DataType):
        # get all files in local_data_path
        if dataType == DataType.TABULAR:
            all_files = glob.glob(f"{local_data_path}/*")
            if len(all_files) > 1:
                raise Exception(
                    'More than one file found in the directory.'
                    ' Please follow guidelines for data upload')
            file = all_files[0]
            print("file is ", file)
            # get file extension
            file_extension = os.path.splitext(file)[1]
            if file_extension not in [".csv", ".xlsx", ".txt", '.sav']:
                raise Exception(
                    'File extension not supported.'
                    ' Please follow guidelines for data upload')
            tabData = TabularData()
            tabData.load(file)
            return tabData
