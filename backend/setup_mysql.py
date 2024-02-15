from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import requests
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
SQLALCHEMY_DATABASE_URI = "URI_HERE"

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Base(DeclarativeBase):
    pass

class TranscriptChunk(Base):
    __tablename__ = "transcripts"

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(String(4096))


def create_table():

    with app.app_context():
        Base.metadata.create_all(db.engine)

def setup_table():

    with app.app_context():
        url = "https://podcast-1uwwj7r.svc.gcp-starter.pinecone.io/vectors/fetch"
        headers = {
            "Api-Key":"API_HERE",
            "accept": "application/json"
        }
        batch_num = 100
        num_records = 28962
        i=2

        while i<num_records+2:
            batch = []
            for j in range(0,batch_num):
                if i<num_records+2:
                    batch.append(str(i))
                    i+=1
                else:
                    break

            data = "?ids=" + "&ids=".join(batch)


            response = requests.get(url+data, headers=headers)

            chunks = response.json()

            upsert_data = []

            for key in chunks["vectors"]:
                text = chunks["vectors"][key]["metadata"]["text"]
                upsert_data.append(TranscriptChunk(id=int(key), content=text))

            db.session.add_all(upsert_data)
            db.session.commit()









