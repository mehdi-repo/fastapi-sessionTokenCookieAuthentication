import uvicorn
from fastapi import FastAPI
from model import userModel
from database.connection import engine
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routes import userRoute,adminRoute
# config DB
userModel.Base.metadata.create_all(bind=engine)

# instance 
app=FastAPI()

# config static and templates
app.mount("/static/",StaticFiles(directory="static",html=True))
templates=Jinja2Templates(directory="templates/")


# config routes
app.include_router(userRoute.userRouter)
app.include_router(adminRoute.adminRouter)


if __name__ == "__main__":
    uvicorn.run("main:app",reload=True)
