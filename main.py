from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.user_management import models
from api.user_management.main import router as user_router
from api.payment.payment import router as payment_router
from database.database import engine

app = FastAPI()


# Create the database tables
models.Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user_router)
app.include_router(payment_router)
