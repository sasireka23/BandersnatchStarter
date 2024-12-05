import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import datetime
import pandas as pd
from pandas import DataFrame
import os


class Machine:
    def __init__(self, df):
        self.timestamp = datetime.datetime.now().strftime("%Y%m%d %H%M")
        self.name = "Random Forest Classifier"
        target = df["Rarity"]
        features = df.drop(columns=["Rarity"])
        self.model = RandomForestClassifier(n_estimators=100)
        self.model.fit(features, target)

    def __call__(self, feature_basis):
        prediction = self.model.predict(feature_basis)
        confidence = np.max(self.model.predict_proba(feature_basis))
        return prediction, confidence

    def save(self, filepath):
        try:
            joblib.dump(self.model, filepath)
            print(f"Model saved successfully to {filepath}")
        except Exception as e:
            print(f"Error saving model: {e}")

    @staticmethod
    def open(filepath):
        model = joblib.load(filepath)
        return model

    def info(self):
        return f"Base Model:{self.name} Timestamp: {self.timestamp}"









