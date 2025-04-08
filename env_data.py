import os
from dotenv import load_dotenv


load_dotenv()
TG_API_KEY = os.getenv("TG_API_KEY")
ADD_LINK = os.getenv("ADD_LINK")
STAT_LINK = os.getenv("STAT_LINK")
