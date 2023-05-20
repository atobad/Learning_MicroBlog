import datetime
import os
from flask import Flask, render_template, request
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    client = MongoClient(os.getenv("MONGODB_URI"))
    app.db = client.microblog

    @app.route("/", methods=["GET", "POST"])
    def home():
        # print([e for e in app.db.entries.find({})])    # 這個是讀取資料使用的，測試。不需要 
        if request.method == "POST":
            entry_content = request.form.get("content")
            formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
            app.db.entries.insert_one({"content" : entry_content , "date" : formatted_date})

        entries_with_date = [
            (
                entry["content"],
                entry["date"],
                datetime.datetime.strptime(entry["date"],"%Y-%m-%d").strftime("%b %d")
            )
            for entry in app.db.entries.find({})
        ]
        # print(entry_content, formatted_date)
        return render_template("home.html", entries = entries_with_date )
    return app

