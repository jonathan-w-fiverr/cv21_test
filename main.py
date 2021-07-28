from typing import Optional
import sys
from fastapi import FastAPI, UploadFile, File
from resume_parser import resumeparse
import aiofiles
app = FastAPI()


@app.get("/")
def stam(fileName):
    data = resumeparse.read_file_return(fileName)
    return data


@app.post("/import")
async def post_endpoint(in_file: UploadFile=File(...)):
    # ...
    async with aiofiles.open('tmp/example', 'wb') as out_file:
        while content := await in_file.read(1024):
            print(123123)# async read chunk
            await out_file.write(content)  # async write chunk

    data = resumeparse.read_file_return('tmp/example')
    return data

