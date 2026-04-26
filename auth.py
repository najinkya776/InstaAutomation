import os
import logging
from instagrapi import Client
from instagrapi.exceptions import LoginRequired, TwoFactorRequired

logger = logging.getLogger(__name__)

SESSION_FILE = "session.json"


def get_client(username: str, password: str) -> Client:
    """
    Returns an authenticated instagrapi Client.
    Loads saved session if available, otherwise logs in fresh.
    """
    cl = Client()
    cl.delay_range = [2, 5]  # random delay between requests (seconds)

    if os.path.exists(SESSION_FILE):
        try:
            cl.load_settings(SESSION_FILE)
            cl.login(username, password)
            cl.get_timeline_feed()  # quick check that session is alive
            logger.info("Loaded existing session.")
            return cl
        except LoginRequired:
            logger.warning("Saved session expired, logging in fresh...")
        except Exception as e:
            logger.warning(f"Session load error ({e}), logging in fresh...")

    try:
        cl.login(username, password)
        cl.dump_settings(SESSION_FILE)
        logger.info("Logged in fresh and saved session.")
        return cl
    except TwoFactorRequired:
        code = input("Enter your 2FA code: ").strip()
        cl.login(username, password, verification_code=code)
        cl.dump_settings(SESSION_FILE)
        logger.info("Logged in with 2FA and saved session.")
        return cl
