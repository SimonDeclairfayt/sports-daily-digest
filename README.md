# Sports Daily Digest

A simple automated tool that collects the latest football news and sends a curated digest by email. Perfect for staying updated on the latest football news without spending time visiting multiple websites.

## Project Overview

Sports Daily Digest uses the Gemini API to search for and summarize the latest football news from selected sources. It's designed to provide a daily email digest containing:

- Latest match results
- Player injuries
- Match analyses
- Competition information (Ligue 1, Champions League, etc.)

## Features

- Automated news collection from trusted sports websites
- Date-filtered content (only news from the last 24 hours)
- Structured output with titles, URLs, publication dates, and summaries
- Planned email delivery feature

## Setup Instructions

### Prerequisites

- Python 3.x
- Google Gemini API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/SimonDeclairfayt/sports-daily-digest.git
cd sports-daily-digest
```

2. Create a virtual environment:
```bash
python -m venv myvenv
source myvenv/bin/activate  # On Windows: myvenv\Scripts\activate
```

3. Install dependencies:
```bash
pip install google-generativeai python-dotenv
```

4. Create a `.env` file in the project root with your Gemini API key:
```
GEMINI_KEY=your_gemini_api_key_here
```

## Usage

Run the script to generate the latest football news digest:

```bash
python extract.py
```

## Planned Features

- Email delivery using a service like Mailjet
- Additional news sources
- Customizable news categories
- Web interface for configuration
- Server deployment for automated daily sending

## Contributing

Feel free to fork this repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
