import os
import tweepy
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import random
from dotenv import load_dotenv

load_dotenv()

auth = tweepy.OAuthHandler(
    os.getenv('TWITTER_API_KEY'),
    os.getenv('TWITTER_API_SECRET')
)

auth.set_access_token(
    os.getenv('TWITTER_ACCESS_TOKEN'),
    os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
)

api = tweepy.Client(
    bearer_token=os.getenv('TWITTER_BEARER_TOKEN'),
    access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
    access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET'),
    consumer_key=os.getenv('TWITTER_API_KEY'),
    consumer_secret=os.getenv('TWITTER_API_SECRET'),
)

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

creds_json = os.getenv('GOOGLE_SHEETS_CREDS')
creds_dict = json.loads(creds_json)

creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)


client = gspread.authorize(creds)
sheet = client.open_by_key(os.getenv('GOOGLE_SHEETS_KEY'))

worksheet = sheet.sheet1

records = worksheet.get_all_records()


post_result = api.create_tweet(text='que pasa mufasa :)')

print(post_result)


