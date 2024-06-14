import json
import logging
import os

import pandas as pd

logger = logging.getLogger(__name__)

class AddressStoreController:
    """
    address controller
    """

    def __init__(self, json_obj=None):
        with open("secrets.json", encoding="utf-8") as f:
            secrets = json.load(f)
            self.datafile_path = secrets["DATAFILE_PATH"]
        if os.path.isfile(self.datafile_path):
            self.store_df = pd.read_feather(self.datafile_path)
        else:
            tmp_df = pd.json_normalize(json_obj)
            self.store_df = pd.DataFrame(columns=list(tmp_df))
            logger.warning("json file not found. Creating a new one.")
            self.store_df.to_feather(self.datafile_path)

    def get_all_address(self):
        """
        get method for addresses df
        """
        return self.store_df

    def insert_address(self, json_row):
        """
        convert into a dataframe and append into existing loaded dataframe and save
        """

        logger.info("shape before update: %s", str(self.store_df.shape))
        row_df = pd.json_normalize(json_row)
        # row_df = pd.DataFrame([json_row])
        self.store_df = pd.concat([self.store_df, row_df], ignore_index=True)

        logger.info("shape after update: %s", str(self.store_df.shape))
        logger.info("saving updated dataframe...")
        self.store_df.to_feather(self.datafile_path)

        return self.store_df

    def clear_database(self):
        """
        purge addresses in feather file
        """
        logger.warning("purging all addresses records: %s", str(self.store_df.shape))
        self.store_df.drop(self.store_df.index, inplace=True)

        logger.info("saving empty dataframe...")
        self.store_df.to_feather(self.datafile_path)
