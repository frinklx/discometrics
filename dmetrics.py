#!/usr/bin/env python3

import os
import typer
import requests
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import track
from datetime import datetime, timedelta
import plotext as plt
from github import Github
from github.GithubException import GithubException
import pandas as pd
from termcolor import colored
import json
from typing import Optional

# Initialize Typer app and Rich console
app = typer.Typer(help="🚀 dmetrics - Beautiful GitHub Analytics CLI")
console = Console()

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
            return {
                "name": user.name or self.username,
                "bio": user.bio,
                "location": user.location,
                "public_repos": user.public_repos,
                "followers": user.followers,
                "following": user.following,
                "created_at": user.created_at,
                "contributions": self._get_contributions(),
                "languages": self._get_language_stats(),
                "stars_received": self._get_stars_received(),
                "commit_activity": self._get_commit_activity()
            }
        except GithubException as e:
            console.print(f"[red]Error: {str(e)}[/red]")
            return None

    def _get_contributions(self):
        response = requests.get(
            f"https://github.com/users/{self.username}/contributions",
            headers=self.headers
        )
        # Parse contribution data (simplified for example)
        return sum(1 for line in response.text.split('\n') if 'data-count' in line)

    def _get_language_stats(self):
        languages = {}
        for repo in track(self.g.get_user(self.username).get_repos(), description="Analyzing repositories..."):
            if repo.language:
                languages[repo.language] = languages.get(repo.language, 0) + 1
        return languages

    def _get_stars_received(self):
        stars = 0
        for repo in self.g.get_user(self.username).get_repos():
            stars += repo.stargazers_count
        return stars

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
    profile.add_row("Name", stats["name"])
    if stats["bio"]:
        profile.add_row("Bio", stats["bio"])
    if stats["location"]:
        profile.add_row("Location", stats["location"])

    console.print(Panel(profile, title="👤 Profile", border_style="blue"))

    # Statistics Panel
    stats_table = Table(show_header=False)
    stats_table.add_row("Repositories", str(stats["public_repos"]))
    stats_table.add_row("Followers", str(stats["followers"]))
    stats_table.add_row("Following", str(stats["following"]))
    stats_table.add_row("Total Stars", str(stats["stars_received"]))
    stats_table.add_row("Contributions", str(stats["contributions"]))

    console.print(Panel(stats_table, title="📊 Statistics", border_style="green"))

    # Language Distribution
    if stats["languages"]:
        console.print("\n[bold]🔤 Language Distribution[/bold]")
        total = sum(stats["languages"].values())
        plt.clear_data()
        plt.bar(
            list(stats["languages"].keys()),
            [count/total*100 for count in stats["languages"].values()],
            orientation="horizontal"
        )
        plt.title("Language Distribution (%)")
        plt.show()

    # Activity Graph
    console.print("\n[bold]📈 Recent Activity[/bold]")
    activity_data = stats["commit_activity"]
    plt.clear_data()
    plt.date_form('Y-m-d')
    plt.plot([a['date'] for a in activity_data], 
            [a['commits'] for a in activity_data])
    plt.title("Commit Activity")
    plt.show()

@app.command()
def stats(
    username: str,
    token: Optional[str] = typer.Option(None, "--token", "-t", help="GitHub personal access token")
):
    """
    View GitHub user statistics and analytics
    """
    console.print(f"\n[bold blue]🚀 dmetrics[/bold blue] - Analyzing GitHub user: [bold]{username}[/bold]\n")
    
    metrics = GitHubMetrics(username, token)
    user_stats = metrics.get_user_info()
    
    if user_stats:
        display_user_info(user_stats)

@app.command()
def compare(user1: str, user2: str):
    """
    Compare two GitHub users
    """
    console.print(f"\n[bold blue]🚀 dmetrics[/bold blue] - Comparing users: [bold]{user1}[/bold] vs [bold]{user2}[/bold]\n")
    
    metrics1 = GitHubMetrics(user1)
    metrics2 = GitHubMetrics(user2)
    
    stats1 = metrics1.get_user_info()
    stats2 = metrics2.get_user_info()
    
    if stats1 and stats2:
        # Create comparison table
        table = Table(title="Comparison")
        table.add_column("Metric")
        table.add_column(user1)
        table.add_column(user2)
        
        metrics = [
            ("Repositories", "public_repos"),
            ("Followers", "followers"),
            ("Following", "following"),
            ("Stars", "stars_received"),
            ("Contributions", "contributions")
        ]
        
        for label, key in metrics:
            table.add_row(
                label,
                str(stats1[key]),
                str(stats2[key])
            )
        
        console.print(table)

if __name__ == "__main__":
    app() 