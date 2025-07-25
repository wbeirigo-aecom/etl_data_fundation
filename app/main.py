
import http
import os
import uuid
from typing import List

from fastapi import FastAPI, UploadFile, File, Response
import os
from dotenv import dotenv_values, load_dotenv

import app.src.config as settings
from app.src.main_task import main
from app.src.coverages import delete_store_layer_style, get_layer



app = FastAPI()


@app.post("/uploadfiles/")
async def upload_files(files: List[UploadFile] = File(...)):
    
    main_path: str = str(uuid.uuid4())
    directory_path = f"{settings.TEMP_FILES}{main_path}"
    os.makedirs(directory_path, exist_ok=True) 
    for file in files:
        contents = await file.read()
        
        with open(f"{directory_path}/{file.filename}", "wb") as f:
            f.write(contents)
    try:
        main(main_path)
    except Exception as e:
        return {"error": str(e)}
    
    return {"filenames": [file.filename for file in files]}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    with open(f"{settings.TEMP_FILES}{file.filename}", "wb") as f:
        f.write(await file.read())
    return {"filename": file.filename}

@app.post("/get_data_dict/")
async def get_data_dict(key: str):
    saida = get_layer(key)
    return saida

@app.delete("/layer/")
async def delete_layer(key: str):
    try:
        delete_store_layer_style(settings.GEOSERVER_WORKSPACE, key)
    except Exception as e:
        return Response(status_code=http.HTTPStatus.INTERNAL_SERVER_ERROR, content=str(e))
    
    return Response(status_code=http.HTTPStatus.NO_CONTENT)
