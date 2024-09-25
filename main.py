import os
import tweepy
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
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

empty_posted_records = [record for record in records if record['Posted'] == '']

if empty_posted_records:
    index = records.index(empty_posted_records[0])
    text = (
         str(empty_posted_records[0]['Title']) + '. ' 
        + str(empty_posted_records[0]['Period']) + ' - ' 
        + str(empty_posted_records[0]['Story']) + ' ' 
        + str(empty_posted_records[0]['Data']) + ' ' 
        + str(empty_posted_records[0]['Conclusion']) + ' ' 
        + str(empty_posted_records[0]['Hashtags'])
    )
    if len(text) > 280:
        text = (
         str(empty_posted_records[0]['Title']) + '. ' 
        + str(empty_posted_records[0]['Period']) + ' - ' 
        + str(empty_posted_records[0]['Story']) + ' ' 
        + str(empty_posted_records[0]['Conclusion']) + ' ' 
        + str(empty_posted_records[0]['Hashtags'])
    )
    if len(text) > 280:
        text = (
         str(empty_posted_records[0]['Title']) + '. ' 
        + str(empty_posted_records[0]['Period']) + ' - ' 
        + str(empty_posted_records[0]['Story']) + ' '
        + str(empty_posted_records[0]['Hashtags'])
    )
    
    post_result = api.create_tweet(text=text)
    
    tweet_id = post_result.data['id']
    print(f"Tweet publicado con ID: {tweet_id}")
    
    worksheet.update_cell(index + 2, 9, "Yes")
    worksheet.update_cell(index + 2, 10, tweet_id)

else:
    print("No se encontró ningún registro con 'Posted' vacío.")


