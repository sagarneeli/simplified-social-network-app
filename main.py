from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessionLocal, engine
from models import User, Post, Follow, generate_post_id, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()


class ComposeRequest(BaseModel):
    userId: str
    content: str


class FollowRequest(BaseModel):
    followerId: str
    followeeId: str


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.post("/compose", status_code=status.HTTP_201_CREATED)
def compose(request: ComposeRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.userId == request.userId).first()
    if not user:
        user = User(userId=request.userId)
        db.add(user)
        db.commit()

    post = Post(postId=generate_post_id(), userId=user.userId, content=request.content)
    db.add(post)
    db.commit()

    return {"message": "Post created successfully."}


@app.get("/getFeed/{userId}")
def get_feed(userId: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.userId == userId).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )

    followed_users = [follow.followeeId for follow in user.follows]
    followed_users.append(user.userId)

    return (
        db.query(Post)
        .filter(Post.userId.in_(followed_users))
        .order_by(Post.postId.desc())
        .limit(10)
        .all()
    )


@app.post("/follow", status_code=status.HTTP_201_CREATED)
def follow(request: FollowRequest, db: Session = Depends(get_db)):
    follower = db.query(User).filter(User.userId == request.followerId).first()
    followee = db.query(User).filter(User.userId == request.followeeId).first()
    if not follower or not followee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User(s) not found."
        )

    follow = Follow(followerId=follower.userId, followeeId=followee.userId)
    db.add(follow)
    db.commit()

    return {"message": "User followed successfully."}


@app.post("/unfollow", status_code=status.HTTP_200_OK)
def unfollow(request: FollowRequest, db: Session = Depends(get_db)):
    follower = db.query(User).filter(User.userId == request.followerId).first()
    followee = db.query(User).filter(User.userId == request.followeeId).first()
    if not follower or not followee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User(s) not found."
        )

    follow = (
        db.query(Follow)
        .filter(
            Follow.followerId == follower.userId, Follow.followeeId == followee.userId
        )
        .first()
    )
    if not follow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not being followed."
        )

    db.delete(follow)
    db.commit()

    return {"message": "User unfollowed successfully."}


@app.get("/", status_code=status.HTTP_200_OK)
def root():
    return {"message": "Hello World"}


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(status_code=exc.status_code, content={"message": exc.detail})


# Register the exception handler globally
app.add_exception_handler(HTTPException, http_exception_handler)
