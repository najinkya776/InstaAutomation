import logging
from instagrapi import Client
from instagrapi.types import Media

logger = logging.getLogger(__name__)


def get_top_reels(client: Client, hashtag: str, top_n: int = 2) -> list[Media]:
    """
    Fetch trending reels for a hashtag, ranked by view count.
    Returns up to top_n Media objects.
    """
    logger.info(f"Fetching top reels for #{hashtag}")
    try:
        # Top posts for the hashtag (Instagram's own trending selection)
        medias = client.hashtag_medias_top(hashtag, amount=30)
    except Exception as e:
        logger.error(f"Failed to fetch medias for #{hashtag}: {e}")
        return []

    # media_type 2 = video/reel, clip_pk present means it's a Reel
    reels = [m for m in medias if m.media_type == 2]

    if not reels:
        logger.warning(f"No reels found for #{hashtag}")
        return []

    ranked = sorted(reels, key=lambda m: m.view_count or 0, reverse=True)
    top = ranked[:top_n]

    for r in top:
        logger.info(
            f"  Reel {r.pk} | views={r.view_count:,} | "
            f"likes={r.like_count} | code={r.code}"
        )

    return top


def reel_url(media: Media) -> str:
    return f"https://www.instagram.com/reel/{media.code}/"
