<div align="center">

```
  ██╗███╗   ██╗███████╗████████╗ █████╗      █████╗ ██╗   ██╗████████╗ ██████╗
  ██║████╗  ██║██╔════╝╚══██╔══╝██╔══██╗    ██╔══██╗██║   ██║╚══██╔══╝██╔═══██╗
  ██║██╔██╗ ██║███████╗   ██║   ███████║    ███████║██║   ██║   ██║   ██║   ██║
  ██║██║╚██╗██║╚════██║   ██║   ██╔══██║    ██╔══██║██║   ██║   ██║   ██║   ██║
  ██║██║ ╚████║███████║   ██║   ██║  ██║    ██║  ██║╚██████╔╝   ██║   ╚██████╔╝
  ╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝  ╚═╝    ╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝
```

**Instagram Reels Automation Bot**

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue?style=flat-square&logo=python)](https://python.org)
[![instagrapi](https://img.shields.io/badge/instagrapi-2.1.3-E1306C?style=flat-square&logo=instagram&logoColor=white)](https://github.com/subzeroid/instagrapi)
[![Claude AI](https://img.shields.io/badge/Claude%20AI-Sonnet%204.6-6B21A8?style=flat-square)](https://anthropic.com)
[![yt-dlp](https://img.shields.io/badge/yt--dlp-latest-FF0000?style=flat-square&logo=youtube&logoColor=white)](https://github.com/yt-dlp/yt-dlp)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Issues](https://img.shields.io/github/issues/najinkya776/InstaAutomation?style=flat-square)](https://github.com/najinkya776/InstaAutomation/issues)
[![Stars](https://img.shields.io/github/stars/najinkya776/InstaAutomation?style=flat-square)](https://github.com/najinkya776/InstaAutomation/stargazers)

*Find it. Download it. Rewrite it. Repost it. Automatically.*

[Features](#features) · [Quick Start](#quick-start) · [API Keys](#api-keys) · [Usage](#usage) · [Configuration](#configuration)

</div>

---

## What is InstaAuto?

InstaAuto is an open-source Instagram Reels automation bot that runs on a schedule. It scrapes hashtags for trending reels, ranks them by real view count, downloads the top performers, rewrites their captions using **Claude AI** so every post is unique, and reposts them directly to your Instagram account.

A SQLite duplicate tracker ensures the same reel is never posted twice. Session persistence avoids repeated logins and 2FA prompts.

No manual work. No repeated captions. No reposting the same reel twice.

---

## Features

| Module | Description | Powered By |
|---|---|---|
| **🔍 Hashtag Scraper** | Pulls Instagram's "Top Posts" for any hashtag and ranks by real view count | instagrapi |
| **⬇️ Smart Downloader** | yt-dlp primary with instagrapi fallback — handles all format edge cases | yt-dlp / instagrapi |
| **🤖 AI Caption Rewriter** | Rewrites every caption from scratch so it's 100% unique, appends your hashtags | Claude Sonnet 4.6 |
| **📤 Reel Uploader** | Posts the video natively as an Instagram Reel with the new caption | instagrapi |
| **🕐 Auto Scheduler** | Configurable interval (default every 6h) — runs indefinitely in the background | schedule |
| **🛡️ Duplicate Guard** | SQLite DB tracks every posted reel PK — never reposts the same one | SQLite |
| **🔑 Session Persistence** | Saves login session to `session.json` to avoid repeated auth + 2FA prompts | instagrapi |
| **🧹 Auto Cleanup** | Deletes local video files after each successful post | — |
| **📋 Full Logging** | Timestamped logs to both console and `automation.log`, run history in DB | logging |

---

## Quick Start

### Prerequisites

- Python 3.11+
- pip
- An Instagram account
- An [Anthropic API key](https://console.anthropic.com)

### Installation

```bash
git clone https://github.com/najinkya776/InstaAutomation.git
cd InstaAutomation
pip install -r requirements.txt
```

### Configure

```bash
cp .env.example .env
```

Edit `.env` with your credentials (see [API Keys](#api-keys) below), then:

```bash
python main.py
```

On first run it logs in, saves `session.json`, runs one full cycle immediately, then schedules recurring runs.

---

## API Keys

InstaAuto works with **no extra API keys** for scraping and downloading. Claude AI is required only for caption rewriting — without it, the original caption is used as a fallback.

| Service | Required For | Get Key |
|---|---|---|
| Instagram Account | Everything (login) | Your existing account |
| [Anthropic Claude](https://console.anthropic.com) | AI caption rewriting | Free credits on signup |

Keys are stored locally in `.env` — this file is **gitignored** and never committed.

---

## Usage

### Run

```bash
python main.py
```

The bot will:
1. Log in to Instagram (or load saved session)
2. Scrape top reels for each hashtag in your config
3. Skip any reel already posted (checked against SQLite DB)
4. Download top-ranked reels via yt-dlp
5. Rewrite the caption using Claude AI
6. Post as an Instagram Reel
7. Wait for the configured delay, then repeat

### Logs

All activity is written to `automation.log` in real time:

```
2026-04-27 08:00:01 [INFO] Starting automation cycle
2026-04-27 08:00:03 [INFO] Fetching top reels for #fitness
2026-04-27 08:00:05 [INFO]   Reel 3421... | views=1,240,000 | likes=84200
2026-04-27 08:00:05 [INFO] Downloaded via yt-dlp: downloads/3421....mp4
2026-04-27 08:00:07 [INFO] Rewritten caption: Push your limits every single day...
2026-04-27 08:00:21 [INFO] Posted reel successfully: 3421... | code=CxYz...
2026-04-27 08:00:21 [INFO] Cycle complete. Posted 1 reel(s).
```

---

## Configuration

| Variable | Default | Description |
|---|---|---|
| `INSTAGRAM_USERNAME` | — | Your Instagram username |
| `INSTAGRAM_PASSWORD` | — | Your Instagram password |
| `ANTHROPIC_API_KEY` | — | Anthropic API key |
| `HASHTAGS` | `fitness` | Comma-separated hashtags (no `#`) |
| `POST_INTERVAL_HOURS` | `6` | Hours between each automated cycle |
| `MAX_POSTS_PER_CYCLE` | `2` | Max reels to post per run |
| `DELAY_BETWEEN_POSTS` | `60` | Seconds to wait between posts |

---

## Project Structure

```
InstaAutomation/
├── main.py            # Entry point — wires everything + runs the scheduler
├── auth.py            # Instagram login + session persistence
├── scraper.py         # Hashtag scraper + view-count ranker
├── downloader.py      # yt-dlp download with instagrapi fallback
├── rewriter.py        # Claude AI caption rewriter
├── uploader.py        # Instagram Reel uploader + local file cleanup
├── db.py              # SQLite duplicate tracker + run logger
├── requirements.txt   # Python dependencies
├── .env.example       # Config template
└── .gitignore         # Keeps .env, session.json, and downloads out of git
```

---

## Safety & Rate Limits

> Instagram detects automation. These defaults are conservative by design.

- Max **2 reels per cycle** (configurable)
- **60-second delay** between posts
- **6-hour interval** between full cycles (~8 posts/day max)
- Random request delays of 2–5s built into every instagrapi call
- Session reuse avoids repeated login challenges

Do not set `MAX_POSTS_PER_CYCLE` above 3 or `POST_INTERVAL_HOURS` below 4 without expecting account action from Instagram.

---

## Contributing

Contributions are welcome! Open an issue or submit a PR.

Ideas for future modules: watermark overlay, multi-account support, Telegram notifications, story reposting, analytics dashboard.

---

## Disclaimer

This tool is for **educational purposes only**. Automating Instagram actions may violate [Instagram's Terms of Service](https://help.instagram.com/581066165581870). Use responsibly and only on accounts you own. The author is not responsible for any account suspension or ban resulting from use of this tool. Always credit original creators when reposting their content.

---

## License

MIT — see [LICENSE](LICENSE) for details.

---

<div align="center">
Built for content creators by <a href="https://github.com/najinkya776">Ajinkya Kadam</a>. Made with Python and Claude AI.
</div>
