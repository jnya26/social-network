import datetime
import os
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader
import cloudinary.api

# load environment variables from .env
load_dotenv()


class Config:
    """
    Base configuration class
    """

    # read from .env file
    SECRET_KEY = os.environ.get("SECRET_KEY")
    # SQLALCHEMY_DATABASE_URI = "sqlite:///network.db"
    POSTGRES_HOST = os.environ.get('POSTGRES_HOST')
    POSTGRES_USER = os.environ.get('POSTGRES_USER')
    POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
    POSTGRES_DATABASE = os.environ.get('POSTGRES_DATABASE')

    # Cloudinary configuration
    cloudinary.config(
        cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME'),
        api_key=os.environ.get('CLOUDINARY_API_KEY'),
        api_secret=os.environ.get('CLOUDINARY_API_SECRET')
    )

    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{}:{}@{}/{}'.format(
        POSTGRES_USER,
        POSTGRES_PASSWORD,
        POSTGRES_HOST,
        POSTGRES_DATABASE
    )


JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=5)
