# Example link from mee6:
# https://reddit.com/r/shorthairedwaifus/comments/lfpg4m/smug_nia_date_a_live/

# Real link from reddit:
# https://www.reddit.com/r/ProjectGG/comments/li2zop/ichika/?

import asyncpraw
import config

# Removal messages
rules = {
    "2": "This post has been removed for violating **Rule 2**:\n\n> 2\. Posts must contain a character with short hair.",
    "6": "This post has been removed for violating **Rule 6**:\n\n> 6\. No reposts within 1 month or any of the current top 50.",
    "7": "This post has been removed for violating **Rule 7**:\n\n> 7\. No lewd lolis."
}

# Create reddit instance
reddit = asyncpraw.Reddit(
    client_id=config.reddit['client_id'],
    client_secret=config.reddit['client_secret'],
    user_agent=config.reddit['user_agent'],
    username=config.reddit['username'],
    password=config.reddit['password']
)

# remove_post("https://www.reddit.com/r/ProjectGG/comments/li2zop/ichika/", 2)
async def remove_post(post_url, rule=''):
    submission = await reddit.submission(url=post_url)
    await submission.mod.remove()
    if rule:
        removal_comment = await submission.reply(rules[str(rule)])
        await removal_comment.mod.distinguish()
