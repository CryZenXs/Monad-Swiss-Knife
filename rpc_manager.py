import time
import requests
from rich.console import Console

console = Console()

# List of known Monad Testnet RPCs (including public and potential private ones user might add)
# Note: Since Monad Testnet is new, this list should be updated with actual active endpoints.
DEFAULT_RPCS = [
    "https://testnet-rpc.monad.xyz/",
    "https://rpc-testnet.monadinfra.com", 
    "https://rpc.ankr.com/monad_testnet",
    "https://monad-testnet.drpc.org",
    "https://rpc.testnet.monad.xyz",
    "https://monad-testnet.g.alchemy.com/v2/demo",
    "https://monad-testnet.rpc.thirdweb.com",
]

def check_rpc_latency(rpc_url):
    """
    Pings an RPC URL and returns the latency in milliseconds.
    Returns float('inf') if reachable but error, or raises exception if connection fails.
    """
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_blockNumber",
        "params": [],
        "id": 1
    }
    
    try:
        start_time = time.time()
        response = requests.post(rpc_url, json=payload, timeout=3)
        end_time = time.time()
        
        if response.status_code == 200 and 'result' in response.json():
            latency = (end_time - start_time) * 1000
            return latency
        else:
            return float('inf')
    except Exception:
        return float('inf')

def find_fastest_rpc():
    """
    Iterates through default RPCs and returns the one with the lowest latency.
    """
    console.print("[bold cyan]🔄 Testing RPC Latency...[/bold cyan]")
    
    fastest_rpc = None
    min_latency = float('inf')
    
    results = []

    for rpc in DEFAULT_RPCS:
        latency = check_rpc_latency(rpc)
        if latency != float('inf'):
            color = "green" if latency < 200 else "yellow"
            console.print(f"  • {rpc}: [{color}]{latency:.2f} ms[/{color}]")
            results.append((rpc, latency))
            
            if latency < min_latency:
                min_latency = latency
                fastest_rpc = rpc
        else:
            console.print(f"  • {rpc}: [red]Timeout/Error[/red]")

    if fastest_rpc:
        console.print(f"\n[bold green]🚀 Fastest RPC found: {fastest_rpc} ({min_latency:.2f} ms)[/bold green]")
        return fastest_rpc
    else:
        console.print("\n[bold red]❌ No working RPCs found. Check your internet connection.[/bold red]")
        return None
