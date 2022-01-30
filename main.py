import datetime

from IPython import display
import math
from pprint import pprint
import pandas as pd
import numpy as np
import nltk
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style='darkgrid', context='talk', palette='Dark2')
import datetime as dt
import praw
from psaw import PushshiftAPI
import pandas as pd
import pickle

r = praw.Reddit(client_id='K9TQ2OD9q_7rn4Hch7hqhA',
                     client_secret='-ygBA4rhS5Gxc41ABLq_1MdXYCgJKg',
                     user_agent='crypto_sentiment_bot')


reddit_api = PushshiftAPI(r)

start_epoch = dt.datetime(2021,1,1)
end_epoch =  dt.datetime(2022,1,30)

current_date = start_epoch
submissions_by_day = []
while current_date <= end_epoch:
    print(current_date)
    curr_date_timestamp = int(current_date.timestamp())

    next_day = current_date + datetime.timedelta(days= 1)

    next_day_timestamp = int(next_day.timestamp())

    results = list(reddit_api.search_submissions(before=next_day_timestamp,
                                                 after=curr_date_timestamp,
                                                 subreddit="CryptoCurrency",


                                                 ))
    if results != []:
        df = pd.DataFrame([[post.name,post.title, post.permalink,post.score,post.num_comments,post.created]for post in results])
        df.columns = ['id','title','link','score','comments_num','date']
        df.drop_duplicates(subset=['id'],inplace=True)

        df.sort_values( by=['score'], ascending=False, inplace=True, ignore_index=True)
        submissions_by_day.append(df)
    # print(len(results))

    current_date +=  datetime.timedelta(days= 1)



with open('submission_data.pickle', 'wb') as handle:
    pickle.dump(submissions_by_day, handle, protocol = pickle.HIGHEST_PROTOCOL)
print("test")