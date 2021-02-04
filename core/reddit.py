from django.conf import settings
import praw


class RedditException(Exception):
    pass


class Reddit:
    reddit = praw.Reddit(
        client_id=settings.REDDIT_CLIENT_ID,
        client_secret=settings.REDDIT_CLIENT_SECRET,
        redirect_uri=settings.REDDIT_REDIRECT_URL,
        user_agent=settings.REDDIT_USER_AGENT
    )

    def get_reddit_url(self, state, format_state=False):
        if format_state:
            state = '-'.join(state)

        return self.reddit.auth.url(
            scopes=["identity", "mysubreddits", "read", "subscribe"],
            state=state,
            duration="temporary",
        )

    def authorize_user(self, code):
        try:
            self.reddit.auth.authorize(code)
        except Exception as e:
            raise RedditException(e)

    def subscribe_to_subreddits(self, subreddit_list):
        current_subreddits = self.get_subreddits_list()
        difference = set(subreddit_list).difference(current_subreddits)

        for subreddit_name in difference:
            try:
                sr = self.reddit.subreddit(subreddit_name)
                sr.subscribe()
            except Exception:
                pass

    def get_subreddits_list(self):
        return [sr.display_name for sr in self.reddit.user.subreddits(limit=None)]
