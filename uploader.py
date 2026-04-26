import os
import logging
from instagrapi import Client

logger = logging.getLogger(__name__)


def post_reel(client: Client, video_path: str, caption: str) -> bool:
    """Upload a video as an Instagram Reel. Returns True on success."""
    if not os.path.exists(video_path):
        logger.error(f"Video file not found: {video_path}")
        return False

    try:
        media = client.clip_upload(path=video_path, caption=caption)
        logger.info(f"Posted reel successfully: {media.pk} | code={media.code}")
        return True
    except Exception as e:
        logger.error(f"Failed to upload reel: {e}")
        return False


def cleanup_video(video_path: str):
    """Delete the local video file after posting."""
    try:
        os.remove(video_path)
        logger.info(f"Cleaned up: {video_path}")
    except Exception as e:
        logger.warning(f"Could not delete {video_path}: {e}")
