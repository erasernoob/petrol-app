from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/uploadFile")
async def getUploadedFile():
    return {"message": "Hello World"}
    
