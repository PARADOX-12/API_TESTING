from dotenv import load_dotenv
import os
import datetime

load_dotenv()

JWT_SECRETE_KEY = os.getenv('JWT_SECRET_KEY')
JWT_ACCESS_TOKEN_EXPIRES =  datetime.timedelta(hours = 1)
JWT_REFRESH_TOKEN = datetime.timedelta(days = 1)