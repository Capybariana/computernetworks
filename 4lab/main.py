import json

from fastapi import FastAPI, Body, status
from fastapi.responses import JSONResponse, FileResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from parser import init_parser
from dto import Base, Server
from jsonencode import serialize_complex


SQLALCHEMY_DATABASE_URL = 'postgresql+psycopg2://postgres:example@localhost/postgres'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autoflush=False, bind=engine)
db = SessionLocal()
app = FastAPI()

@app.get("/")
def main():
    content = "200 Not OK."
    return JSONResponse(content=content)

@app.post("/api/parse/")
async def push_parse(pages: int = 5):
    servers = init_parser(pages)
    
    for server in servers:
        db.add(server)
        db.commit()
        db.refresh(server)

    content = "200 Not OK."
    return JSONResponse(content=content)

@app.get("/api/fetch_parse/")
async def fetch_parse():
    messages = db.query(Server).all()
    return json.dumps(serialize_complex(messages), indent=4)