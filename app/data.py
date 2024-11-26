import os
import pandas as pd
from certifi import where
from dotenv import load_dotenv
from MonsterLab import Monster
from pandas import DataFrame
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
load_dotenv()

class Database:

    def __init__(self, uri: str, database_name: str, collection_name: str):
        """
        Initializes the MongoDBInterface with a connection URI and database name and Collection name.
        """
        try:
            self.client = MongoClient(uri)
            self.database = self.client[database_name]
            self.collection = self.database[collection_name]
            print("Successfully connected to MongoDB!")
        except ConnectionFailure as e:
            print(f"Could not connect to MongoDB: {e}")

    def seed(self, amount):
        """
        Seeds the database with specified amount of records
        :param amount: int
        :return:None
        """
        monster_records = []
        for _ in range(amount):
            monster = Monster()
            monster_record = {
                "name": monster.name,
                "type": monster.type,
                "level": monster.level,
                "rarity": monster.rarity,
                "damage": monster.damage,
                "health": monster.health,
                "energy": monster.energy,
                "sanity": monster.sanity,
                "timestamp": monster.timestamp
            }
            monster_records.append(monster_record)
        # Insert records into MongoDB
        result_ins = self.collection.insert_many(monster_records)
        print(f"Inserted {len(result_ins.inserted_ids)} monsters into the collection.")

    def reset(self):
        """
        Deletes all documents from the collection
        :return: None
        """
        result_reset = self.collection.delete_many({})
        print(f"Deleted {result_reset.deleted_count} document(s).")

    def count(self) -> int:
        """
         Returns the number of documents in the collection
        :return: int
        """
        result_count = self.collection.count_documents({})
        print(f"Number of Documents: {result_count}")
        return result_count

    def dataframe(self) -> DataFrame:
        """
        Returns a DataFrame containing all documents in the collection.
        :return: DataFrame
        """
        cursor = self.collection.find()
        df = pd.DataFrame(list(cursor))
        return df

    def html_table(self) -> str:
        """
        returns an HTML table representation of the DataFrame, or None if the collection is empty.
        :return: html table or None
        """
        if self.collection.count_documents({}) > 0:
            cursor = self.collection.find()
            df = pd.DataFrame(list(cursor))
            html_table = df.to_html()
            return html_table
        return 'None'


if __name__ == "__main__":
    MONGO_URI = os.getenv("DB_URL")
    DATABASE_NAME = "example_db"
    COLLECTION_NAME = "test_collection"
    db = Database(MONGO_URI, DATABASE_NAME, COLLECTION_NAME)

    # Delete all the records from the collection
    db.reset()

    # Insert the specified number of records in the collection
    db.seed(1000)

    # Count the number of documents in the collection
    count = db.count()

    # Return the documents in Data Frame format
    df_result = db.dataframe()
    print(df_result.head())

    # Get the HTML Representation of dataframe
    result = db.html_table()
    print(result)








