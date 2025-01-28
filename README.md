# DiscoMetrics 🎮

A powerful CLI tool for viewing Discord user statistics and analytics with beautiful terminal visualizations.

## Features

- View detailed user information
- See user roles and status
- Display recent activities
- Visualize account activity over time
- Beautiful terminal UI with graphs and panels

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd discometrics
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root and add your Discord bot token:
```
DISCORD_TOKEN=your_discord_bot_token_here
```

To get a Discord bot token:
1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Go to the Bot section and create a bot
4. Copy the bot token and paste it in your `.env` file

## Usage

View user statistics:
```bash
python discometrics.py stats USERNAME
```

Replace `USERNAME` with the Discord username you want to analyze.

## Example

```bash
python discometrics.py stats "JohnDoe"
```

This will display:
- User information in a beautiful panel
- Account creation date
- Current status and roles
- Recent activities
- Activity graph over time

## Requirements

- Python 3.7+
- Discord Bot Token
- Required packages (listed in requirements.txt)

## Note

Make sure your Discord bot is invited to the servers where you want to analyze users. The bot needs appropriate permissions to view user information. 