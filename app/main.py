import datetime
from base64 import b64decode
import os

import random

import numpy as np
import pandas as pd
from MonsterLab import Monster
from flask import Flask, render_template, request
from pandas import DataFrame

from app.data import Database
from app.graph import chart
from app.machine import Machine

MONGO_URI = os.getenv("DB_URL")
DATABASE_NAME = "example_db"
COLLECTION_NAME = "test_collection"
SPRINT = 3
APP = Flask(__name__)


@APP.route("/")
def home():
    return render_template(
        "home.html",
        sprint=f"Sprint {SPRINT}",
        monster=Monster().to_dict(),
        password=b64decode(b"VGFuZ2VyaW5lIERyZWFt"),
    )


@APP.route("/data")
def data():
    if SPRINT < 1:
        return render_template("data.html")

    db = Database(MONGO_URI, DATABASE_NAME, COLLECTION_NAME)
    return render_template(
        "data.html",
        count=db.count(),
        table=db.html_table(),
    )


@APP.route("/view", methods=["GET", "POST"])
def view():
    if SPRINT < 2:
        return render_template("view.html")
    db = Database(MONGO_URI, DATABASE_NAME, COLLECTION_NAME)
    options = ["Level", "Health", "Energy", "Sanity", "Rarity"]
    x_axis = request.values.get("x_axis") or options[1]
    y_axis = request.values.get("y_axis") or options[2]
    target = request.values.get("target") or options[4]
    graph = chart(
        df=db.dataframe(),
        x=x_axis,
        y=y_axis,
        target=target,
    ).to_json()
    return render_template(
        "view.html",
        options=options,
        x_axis=x_axis,
        y_axis=y_axis,
        target=target,
        count=db.count(),
        graph=graph,
    )


@APP.route("/model", methods=["GET", "POST"])
def model():
    if SPRINT < 3:
        return render_template("model.html")
    db = Database(MONGO_URI, DATABASE_NAME, COLLECTION_NAME)
    options = ["Level", "Health", "Energy", "Sanity", "Rarity"]
    filepath = os.path.join("app", "model.joblib")
    if not os.path.exists(filepath):
        df = db.dataframe()
        machine = Machine(df[options])
        machine.save(filepath)
        machine = Machine.open(filepath)
    else:
        machine = Machine.open(filepath)
    stats = [round(random.uniform(1, 250), 2) for _ in range(3)]
    level = request.values.get("level", type=int) or random.randint(1, 20)
    health = request.values.get("health", type=float) or stats.pop()
    energy = request.values.get("energy", type=float) or stats.pop()
    sanity = request.values.get("sanity", type=float) or stats.pop()
    data_frame = DataFrame([dict(zip(options, (level, health, energy, sanity)))])
    prediction = machine.predict(data_frame)
    confidence = np.max(machine.predict_proba(data_frame))
    model_name = type(machine).__name__
    timestamp = os.path.getmtime(filepath)
    time = datetime.datetime.fromtimestamp(timestamp).replace(microsecond=0)
    info = f"""
            Base Model:{model_name} 
            Timestamp:{time}
            """

    return render_template(
        "model.html",
        info=info,
        level=level,
        health=health,
        energy=energy,
        sanity=sanity,
        prediction=prediction,
        confidence=f"{confidence:.2%}",
    )


if __name__ == '__main__':
    APP.run()
