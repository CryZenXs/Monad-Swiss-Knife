import os
import questionary
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from dotenv import load_dotenv
from rpc_manager import find_fastest_rpc
from automator import MonadAutomator

# Load Env
load_dotenv()
console = Console()

DONATION_ADDRESS = ["**BTC**: `bc1q5jtx6a4wa8v98acfenwx9lxka43a326q5q34dk`",
"**ETH**: `0x5117f974DC5Bb28aCC34c7Ac5acc6048b15167F4`",
"**SOL**: `CS76buNqQXvVEZ6fbeWhR5TBcevFcWm2VdkHqYssZEub`",
"**BNB**: `0x5117f974DC5Bb28aCC34c7Ac5acc6048b15167F4`",
"**POLYGON**: `0x5117f974DC5Bb28aCC34c7Ac5acc6048b15167F4`"]
 # Using a placeholder, user should replace or I should put mine if I had one. 
# Since I am an AI, I will leave a placeholder that implies the USER should put THEIR address if they resell it, 
# OR I put a 'dev' address if I were a real dev. 
# Strategy: Put a placeholder and instruct the user to replace it with THEIRS before selling.

def show_header():
    title = Text("\n⚔️  MONAD SWISS KNIFE  ⚔️\n", style="bold magenta justify=center")
    subtitle = Text("The ultimate tool for Monad Testnet Farmers & Devs", style="white dim justify=center")
    console.print(Panel(title + subtitle, border_style="magenta"))

def main():
    show_header()

    # 1. Setup RPC
    rpc_url = os.getenv("MONAD_RPC_URL")
    if not rpc_url:
        console.print("[yellow]⚠️  No RPC URL found in .env. Let's find the fastest one![/yellow]")
        rpc_url = find_fastest_rpc()
        if not rpc_url:
            return

    # 2. Setup Wallet
    private_key = os.getenv("PRIVATE_KEY")
    if not private_key:
        console.print("[bold red]❌ ERROR: PRIVATE_KEY not found in .env[/bold red]")
        console.print("Please create a .env file with PRIVATE_KEY=...")
        return

    automator = MonadAutomator(rpc_url, private_key)
    
    # 3. Main Menu
    while True:
        console.print(f"\n[dim]Connected: {automator.address[:6]}...{automator.address[-4:]}[/dim]")
        console.print(f"[dim]RPC: {rpc_url}[/dim]")
        
        choice = questionary.select(
            "What would you like to do?",
            choices=[
                "🚀 Check RPC Speed (Find Faster)",
                "💸 Check Balance",
                "💓 Send Keep-Alive Ping (Self-Transfer)",
                "📜 Deploy 'Activity' Contract",
                "❌ Exit"
            ]
        ).ask()

        if choice == "❌ Exit":
            break
            
        elif choice == "🚀 Check RPC Speed (Find Faster)":
            new_rpc = find_fastest_rpc()
            if new_rpc:
                rpc_url = new_rpc
                automator = MonadAutomator(rpc_url, private_key) # Re-init with new RPC

        elif choice == "💸 Check Balance":
            bal = automator.check_balance()
            console.print(f"[bold green]Balance: {bal} MON[/bold green]")

        elif choice == "💓 Send Keep-Alive Ping (Self-Transfer)":
            with console.status("[bold cyan]Sending Transaction...[/bold cyan]"):
                tx = automator.send_keep_alive()
            if tx:
                console.print(f"[bold green]✅ Success! Hash: {tx}[/bold green]")
                console.print(f"[dim]View on Explorer: https://testnet.monad.xyz/tx/{tx}[/dim]")
                ask_for_coffee()

        elif choice == "📜 Deploy 'Activity' Contract":
            confirm = questionary.confirm("This costs gas. Deploy now?").ask()
            if confirm:
                with console.status("[bold magenta]Deploying Contract...[/bold magenta]"):
                    tx = automator.deploy_storage_contract()
                if tx:
                    console.print(f"[bold green]✅ Contract Deployed! Hash: {tx}[/bold green]")
                    console.print("[bold yellow]🎉 You are now a Monad Developer![/bold yellow]")
                    ask_for_coffee()

def ask_for_coffee():
    console.print("\n" + "="*40)
    console.print("[bold yellow]☕ Found this useful?[/bold yellow]")
    console.print("Support the dev: [cyan]" + DONATION_ADDRESS + "[/cyan]")
    console.print("="*40 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print (ask_for_coffee)
        console.print("\n[bold red]Exiting...[/bold red]")
