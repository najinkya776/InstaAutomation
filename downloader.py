import os
import logging
import yt_dlp
from instagrapi import Client
from instagrapi.types import Media

logger = logging.getLogger(__name__)

DOWNLOAD_DIR = "downloads"


def download_reel_ytdlp(url: str) -> str | None:
    """Download a reel via yt-dlp. Returns local file path or None on failure."""
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    opts = {
        "outtmpl": os.path.join(DOWNLOAD_DIR, "%(id)s.%(ext)s"),
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "merge_output_format": "mp4",
        "quiet": True,
        "no_warnings": True,
    }

    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
            path = ydl.prepare_filename(info)
            # yt-dlp may change extension after merge
            if not os.path.exists(path):
                path = path.rsplit(".", 1)[0] + ".mp4"
            logger.info(f"Downloaded via yt-dlp: {path}")
            return path
    except Exception as e:
        logger.error(f"yt-dlp download failed for {url}: {e}")
        return None


def download_reel_instagrapi(client: Client, media: Media) -> str | None:
    """Fallback: download via instagrapi's built-in clip_download."""
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    try:
        path = client.clip_download(media.pk, folder=DOWNLOAD_DIR)
        logger.info(f"Downloaded via instagrapi: {path}")
        return str(path)
    except Exception as e:
        logger.error(f"instagrapi download failed for {media.pk}: {e}")
        return None


def download_reel(client: Client, media: Media, url: str) -> str | None:
    """Try yt-dlp first, fall back to instagrapi."""
    path = download_reel_ytdlp(url)
    if path and os.path.exists(path):
        return path
    logger.warning("yt-dlp failed, trying instagrapi fallback...")
    return download_reel_instagrapi(client, media)
