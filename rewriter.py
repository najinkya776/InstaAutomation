import logging
import anthropic

logger = logging.getLogger(__name__)

_client: anthropic.Anthropic | None = None


def _get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic()
    return _client


def rewrite_caption(original: str, hashtags: list[str]) -> str:
    """
    Use Claude to rewrite an Instagram caption so it's fresh and unique.
    Always appends the provided hashtags.
    """
    tag_string = " ".join(f"#{h}" for h in hashtags)

    if not original.strip():
        prompt = (
            f"Write a short, engaging Instagram Reel caption (2-3 sentences max). "
            f"Make it motivational, relatable, and trendy. "
            f"End with these hashtags on a new line: {tag_string}"
        )
    else:
        prompt = (
            f"Rewrite this Instagram Reel caption in a fresh, engaging way. "
            f"Keep the same topic and energy but use completely different words. "
            f"Keep it short (2-3 sentences max). "
            f"End with these hashtags on a new line: {tag_string}\n\n"
            f"Original caption:\n{original[:500]}"
        )

    try:
        response = _get_client().messages.create(
            model="claude-sonnet-4-6",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}],
        )
        new_caption = response.content[0].text.strip()
        logger.info(f"Rewritten caption: {new_caption[:80]}...")
        return new_caption
    except Exception as e:
        logger.error(f"Caption rewrite failed: {e}")
        # Fall back to original caption + hashtags if AI fails
        fallback = (original[:400] + "\n\n" + tag_string).strip()
        return fallback
