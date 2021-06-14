import json
from praw.reddit import Submission
from praw.models import MoreComments

class Extract:

    def __init__(self, reddit, reddit_db):

        self._reddit = reddit
        self._reddit_db = reddit_db

    def extractComments(self, url):

        print("EXTRACTING COMMENTS")

        submission = self._reddit.submission(url=url)
        submission.comments.replace_more(limit=0)

        for top_level_comment in submission.comments:
            Extract.saveComment(top_level_comment, self._reddit_db._collection)

    def saveComment(comment, collection):

        print("SAVING COMMENT...")

        try:
            commentObj = {
                "Author": comment.author.name,
                "ID": comment.id,
                "Sub-ID": comment.subreddit_id,
                "Sub-Name": comment.subreddit.name,
                "Time Created": comment.created_utc,
                "Text": comment.body,
                "Score": comment.score
            }

            x = collection.insert_one(commentObj)
            print(x.inserted_id)

        except:
            print("Name/Comment doesn't exist!")



