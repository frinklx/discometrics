#!/usr/bin/env python3

import os
import typer
import discord
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from dotenv import load_dotenv
import plotext as plt
from datetime import datetime, timedelta
import asyncio

# Initialize Typer app and Rich console
app = typer.Typer(help="DiscoMetrics - Discord User Analytics CLI")
console = Console()

# Load environment variables
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

class DiscordStats:
    def __init__(self):
        self.client = discord.Client(intents=discord.Intents.default())
        
    async def get_user_stats(self, username):
        try:
            await self.client.login(DISCORD_TOKEN)
            
            # Find user
            user = None
            for guild in self.client.guilds:
                for member in guild.members:
                    if f"{member.name}" == username:
                        user = member
                        break
                if user:
                    break
            
            if not user:
                console.print("[red]User not found![/red]")
                return None
            
            # Collect user stats
            stats = {
                "username": str(user),
                "id": user.id,
                "created_at": user.created_at,
                "status": str(user.status),
                "activities": [str(activity) for activity in user.activities],
                "roles": [role.name for role in user.roles if role.name != "@everyone"],
                "avatar_url": str(user.avatar.url) if user.avatar else None,
            }
            
            await self.client.close()
            return stats
            
        except Exception as e:
            console.print(f"[red]Error: {str(e)}[/red]")
            return None

def display_user_info(stats):
    if not stats:
        return
    
    # Create a rich panel with user information
    table = Table(show_header=False)
    table.add_row("Username", stats["username"])
    table.add_row("User ID", str(stats["id"]))
    table.add_row("Account Created", stats["created_at"].strftime("%Y-%m-%d %H:%M:%S"))
    table.add_row("Status", stats["status"])
    table.add_row("Roles", ", ".join(stats["roles"]) if stats["roles"] else "No roles")
    
    panel = Panel(table, title="User Information", border_style="blue")
    console.print(panel)
    
    # Display activity graph
    if stats["activities"]:
        console.print("\n[bold]Recent Activities:[/bold]")
        for activity in stats["activities"]:
            console.print(f"• {activity}")

def plot_account_age(created_at):
    days_old = (datetime.now() - created_at).days
    months = []
    activity = []
    
    # Generate sample activity data (you would replace this with real data)
    for i in range(6):
        date = datetime.now() - timedelta(days=30 * i)
        months.append(date.strftime("%b"))
        activity.append(int(days_old / (i + 1)))  # Sample data
    
    months.reverse()
    activity.reverse()
    
    # Plot activity graph
    plt.clear_data()
    plt.plot(months, activity)
    plt.title("Account Activity Over Time")
    plt.show()

@app.command()
def stats(username: str):
    """
    View Discord user statistics and analytics
    """
    console.print(f"\n[bold blue]🎮 DiscoMetrics[/bold blue] - Analyzing user: [bold]{username}[/bold]\n")
    
    stats_manager = DiscordStats()
    user_stats = asyncio.run(stats_manager.get_user_stats(username))
    
    if user_stats:
        display_user_info(user_stats)
        plot_account_age(user_stats["created_at"])

if __name__ == "__main__":
    app() 