import json
from praw.reddit import Submission
from praw.models import MoreComments

#
#
#

class Extract:

    #   reddit:     PRAW reddit connection
    #   reddit_db:  MongoDB connection details
    def __init__(self, reddit, reddit_db):
        self._reddit = reddit
        self._reddit_db = reddit_db

    #Extracts comments from a reddit url, iterates through the top comments
    #and saves them in a mongodb collection as well as a local JSON file.
    #
    #   url:            The url of a reddit thread
    #   numComments:    The amount of comments to save
    def extractComments(self, url, numComments):

        print("EXTRACTING COMMENTS")

        submission = self._reddit.submission(url=url)
        submission.comments.replace_more(limit=0)

        x = 0
        comments = []

        for top_level_comment in submission.comments:
            comments.append(Extract.saveCommentToDatabase(top_level_comment, self._reddit_db._collection))
            x += 1
            if x > numComments:
                break
        
        Extract.saveCommentsToJson(comments)

    #Saves each comment found in extractComments to a mongodb collection
    #Also returns a comment dict to be added to an array and saved as JSON.
    #
    #   comment:    The comment obj extracted from extractComments
    #   collection: The MongoDB collection to insert the comments into
    def saveCommentToDatabase(comment, collection):

        print("SAVING COMMENT...")

        try:
            commentObj = {
                "Author": comment.author.name,
                "ID": comment.id,
                "Sub-ID": comment.subreddit_id,
                "Sub-Name": comment.subreddit.display_name,
                "Time Created": comment.created_utc,
                "Text": comment.body,
                "Score": comment.score,
                "Link": comment.permalink
            }

            x = collection.insert_one(commentObj)
            print(x.inserted_id)
            commentObj.pop("_id", None)

        except:
            print("Name/Comment doesn't exist!")

        #Remove this attribute from JSON because it can't serialize it
        return commentObj

    #Takes an array of comment dicts to be saved to a JSON file.
    #
    #   comments:   The array of comments to be saved to JSON
    def saveCommentsToJson(comments):

        with open('./test-data/comments.json', 'w', encoding='utf-8') as file:
            json.dump(comments, file, ensure_ascii=False, indent=4)

