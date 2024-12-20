from typing import Union
from fastapi import FastAPI, UploadFile
from pymongo.mongo_client import MongoClient
from urllib.parse import quote_plus
import pandas as pd



app=FastAPI(title="Movie Dataset")


db_password = quote_plus('Ethan@264')
uri = "mongodb+srv://Bhargav:{}@cluster0.sgkor.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0".format(db_password)
client = MongoClient(uri)

db = client.MovieDB

@app.post("/uploadfile/")
def create_upload_file(file: Union[UploadFile,None] = None):
    if not file:
        return {"message": "No upload file sent"}

    file_name = file.filename.strip()
    file_type = file_name.split(".")[1]
    file_size_mb = file.size/1024/1000

    if "csv" not in file_type:
        return {"message": "please upload csv not this {} file".format(file_type)}

    if file_size_mb > 100:
        return {"message": "file size should be less than 100"}

    df = pd.read_csv(file_name)
    required_df = df [['release_date', 'revenue', 'status', 'title', 'vote_average','languages']]
    required_df['release_date'] = required_df['release_date'].ffill()
    required_df['release_date'] = pd.to_datetime(required_df['release_date'], errors='coerce')
    required_df['release_year'] = required_df['release_date'].dt.year.fillna(0).astype(int)
    movie_collection = []
    for _, row in required_df.iterrows():
        data = {
            "release_year": row['release_year'],
            "release_date": row['release_date'],
            "revenue": row['revenue'],
            "title": row['title'],
            "rating": row['vote_average'],
            "languages": row['languages'],
            "status": row['status']
        }
        movie_collection.append(data)
    db.movies.insert_many(movie_collection)
    return {"message": "file upload successfully"}

@app.get("/api/v1/crm/data")
def get_data(start_index:int=1, count:int=10, release_year:int=None, sort_by:str=None, language:str=None):
    skip = (start_index - 1) * count
    query = {}
    if release_year:
        query["release_year"] = release_year
    if language:
        query["languages"] = {"$in": [f"['{language}']"]}

    sort_criteria = None
    if sort_by in ["release_date", "rating"]:
        sort_criteria = {sort_by:-1}  # Descending order

    # Fetch data from MongoDB
    try:
        cursor = db.movies.find(query, {"_id": 0})  # Exclude '_id' field
        if sort_criteria:
            cursor = cursor.sort(sort_criteria)
        cursor = cursor.skip(skip).limit(count)
        data = list(cursor)
        return {"status": "SUCCESS", "data": data}
    except Exception as e:
        return {"status": "FAILED", "message": str(e)}
