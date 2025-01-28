# dmetrics 🚀

A beautiful command-line tool for viewing GitHub user statistics and analytics with stunning terminal visualizations.

## Features

- 👤 Detailed GitHub user profile information
- 📊 Repository statistics and analytics
- 🔤 Programming language distribution
- 📈 Contribution activity graphs
- ⭐ Star counts and statistics
- 🔄 User comparison functionality
- 🎨 Beautiful terminal UI with graphs and panels

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd dmetrics
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Set up a GitHub token for increased API rate limits:
- Go to GitHub Settings → Developer Settings → Personal Access Tokens
- Generate a new token with `read:user` and `repo` scopes
- Save it for use with the `--token` flag

## Usage

### View user statistics
```bash
python dmetrics.py stats USERNAME
```

With GitHub token:
```bash
python dmetrics.py stats USERNAME --token YOUR_GITHUB_TOKEN
```

### Compare two users
```bash
python dmetrics.py compare USER1 USER2
```

## Example Output

The tool provides:
- User profile information in a beautiful panel
- Repository and contribution statistics
- Language distribution visualization
- Contribution activity graphs
- Comparative analytics between users

## Requirements

- Python 3.7+
- Required packages (listed in requirements.txt)
- GitHub Personal Access Token (optional, but recommended)

## Tips

- Use a GitHub token to avoid API rate limits
- The comparison feature helps you benchmark against other developers
- Language distribution shows your tech stack diversity
- Activity graphs help track your GitHub engagement

## Note

This tool respects GitHub's API rate limits. Using a personal access token is recommended for the best experience. 