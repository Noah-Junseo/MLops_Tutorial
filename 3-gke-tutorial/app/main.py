from fastapi import FastAPI
import uvicorn
import math

app = FastAPI()



@app.get("/")
async def root():
    x = 0.0001
    for i in range(1000000):
        x += math.sqrt(x)
    return f"안녕하세요. 😘"



if __name__ == "__main__":
    uvicorn.run(app="main:app", host='0.0.0.0', port=8080)
