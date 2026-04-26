import os
import time
import logging
import schedule
from dotenv import load_dotenv

from auth import get_client
from scraper import get_top_reels, reel_url
from downloader import download_reel, cleanup_video
from rewriter import rewrite_caption
from uploader import post_reel
from db import init_db, already_posted, mark_posted, log_run

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler("automation.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

USERNAME = os.getenv("INSTAGRAM_USERNAME", "")
PASSWORD = os.getenv("INSTAGRAM_PASSWORD", "")
HASHTAGS = [h.strip() for h in os.getenv("HASHTAGS", "fitness").split(",")]
POST_INTERVAL_HOURS = int(os.getenv("POST_INTERVAL_HOURS", "6"))
MAX_POSTS_PER_CYCLE = int(os.getenv("MAX_POSTS_PER_CYCLE", "2"))
DELAY_BETWEEN_POSTS = int(os.getenv("DELAY_BETWEEN_POSTS", "60"))


def run_cycle():
    logger.info("=== Starting automation cycle ===")
    log_run("started", f"hashtags={HASHTAGS}")
    posts_this_cycle = 0

    for hashtag in HASHTAGS:
        if posts_this_cycle >= MAX_POSTS_PER_CYCLE:
            logger.info("Reached max posts per cycle, stopping.")
            break

        reels = get_top_reels(client, hashtag, top_n=5)

        for media in reels:
            if posts_this_cycle >= MAX_POSTS_PER_CYCLE:
                break

            if already_posted(media.pk):
                logger.info(f"Skipping already-posted reel {media.pk}")
                continue

            url = reel_url(media)
            logger.info(f"Processing reel: {url}")

            video_path = download_reel(client, media, url)
            if not video_path:
                logger.error(f"Download failed for {url}, skipping.")
                continue

            original_caption = media.caption_text or ""
            new_caption = rewrite_caption(original_caption, [hashtag])

            success = post_reel(client, video_path, new_caption)
            cleanup_video(video_path)

            if success:
                mark_posted(media.pk, hashtag=hashtag, original_url=url)
                posts_this_cycle += 1
                logger.info(f"Posted {posts_this_cycle}/{MAX_POSTS_PER_CYCLE} this cycle.")
                if posts_this_cycle < MAX_POSTS_PER_CYCLE:
                    logger.info(f"Waiting {DELAY_BETWEEN_POSTS}s before next post...")
                    time.sleep(DELAY_BETWEEN_POSTS)

    log_run("completed", f"posted={posts_this_cycle}")
    logger.info(f"=== Cycle complete. Posted {posts_this_cycle} reel(s). ===")


if __name__ == "__main__":
    if not USERNAME or not PASSWORD:
        raise SystemExit("ERROR: Set INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD in .env")

    init_db()
    client = get_client(USERNAME, PASSWORD)

    logger.info(f"Scheduler started. Running every {POST_INTERVAL_HOURS} hour(s).")
    logger.info(f"Monitoring hashtags: {HASHTAGS}")

    # Run once immediately on startup
    run_cycle()

    # Then schedule recurring runs
    schedule.every(POST_INTERVAL_HOURS).hours.do(run_cycle)

    while True:
        schedule.run_pending()
        time.sleep(60)
