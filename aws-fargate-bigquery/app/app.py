import datetime
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import os
from google.cloud import bigquery
from google.oauth2 import service_account
credentials = service_account.Credentials.from_service_account_file('./gcreds.json')

client = bigquery.Client(
    credentials=credentials,
    project=credentials.project_id,
)

#consumer key, consumer secret, access token, access secret.
ACCESS_TOKEN =""
ACCESS_SECRET =""
CONSUMER_KEY =""
CONSUMER_SECRET =""
count=0
project_id = ''
dataset_id=""
table_id = ''
dataset_ref = client.dataset(dataset_id, project=project_id)
table_ref = dataset_ref.table(table_id)
table = client.get_table(table_ref)  # API Request

def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()
    return json.dumps(
      item,
      sort_keys=True,
      indent=1,
      default=default)


class listener(StreamListener):
    def on_data(self, data):
        global count
        all_data = json.loads(data)
        tweet = all_data["text"]
        username = all_data["user"]["screen_name"]
        lang = all_data["lang"]
        from datetime import datetime
        import pytz
        tz = pytz.timezone('Europe/Berlin')
        now = datetime.now(tz)
        import datetime
        now = default(now)
        count=count+1
        print(count,tweet,username,lang,now)
        rows_to_insert = [(tweet,username,lang,now)]
        errors = client.insert_rows(table, rows_to_insert)  # API request
        assert errors == []
        return(True)

    def on_error(self, status):
        print(status)

auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
twitterStream = Stream(auth, listener())

try:
    twitterStream.filter(track=["grève","Retraites","cgt","reforme","reformedesretraites","manifestation","CFDT"],languages=["fr"])
except Exception as err:
    print(err.message)
    for i in err.message:
        print(i)
