import sys
import json
import praw

from comments import Extract
from scraper_db import Database

#
#
#

class Main():

    def main():
        print("START...")

        with open('/home/tarand/Documents/Projects/crispy-funicular/src/settings.json') as f:
            reddit_data = json.load(f)

        reddit = praw.Reddit(
            user_agent=reddit_data["user_agent"],
            client_id=reddit_data["client_id"],
            client_secret=reddit_data["client_secret"],
            username=reddit_data["username"],
            password=reddit_data["password"],
        )

        #sub_url = input("Enter submission url: ")
        sub_url = "https://www.reddit.com/r/wallstreetbets/comments/nzjc6w/daily_discussion_thread_for_june_14_2021/?sort=new"
        
        scraper_reddit_db = Database(client=reddit_data["db_client"], database=reddit_data["db_database"], collection=reddit_data["db_collection"])
        Database.connect(scraper_reddit_db)

        comment_scraper = Extract(reddit, scraper_reddit_db)
        Extract.extractComments(comment_scraper, sub_url)

        exit()

if __name__ == "__main__":
    Main.main()