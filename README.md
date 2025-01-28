# dmetrics 🚀

A beautiful dark-mode command-line tool for viewing GitHub user statistics and analytics with stunning terminal visualizations.

## Features

- 👤 Detailed GitHub user profile information
- 📊 Repository statistics and analytics
- 🔤 Programming language distribution with dark mode graphs
- 📈 Contribution activity visualization
- ⭐ Star counts and statistics
- 🔄 User comparison functionality
- 🎨 Beautiful dark-mode terminal UI
- 🌟 Top repositories showcase
- 📅 Contribution streak tracking
- 🔗 Social links and contact information
- ⚙️ Configuration management
- 🌐 Quick profile opening in browser

## Installation

### Using pip (Recommended)
```bash
pip install .
```

The `dmetrics` command will be available globally in your terminal.

### Manual Installation
1. Clone this repository:
```bash
git clone <repository-url>
cd dmetrics
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

Set up your GitHub token (recommended to avoid API rate limits):

```bash
dmetrics config --token YOUR_GITHUB_TOKEN
```

View current configuration:
```bash
dmetrics config --show
```

Clear configuration:
```bash
dmetrics config --clear
```

## Usage

### View user statistics
```bash
dmetrics stats USERNAME
```

With a one-time token:
```bash
dmetrics stats USERNAME --token YOUR_GITHUB_TOKEN
```

Save token while viewing stats:
```bash
dmetrics stats USERNAME --token YOUR_GITHUB_TOKEN --save
```

### Compare two users
```bash
dmetrics compare USER1 USER2
```

### Open user's GitHub profile
```bash
dmetrics open USERNAME
```

## Example Output

The tool provides:
- User profile information in a sleek dark panel
- Repository and contribution statistics
- Language distribution visualization
- Contribution activity graphs
- Top repositories showcase
- Comparative analytics between users
- Contribution streak information

## Features in Detail

### Profile Information
- Name and bio
- Location and company
- Email and website
- Twitter username
- Contribution statistics

### Repository Analytics
- Total public repositories
- Star count across all repos
- Top repositories by stars
- Fork counts
- Primary languages

### Activity Metrics
- Contribution count
- Current streak
- Recent activity graph
- Language distribution

### Comparison Features
- Side-by-side user comparison
- Metric-by-metric analysis
- Visual differentiation

## Requirements

- Python 3.7+
- Required packages (listed in requirements.txt)
- GitHub Personal Access Token (optional, but recommended)

## Tips

- Use a GitHub token to avoid API rate limits
- Save your token using the config command for convenience
- The comparison feature helps you benchmark against other developers
- Language distribution shows your tech stack diversity
- Activity graphs help track your GitHub engagement

## Note

This tool respects GitHub's API rate limits. Using a personal access token is recommended for the best experience. 