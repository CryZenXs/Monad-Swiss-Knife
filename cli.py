import os
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt, Confirm
from dotenv import load_dotenv
from rpc_manager import find_fastest_rpc
from automator import MonadAutomator

# Load Env
load_dotenv()
console = Console()

DONATION_ADDRESS = ["**BTC**: `bc1qf0pmej7pwsn452t86rwhp2zd2evnm08pd4l839`",
"**ETH**: `0xEf972A58dBFD48F49B133Ba7992d7a23911B40E2`",
"**SOL**: `w4qG4YZEVgNa2CCJJSoUcUew1mYBHbwo2eDq4yw19gd`",
"**BNB**: `0xEf972A58dBFD48F49B133Ba7992d7a23911B40E2`",
"**POLYGON**: `0xEf972A58dBFD48F49B133Ba7992d7a23911B40E2`"]

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
        
        # Using Rich Prompt instead of Questionary
        console.print("\n[bold]Options:[/bold]")
        console.print("1. 🚀 Check RPC Speed")
        console.print("2. 💸 Check Balance")
        console.print("3. 💓 Send Keep-Alive Ping")
        console.print("4. 📜 Deploy Contract")
        console.print("5. 🔄 Wrap MON (DeFi Activity) [New!]")
        console.print("6. 🎨 Mint 'Early Adopter' NFT [New!]")
        console.print("7. ❌ Exit")
        
        choice = Prompt.ask("Choose an option", choices=["1", "2", "3", "4", "5", "6", "7"], default="1")

        if choice == "7":
            break
            
        elif choice == "1":
            new_rpc = find_fastest_rpc()
            if new_rpc:
                rpc_url = new_rpc
                automator = MonadAutomator(rpc_url, private_key)

        elif choice == "2":
            bal = automator.check_balance()
            console.print(f"[bold green]Balance: {bal} MON[/bold green]")

        elif choice == "3":
            with console.status("[bold cyan]Sending Transaction...[/bold cyan]"):
                tx = automator.send_keep_alive()
            if tx:
                console.print(f"[bold green]✅ Success! Hash: {tx}[/bold green]")
                console.print(f"[dim]View on Explorer: https://testnet.monad.xyz/tx/{tx}[/dim]")
                ask_for_coffee()

        elif choice == "4":
            if Confirm.ask("This costs gas. Deploy now?"):
                with console.status("[bold magenta]Deploying Contract...[/bold magenta]"):
                    tx = automator.deploy_storage_contract()
                if tx:
                    console.print(f"[bold green]✅ Contract Deployed! Hash: {tx}[/bold green]")
                    console.print("[bold yellow]🎉 You are now a Monad Developer![/bold yellow]")
                    ask_for_coffee()

        elif choice == "5":
            amount = Prompt.ask("Amount to wrap (MON)", default="0.001")
            with console.status("[bold blue]Wrapping MON...[/bold blue]"):
                tx = automator.wrap_mon(float(amount))
            if tx:
                console.print(f"[bold green]✅ DeFi Activity Recorded! Hash: {tx}[/bold green]")
                ask_for_coffee()

        elif choice == "6":
             if Confirm.ask("Minting costs gas. Proceed?"):
                with console.status("[bold purple]Minting NFT...[/bold purple]"):
                    tx = automator.deploy_nft()
                if tx:
                    console.print(f"[bold green]✅ NFT Minted! Hash: {tx}[/bold green]")
                    ask_for_coffee()

def ask_for_coffee():
    console.print("\n" + "="*40)
    console.print("[bold yellow]☕ Found this useful?[/bold yellow]")
    console.print("Support the dev:")
    for addr in DONATION_ADDRESS:
        console.print(f"[cyan]{addr}[/cyan]")
    console.print("="*40 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        ask_for_coffee()
        console.print("\n[bold red]Exiting...[/bold red]")
