import praw
import config

def main():
    """
    Main function to interact with Reddit API.
    """
    # Define the subreddit and thread URL
    thread_url = 'https://www.reddit.com/r/FantasyPL/comments/1gx5i1g/rate_my_team_quick_questions_general_advice_daily/'

    title, comments = fetch_top_level_comments(thread_url)

    # Output the submission title
    print(f"Thread Title: {title}\n")

    # Output the total number of comments fetched
    print(f"Total Comments Fetched: {len(comments)}\n")

    # Iterate through comments and print author and comment body
    for comment in comments:
        print(f"Author: {comment.author}")
        print(f"Comment: {comment.body}\n")
        print('_' * 40)

def fetch_top_level_comments(thread_url):
    """
    Fetches top-level comments from Reddit thread
    """
    # Initialize Reddit instance
    reddit = praw.Reddit(
        client_id=config.REDDIT_CLIENT_ID,
        client_secret=config.REDDIT_CLIENT_SECRET,
        username=config.REDDIT_USERNAME,
        password=config.REDDIT_PASSWORD,
        user_agent=config.REDDIT_USER_AGENT
    )

    # Fetch the submission using the URL
    submission = reddit.submission(url=thread_url)

    # Fetch only top-level comments
    submission.comments.replace_more(limit=0)
    comments = list(submission.comments)

    return submission.title, comments


if __name__ == "__main__":
    main()