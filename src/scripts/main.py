from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

DATABASE_URL = "mysql+pymysql://root:**********@localhost/Lab4"


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

app = FastAPI()


class Content(Base):
    __tablename__ = "Content"
    id = Column(Integer, primary_key=True, autoincrement=True)
    uploader_id = Column(Integer, nullable=False)
    title = Column(String(200), nullable=False)
    category = Column(String(50))
    url = Column(String(255), nullable=False)


class Queue(Base):
    __tablename__ = "Queue"
    id = Column(Integer, primary_key=True, autoincrement=True)
    reviewer_id = Column(Integer)
    status = Column(String(50))
    Content_id = Column(Integer, ForeignKey("Content.id"), nullable=False)

    content = relationship("Content")


class ContentBase(BaseModel):
    uploader_id: int
    title: str
    category: Optional[str]
    url: str


class ContentCreate(ContentBase):
    pass


class ContentOut(ContentBase):
    id: int

    class Config:
        orm_mode = True


class QueueBase(BaseModel):
    reviewer_id: Optional[int]
    status: Optional[str]
    Content_id: int


class QueueCreate(QueueBase):
    pass


class QueueOut(QueueBase):
    id: int

    class Config:
        orm_mode = True


@app.get("/contents", response_model=List[ContentOut])
def get_contents():
    db = SessionLocal()
    contents = db.query(Content).all()
    db.close()
    return contents


@app.post("/contents", response_model=ContentOut)
def create_content(content: ContentCreate):
    db = SessionLocal()
    db_content = Content(**content.dict())
    db.add(db_content)
    db.commit()
    db.refresh(db_content)
    db.close()
    return db_content


@app.put("/contents/{content_id}", response_model=ContentOut)
def update_content(content_id: int, updated: ContentCreate):
    db = SessionLocal()
    db_content = db.query(Content).get(content_id)
    if not db_content:
        db.close()
        raise HTTPException(status_code=404, detail="Content not found")
    for key, value in updated.dict().items():
        setattr(db_content, key, value)
    db.commit()
    db.refresh(db_content)
    db.close()
    return db_content


@app.delete("/contents/{content_id}")
def delete_content(content_id: int):
    db = SessionLocal()
    db_content = db.query(Content).get(content_id)
    if not db_content:
        db.close()
        raise HTTPException(status_code=404, detail="Content not found")
    db.delete(db_content)
    db.commit()
    db.close()
    return {"message": "Content deleted successfully"}


# ---------- CRUD для Queue ----------
@app.get("/queues", response_model=List[QueueOut])
def get_queues():
    db = SessionLocal()
    queues = db.query(Queue).all()
    db.close()
    return queues


@app.post("/queues", response_model=QueueOut)
def create_queue(queue: QueueCreate):
    db = SessionLocal()
    db_queue = Queue(**queue.dict())
    db.add(db_queue)
    db.commit()
    db.refresh(db_queue)
    db.close()
    return db_queue


@app.put("/queues/{queue_id}", response_model=QueueOut)
def update_queue(queue_id: int, updated: QueueCreate):
    db = SessionLocal()
    db_queue = db.query(Queue).get(queue_id)
    if not db_queue:
        db.close()
        raise HTTPException(status_code=404, detail="Queue not found")
    for key, value in updated.dict().items():
        setattr(db_queue, key, value)
    db.commit()
    db.refresh(db_queue)
    db.close()
    return db_queue


@app.delete("/queues/{queue_id}")
def delete_queue(queue_id: int):
    db = SessionLocal()
    db_queue = db.query(Queue).get(queue_id)
    if not db_queue:
        db.close()
        raise HTTPException(status_code=404, detail="Queue not found")
    db.delete(db_queue)
    db.commit()
    db.close()
    return {"message": "Queue deleted successfully"}
