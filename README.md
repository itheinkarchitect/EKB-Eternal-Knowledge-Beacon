# EKB — Eternal Knowledge Beacon

A self-hosted Discord bot for automatic server moderation. EKB monitors messages, tracks profanity violations, and applies escalating actions — warnings, temporary mutes, and bans — without manual admin intervention.

![Python](https://img.shields.io/badge/python-3.14-3776AB)
![discord.py](https://img.shields.io/badge/discord.py-2.x-5865F2)
![License](https://img.shields.io/badge/license-MIT-green)

---

## Table of Contents

* [Features](#features)
* [Tech Stack](#tech-stack)
* [Requirements](#requirements)
* [Installation](#installation)
* [Configuration](#configuration)
* [Running the Bot](#running-the-bot)
* [How It Works](#how-it-works)
* [Project Structure](#project-structure)
* [Contributing](#contributing)
* [License](#license)

---

## Features

* **Automatic message monitoring** — scans every message in channels EKB can read.
* **Profanity detection** — filters messages against a word list stored in `bot/data/bad_words.py` and logs each hit.
* **Rolling 24-hour window** — profanity is counted over the last 24 hours, not a calendar day.
* **Escalating punishment system** — warnings → temporary mutes → bans.
* **Repeat-offender bans** — three mutes within a rolling 30-day window trigger a 7-day ban.
* **Ban checker** — background task that lifts bans automatically once they expire.
* **Persistent storage** — violations, warnings, mutes, and bans are stored in SQLite via SQLAlchemy.
* **Lightweight** — runs locally with no external services or paid hosting required.

---

## Tech Stack

| Component       | Technology     |
| --------------- | -------------- |
| Language        | Python 3.14    |
| Discord API     | discord.py 2.x |
| ORM             | SQLAlchemy     |
| Database        | SQLite         |
| Config          | python-dotenv  |
| Package manager | pip            |

---

## Requirements

* Python **3.14** or higher
* A Discord bot token ([how to get one](https://discord.com/developers/applications))
* The **`MESSAGE CONTENT INTENT`** enabled in the Developer Portal — required to read message content.
* Bot permissions on the target server:

  * `Moderate Members` (for mutes)
  * `Ban Members`
  * `Send Messages`

---

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/itheinkarchitect/EKB-Eternal-Knowledge-Beacon.git
   cd EKB-Eternal-Knowledge-Beacon
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv venv

   # Linux / macOS
   source venv/bin/activate

   # Windows
   venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

---

## Configuration

Create a `.env` file in the project root:

```env
DISCORD_TOKEN=your_bot_token_here
```

| Variable        | Description                                 | Required |
| --------------- | ------------------------------------------- | -------- |
| `DISCORD_TOKEN` | Bot token from the Discord Developer Portal | Yes      |

---

## Running the Bot

```bash
python -m bot.main
```

On first launch, the SQLite database is created automatically via `init_database()`.

---

## How It Works

EKB uses a **three-stage escalation model** built on a rolling profanity counter.

### Stage 1 — Warnings

* Profanity is counted per user over a **rolling 24-hour window** (`datetime.now() - timedelta(hours=24)`).
* The threshold check is `total > 30`, so **30 profanities in the last 24 hours are not a violation**.
* The **31st profanity** issues the first warning.
* Every additional profanity past the threshold adds **+1 warning**.

  | Profanities in last 24h | Warnings issued |
  | ----------------------- | --------------- |
  | ≤ 30                    | 0               |
  | 31                      | 1               |
  | 32                      | +1 (total 2)    |
  | 33                      | +1 (total 3)    |
  | …                       | …               |

### Stage 2 — Mutes

* Once a user accumulates **5 warnings**, EKB issues a temporary mute.
* The mute is applied as a Discord timeout for **24 hours** (`timedelta(hours=24)`).

### Stage 3 — Bans

* If a user receives **3 mutes within a rolling 30-day window**, EKB issues a ban.
* Ban length is **7 days**.
* `services/ban_checker.py` runs in the background and **lifts the ban automatically** after the 7-day period expires. The 24-hour Discord timeout is not managed by this service.

The full pipeline: `handler → profanity service → rolling 24h counter → warning → mute → ban`, with moderation events persisted through SQLAlchemy models in `bot/database/`.

---

## Project Structure

```text
EKB-Eternal-Knowledge-Beacon/
├── bot/
│   ├── data/
│   │   └── bad_words.py          # Profanity word list
│   ├── database/
│   │   ├── models.py             # SQLAlchemy ORM models
│   │   ├── database.py           # Engine, session, initialization
│   │   ├── profanity_logs.py     # Logging of detected profanity
│   │   ├── warning.py            # Warning persistence
│   │   ├── mute.py               # Mute persistence
│   │   └── ban.py                # Ban persistence
│   ├── services/
│   │   ├── profanity.py          # Profanity detection logic
│   │   ├── moderation.py         # Core moderation actions
│   │   └── ban_checker.py        # Background task for expired bans
│   ├── handlers/
│   │   └── messages.py           # Message event listener
│   ├── app.py                    # Bot setup and event registration
│   └── main.py                   # Entry point
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## Contributing

Contributions are welcome. To keep things clean:

1. Fork the repository and create a feature branch:

   ```bash
   git checkout -b feature/your-feature
   ```
2. Follow **PEP 8** and keep functions small and focused.
3. Test your changes against a private Discord server before opening a PR.
4. Open a pull request with a clear description of what changed and why.

For bug reports, please include:

* Python version
* discord.py version
* Steps to reproduce
* Relevant console output

---

## License

MIT — see [LICENSE](LICENSE) for details.

```