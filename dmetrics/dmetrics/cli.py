#!/usr/bin/env python3

import os
import typer
import requests
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import track
from rich.style import Style
from rich.theme import Theme
from datetime import datetime, timedelta
import plotext as plt
from github import Github
from github.GithubException import GithubException
import pandas as pd
from termcolor import colored
import json
from typing import Optional, List
from pathlib import Path
import webbrowser

# Custom dark theme
custom_theme = Theme({
    "info": "cyan",
    "warning": "yellow",
    "error": "red",
    "success": "green",
    "title": Style(color="blue", bold=True),
    "metric": Style(color="magenta", bold=True),
    "value": Style(color="cyan"),
})

app = typer.Typer(help="🚀 dmetrics - Beautiful GitHub Analytics CLI")
console = Console(theme=custom_theme)

# Config management
CONFIG_DIR = Path.home() / ".config" / "dmetrics"
CONFIG_FILE = CONFIG_DIR / "config.json"

def load_config():
    if CONFIG_FILE.exists():
        return json.loads(CONFIG_FILE.read_text())
    return {}

def save_config(config):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(config, indent=2))

class GitHubMetrics:
    def __init__(self, username: str, token: Optional[str] = None):
        self.username = username
        self.token = token
        self.g = Github(token) if token else Github()
        self.base_url = "https://api.github.com"
        self.headers = {"Authorization": f"token {token}"} if token else {}

    def get_user_info(self):
        try:
            user = self.g.get_user(self.username)
            repos = list(user.get_repos())
            
            return {
                "name": user.name or self.username,
                "bio": user.bio,
                "location": user.location,
                "public_repos": user.public_repos,
                "followers": user.followers,
                "following": user.following,
                "created_at": user.created_at,
                "contributions": self._get_contributions(),
                "languages": self._get_language_stats(repos),
                "stars_received": self._get_stars_received(repos),
                "commit_activity": self._get_commit_activity(),
                "top_repos": self._get_top_repos(repos),
                "contribution_streak": self._get_contribution_streak(),
                "email": user.email,
                "company": user.company,
                "blog": user.blog,
                "twitter": user.twitter_username
            }
        except GithubException as e:
            console.print(f"[error]Error: {str(e)}[/error]")
            return None

    def _get_top_repos(self, repos, limit=5):
        sorted_repos = sorted(repos, key=lambda x: x.stargazers_count, reverse=True)
        return [{
            "name": repo.name,
            "stars": repo.stargazers_count,
            "forks": repo.forks_count,
            "language": repo.language,
            "description": repo.description
        } for repo in sorted_repos[:limit]]

    def _get_contributions(self):
        response = requests.get(
            f"https://github.com/users/{self.username}/contributions",
            headers=self.headers
        )
        return sum(1 for line in response.text.split('\n') if 'data-count' in line)

    def _get_contribution_streak(self):
        response = requests.get(
            f"https://github.com/users/{self.username}/contributions",
            headers=self.headers
        )
        # This is a simplified version - you might want to parse the actual SVG data
        return len([1 for line in response.text.split('\n') if 'data-count="0"' not in line and 'data-count' in line])

    def _get_language_stats(self, repos):
        languages = {}
        for repo in track(repos, description="[info]Analyzing repositories...[/info]"):
            if repo.language:
                languages[repo.language] = languages.get(repo.language, 0) + 1
        return languages

    def _get_stars_received(self, repos):
        return sum(repo.stargazers_count for repo in repos)

    def _get_commit_activity(self):
        activity = []
        now = datetime.now()
        for i in range(7):
            date = now - timedelta(days=i)
            activity.append({
                'date': date.strftime('%Y-%m-%d'),
                'commits': 0  # In a real implementation, we'd get actual commit counts
            })
        return activity

def display_user_info(stats):
    if not stats:
        return

    # User Profile Panel
    profile = Table(show_header=False, box=None)
    profile.add_row("[metric]Name[/metric]", f"[value]{stats['name']}[/value]")
    if stats["bio"]:
        profile.add_row("[metric]Bio[/metric]", f"[value]{stats['bio']}[/value]")
    if stats["location"]:
        profile.add_row("[metric]Location[/metric]", f"[value]{stats['location']}[/value]")
    if stats["email"]:
        profile.add_row("[metric]Email[/metric]", f"[value]{stats['email']}[/value]")
    if stats["company"]:
        profile.add_row("[metric]Company[/metric]", f"[value]{stats['company']}[/value]")
    if stats["blog"]:
        profile.add_row("[metric]Website[/metric]", f"[value]{stats['blog']}[/value]")
    if stats["twitter"]:
        profile.add_row("[metric]Twitter[/metric]", f"[value]@{stats['twitter']}[/value]")

    console.print(Panel(profile, title="👤 Profile", border_style="blue"))

    # Statistics Panel
    stats_table = Table(show_header=False)
    stats_table.add_row("[metric]Repositories[/metric]", f"[value]{stats['public_repos']}[/value]")
    stats_table.add_row("[metric]Followers[/metric]", f"[value]{stats['followers']}[/value]")
    stats_table.add_row("[metric]Following[/metric]", f"[value]{stats['following']}[/value]")
    stats_table.add_row("[metric]Total Stars[/metric]", f"[value]{stats['stars_received']}[/value]")
    stats_table.add_row("[metric]Contributions[/metric]", f"[value]{stats['contributions']}[/value]")
    stats_table.add_row("[metric]Contribution Streak[/metric]", f"[value]{stats['contribution_streak']} days[/value]")

    console.print(Panel(stats_table, title="📊 Statistics", border_style="green"))

    # Top Repositories
    if stats["top_repos"]:
        console.print("\n[title]🌟 Top Repositories[/title]")
        repo_table = Table(show_header=True)
        repo_table.add_column("Repository")
        repo_table.add_column("Stars")
        repo_table.add_column("Forks")
        repo_table.add_column("Language")
        
        for repo in stats["top_repos"]:
            repo_table.add_row(
                f"[value]{repo['name']}[/value]",
                f"[value]{repo['stars']}[/value]",
                f"[value]{repo['forks']}[/value]",
                f"[value]{repo['language'] or 'N/A'}[/value]"
            )
        console.print(repo_table)

    # Language Distribution
    if stats["languages"]:
        console.print("\n[title]🔤 Language Distribution[/title]")
        total = sum(stats["languages"].values())
        plt.clear_data()
        plt.theme('dark')
        plt.bar(
            list(stats["languages"].keys()),
            [count/total*100 for count in stats["languages"].values()],
            orientation="horizontal"
        )
        plt.title("Language Distribution (%)")
        plt.show()

    # Activity Graph
    console.print("\n[title]📈 Recent Activity[/title]")
    activity_data = stats["commit_activity"]
    plt.clear_data()
    plt.theme('dark')
    plt.date_form('Y-m-d')
    plt.plot([a['date'] for a in activity_data], 
            [a['commits'] for a in activity_data])
    plt.title("Commit Activity")
    plt.show()

@app.command()
def stats(
    username: str,
    token: Optional[str] = typer.Option(None, "--token", "-t", help="GitHub personal access token"),
    save_token: bool = typer.Option(False, "--save", help="Save the token for future use")
):
    """
    View GitHub user statistics and analytics
    """
    if not token:
        config = load_config()
        token = config.get("github_token")

    if save_token and token:
        save_config({"github_token": token})
        console.print("[success]Token saved successfully![/success]")

    console.print(f"\n[title]🚀 dmetrics[/title] - Analyzing user: [value]{username}[/value]\n")
    
    metrics = GitHubMetrics(username, token)
    user_stats = metrics.get_user_info()
    
    if user_stats:
        display_user_info(user_stats)

@app.command()
def compare(
    user1: str,
    user2: str,
    token: Optional[str] = typer.Option(None, "--token", "-t", help="GitHub personal access token")
):
    """
    Compare two GitHub users
    """
    if not token:
        config = load_config()
        token = config.get("github_token")

    console.print(f"\n[title]🚀 dmetrics[/title] - Comparing users: [value]{user1}[/value] vs [value]{user2}[/value]\n")
    
    metrics1 = GitHubMetrics(user1, token)
    metrics2 = GitHubMetrics(user2, token)
    
    stats1 = metrics1.get_user_info()
    stats2 = metrics2.get_user_info()
    
    if stats1 and stats2:
        table = Table(title="Comparison")
        table.add_column("Metric")
        table.add_column(user1)
        table.add_column(user2)
        
        metrics = [
            ("Repositories", "public_repos"),
            ("Followers", "followers"),
            ("Following", "following"),
            ("Stars", "stars_received"),
            ("Contributions", "contributions"),
            ("Streak", "contribution_streak")
        ]
        
        for label, key in metrics:
            table.add_row(
                f"[metric]{label}[/metric]",
                f"[value]{stats1[key]}[/value]",
                f"[value]{stats2[key]}[/value]"
            )
        
        console.print(table)

@app.command()
def config(
    token: Optional[str] = typer.Option(None, "--token", "-t", help="Set GitHub personal access token"),
    show: bool = typer.Option(False, "--show", help="Show current configuration"),
    clear: bool = typer.Option(False, "--clear", help="Clear saved configuration")
):
    """
    Configure dmetrics settings
    """
    if clear:
        if CONFIG_FILE.exists():
            CONFIG_FILE.unlink()
        console.print("[success]Configuration cleared successfully![/success]")
        return

    if show:
        config = load_config()
        if config:
            console.print(Panel(json.dumps(config, indent=2), title="Current Configuration"))
        else:
            console.print("[warning]No configuration found[/warning]")
        return

    if token:
        save_config({"github_token": token})
        console.print("[success]Token saved successfully![/success]")

@app.command()
def open(username: str):
    """
    Open user's GitHub profile in the default browser
    """
    url = f"https://github.com/{username}"
    webbrowser.open(url)
    console.print(f"[success]Opening {url} in your browser[/success]")

if __name__ == "__main__":
    app() 