import subprocess
import json
import os
import re
from typing import Dict, List, Optional, Tuple, Union

class DymensionCLI:
    """Wrapper for Dymension CLI commands"""
    
    def __init__(self, binary_path: str = "dymd"):
        """Initialize the DymensionCLI handler.
        
        Args:
            binary_path: Path to the dymd binary. Defaults to 'dymd' (assuming it's in PATH)
        """
        self.binary_path = binary_path
        self.binary_version = self._get_binary_version()
        
    def _get_binary_version(self) -> str:
        """Get the version of the dymd binary."""
        try:
            result = subprocess.run(
                [self.binary_path, "version"], 
                capture_output=True, 
                text=True,
                check=True
            )
            return result.stdout.strip()
        except (subprocess.SubprocessError, FileNotFoundError):
            return "Unknown"
    
    def run_command(self, args: List[str], parse_json: bool = False) -> Dict:
        """Run a dymd command with the given arguments.
        
        Args:
            args: List of command arguments
            parse_json: Whether to parse the output as JSON
            
        Returns:
            Dict containing command result with status, output, and error fields
        """
        try:
            cmd = [self.binary_path] + args
            print(f"Executing command: {' '.join(cmd)}")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                return {
                    "status": "error",
                    "output": "",
                    "error": result.stderr or f"Command failed with exit code {result.returncode}"
                }
            
            output = result.stdout.strip()
            
            if parse_json and output:
                try:
                    parsed_output = json.loads(output)
                    return {
                        "status": "success",
                        "output": parsed_output,
                        "error": ""
                    }
                except json.JSONDecodeError as e:
                    return {
                        "status": "error",
                        "output": output,
                        "error": f"Failed to parse JSON output: {str(e)}"
                    }
            
            return {
                "status": "success",
                "output": output,
                "error": ""
            }
            
        except Exception as e:
            return {
                "status": "error",
                "output": "",
                "error": str(e)
            }
    
    def get_status(self) -> Dict:
        """Get the status of the Dymension node."""
        return self.run_command(["status"], parse_json=True)
    
    def create_wallet(self, name: str) -> Dict:
        """Create a new wallet.
        
        Args:
            name: Name of the wallet
            
        Returns:
            Dict with wallet info and mnemonic
        """
        return self.run_command(["keys", "add", name, "--output", "json"], parse_json=True)
    
    def recover_wallet(self, name: str) -> Dict:
        """Recover a wallet from mnemonic.
        
        Args:
            name: Name to assign to the recovered wallet
            
        Returns:
            Dict with command output/status
        """
        # Note: This will prompt for mnemonic input interactively
        return self.run_command(["keys", "add", name, "--recover"])
    
    def list_wallets(self) -> Dict:
        """List all wallets."""
        return self.run_command(["keys", "list", "--output", "json"], parse_json=True)
    
    def get_balance(self, address: str) -> Dict:
        """Get account balance.
        
        Args:
            address: Account address
            
        Returns:
            Dict with balance info
        """
        return self.run_command(["query", "bank", "balances", address, "--output", "json"], parse_json=True)
    
    def transfer_tokens(self, from_wallet: str, to_address: str, amount: str, chain_id: str) -> Dict:
        """Transfer tokens between accounts.
        
        Args:
            from_wallet: Sender wallet name
            to_address: Recipient address
            amount: Amount with denomination (e.g., "10adym")
            chain_id: Chain ID (e.g., "dymension_1100-1")
            
        Returns:
            Dict with transaction result
        """
        return self.run_command([
            "tx", "bank", "send", 
            from_wallet, to_address, amount,
            "--chain-id", chain_id,
            "--gas", "auto",
            "--gas-adjustment", "1.3",
            "--output", "json",
            "-y"  # Auto-confirm
        ], parse_json=True)
    
    # RollApp specific commands
    
    def create_rollapp(self, rollapp_id: str, from_wallet: str, chain_id: str) -> Dict:
        """Create a new RollApp.
        
        Args:
            rollapp_id: RollApp identifier (e.g., "myrollapp_1234")
            from_wallet: Creator wallet name
            chain_id: Chain ID (e.g., "dymension_1100-1")
            
        Returns:
            Dict with RollApp creation result
        """
        return self.run_command([
            "tx", "rollapp", "create-rollapp", 
            rollapp_id,
            "--from", from_wallet,
            "--chain-id", chain_id,
            "--gas", "auto",
            "--output", "json",
            "-y"  # Auto-confirm
        ], parse_json=True)
    
    def register_sequencer(self, 
                          rollapp_id: str, 
                          sequencer_address: str, 
                          from_wallet: str,
                          dym_account: str,
                          pubkey: str,
                          chain_id: str) -> Dict:
        """Register a sequencer for a RollApp.
        
        Args:
            rollapp_id: RollApp identifier
            sequencer_address: Sequencer address
            from_wallet: Wallet name to sign transaction
            dym_account: Dymension account for fee payments
            pubkey: Sequencer pubkey
            chain_id: Chain ID
            
        Returns:
            Dict with sequencer registration result
        """
        return self.run_command([
            "tx", "sequencer", "register-sequencer",
            rollapp_id,
            sequencer_address,
            dym_account,
            pubkey,
            "--from", from_wallet,
            "--chain-id", chain_id,
            "--gas", "auto",
            "--output", "json",
            "-y"  # Auto-confirm
        ], parse_json=True)
    
    def query_rollapp(self, rollapp_id: str) -> Dict:
        """Query RollApp information.
        
        Args:
            rollapp_id: RollApp identifier
            
        Returns:
            Dict with RollApp info
        """
        return self.run_command([
            "query", "rollapp", "rollapp", 
            rollapp_id,
            "--output", "json"
        ], parse_json=True)
    
    def list_rollapp(self) -> Dict:
        """List all RollApps."""
        return self.run_command([
            "query", "rollapp", "rollapp-list",
            "--output", "json"
        ], parse_json=True)
    
    def query_sequencers(self, rollapp_id: str) -> Dict:
        """Query sequencers for a RollApp.
        
        Args:
            rollapp_id: RollApp identifier
            
        Returns:
            Dict with sequencer info
        """
        return self.run_command([
            "query", "sequencer", "sequencers", 
            rollapp_id,
            "--output", "json"
        ], parse_json=True)
    
    def claim_settlement(self, 
                        settlement_id: str, 
                        from_wallet: str,
                        chain_id: str) -> Dict:
        """Claim a settlement.
        
        Args:
            settlement_id: Settlement identifier
            from_wallet: Wallet name to sign transaction
            chain_id: Chain ID
            
        Returns:
            Dict with claim result
        """
        return self.run_command([
            "tx", "settlement", "claim-settlement",
            settlement_id,
            "--from", from_wallet,
            "--chain-id", chain_id,
            "--gas", "auto",
            "--output", "json",
            "-y"  # Auto-confirm
        ], parse_json=True)
    
    def submit_batch(self, 
                   rollapp_id: str,
                   from_wallet: str,
                   da_path: str,
                   height_start: int,
                   height_end: int,
                   chain_id: str) -> Dict:
        """Submit a batch of transactions.
        
        Args:
            rollapp_id: RollApp identifier
            from_wallet: Wallet name to sign transaction
            da_path: Data availability proof path
            height_start: Starting height
            height_end: Ending height
            chain_id: Chain ID
            
        Returns:
            Dict with batch submission result
        """
        return self.run_command([
            "tx", "sequencer", "submit-batch",
            rollapp_id,
            str(height_start),
            str(height_end),
            da_path,
            "--from", from_wallet,
            "--chain-id", chain_id,
            "--gas", "auto",
            "--output", "json",
            "-y"  # Auto-confirm
        ], parse_json=True)
    
    def update_whitelisted_relayers(self, 
                               addresses: List[str], 
                               from_wallet: str,
                               chain_id: str) -> Dict:
        """Update the list of whitelisted relayers for gas-free IBC transactions.
        
        Args:
            addresses: List of relayer addresses to whitelist
            from_wallet: Wallet name to sign transaction (must be the hub sequencer key)
            chain_id: Chain ID
            
        Returns:
            Dict with update result
        """
        addresses_str = ','.join(addresses)
        return self.run_command([
            "tx", "sequencer", "update-whitelisted-relayers",
            addresses_str,
            "--from", from_wallet,
            "--chain-id", chain_id,
            "--gas", "auto",
            "--output", "json",
            "-y"  # Auto-confirm
        ], parse_json=True)
    
    def parse_command(self, command_text: str) -> Dict:
        """Parse a command string provided by the user and execute the appropriate Dymension command.
        
        Args:
            command_text: Natural language command description
            
        Returns:
            Dict with command result
        """
        command_text = command_text.lower()
        
        # Wallet management
        if re.search(r"create (?:a )?(?:new )?wallet", command_text):
            match = re.search(r"(?:named|called|name) ['\"]*(\w+)['\"]*", command_text)
            if match:
                wallet_name = match.group(1)
                return self.create_wallet(wallet_name)
            else:
                return {"status": "error", "error": "Please specify a wallet name", "output": ""}
        
        elif re.search(r"recover (?:a )?wallet", command_text):
            match = re.search(r"(?:named|called|name) ['\"]*(\w+)['\"]*", command_text)
            if match:
                wallet_name = match.group(1)
                return self.recover_wallet(wallet_name)
            else:
                return {"status": "error", "error": "Please specify a wallet name", "output": ""}
        
        elif re.search(r"list (?:all )?wallets", command_text):
            return self.list_wallets()
        
        # Balance and transfers
        elif re.search(r"(?:check|get|show) (?:the )?balance", command_text):
            match = re.search(r"(?:for|of) (?:address )?['\"]*([a-zA-Z0-9]+)['\"]*", command_text)
            if match:
                address = match.group(1)
                return self.get_balance(address)
            else:
                return {"status": "error", "error": "Please specify an address", "output": ""}
        
        elif re.search(r"(?:transfer|send) (?:tokens|funds|money)", command_text):
            from_match = re.search(r"from ['\"]*(\w+)['\"]*", command_text)
            to_match = re.search(r"to ['\"]*([a-zA-Z0-9]+)['\"]*", command_text)
            amount_match = re.search(r"([0-9]+(?:\.[0-9]+)?)[\s]*([a-zA-Z]+)", command_text)
            chain_match = re.search(r"chain(?:-| )id ['\"]*([a-zA-Z0-9_-]+)['\"]*", command_text)
            
            if from_match and to_match and amount_match and chain_match:
                from_wallet = from_match.group(1)
                to_address = to_match.group(1)
                amount = amount_match.group(1) + amount_match.group(2)
                chain_id = chain_match.group(1)
                return self.transfer_tokens(from_wallet, to_address, amount, chain_id)
            else:
                missing = []
                if not from_match:
                    missing.append("sender wallet name")
                if not to_match:
                    missing.append("recipient address")
                if not amount_match:
                    missing.append("amount and denomination")
                if not chain_match:
                    missing.append("chain ID")
                
                return {
                    "status": "error", 
                    "error": f"Missing parameters: {', '.join(missing)}", 
                    "output": ""
                }
        
        # RollApp operations
        elif re.search(r"create (?:a )?(?:new )?rollapp", command_text):
            id_match = re.search(r"(?:id|named|called) ['\"]*([a-zA-Z0-9_]+)['\"]*", command_text)
            from_match = re.search(r"from ['\"]*(\w+)['\"]*", command_text)
            chain_match = re.search(r"chain(?:-| )id ['\"]*([a-zA-Z0-9_-]+)['\"]*", command_text)
            
            if id_match and from_match and chain_match:
                rollapp_id = id_match.group(1)
                from_wallet = from_match.group(1)
                chain_id = chain_match.group(1)
                return self.create_rollapp(rollapp_id, from_wallet, chain_id)
            else:
                missing = []
                if not id_match:
                    missing.append("RollApp ID")
                if not from_match:
                    missing.append("wallet name")
                if not chain_match:
                    missing.append("chain ID")
                
                return {
                    "status": "error", 
                    "error": f"Missing parameters: {', '.join(missing)}", 
                    "output": ""
                }
        
        elif re.search(r"register (?:a )?sequencer", command_text):
            rollapp_match = re.search(r"(?:for|to) rollapp ['\"]*([a-zA-Z0-9_]+)['\"]*", command_text)
            address_match = re.search(r"(?:with )?(?:address|addr) ['\"]*([a-zA-Z0-9]+)['\"]*", command_text)
            from_match = re.search(r"from ['\"]*(\w+)['\"]*", command_text)
            dym_match = re.search(r"dym account ['\"]*([a-zA-Z0-9]+)['\"]*", command_text)
            pubkey_match = re.search(r"pubkey ['\"]*([a-zA-Z0-9/+=]+)['\"]*", command_text)
            chain_match = re.search(r"chain(?:-| )id ['\"]*([a-zA-Z0-9_-]+)['\"]*", command_text)
            
            if rollapp_match and address_match and from_match and dym_match and pubkey_match and chain_match:
                return self.register_sequencer(
                    rollapp_match.group(1),
                    address_match.group(1),
                    from_match.group(1),
                    dym_match.group(1),
                    pubkey_match.group(1),
                    chain_match.group(1)
                )
            else:
                missing = []
                if not rollapp_match:
                    missing.append("RollApp ID")
                if not address_match:
                    missing.append("sequencer address")
                if not from_match:
                    missing.append("wallet name")
                if not dym_match:
                    missing.append("Dymension account")
                if not pubkey_match:
                    missing.append("public key")
                if not chain_match:
                    missing.append("chain ID")
                
                return {
                    "status": "error", 
                    "error": f"Missing parameters: {', '.join(missing)}", 
                    "output": ""
                }
        
        elif re.search(r"(?:show|get|list) (?:all )?rollapp(?:s)?", command_text):
            if "all" in command_text or "list" in command_text:
                return self.list_rollapp()
            else:
                match = re.search(r"(?:named|called|for|id) ['\"]*([a-zA-Z0-9_]+)['\"]*", command_text)
                if match:
                    rollapp_id = match.group(1)
                    return self.query_rollapp(rollapp_id)
                else:
                    return {"status": "error", "error": "Please specify a RollApp ID", "output": ""}
        
        elif re.search(r"(?:show|get|query) sequencers", command_text):
            match = re.search(r"(?:for|of) rollapp ['\"]*([a-zA-Z0-9_]+)['\"]*", command_text)
            if match:
                rollapp_id = match.group(1)
                return self.query_sequencers(rollapp_id)
            else:
                return {"status": "error", "error": "Please specify a RollApp ID", "output": ""}
        
        elif re.search(r"claim settlement", command_text):
            id_match = re.search(r"(?:with )?id ['\"]*([a-zA-Z0-9_-]+)['\"]*", command_text)
            from_match = re.search(r"from ['\"]*(\w+)['\"]*", command_text)
            chain_match = re.search(r"chain(?:-| )id ['\"]*([a-zA-Z0-9_-]+)['\"]*", command_text)
            
            if id_match and from_match and chain_match:
                return self.claim_settlement(
                    id_match.group(1),
                    from_match.group(1),
                    chain_match.group(1)
                )
            else:
                missing = []
                if not id_match:
                    missing.append("settlement ID")
                if not from_match:
                    missing.append("wallet name")
                if not chain_match:
                    missing.append("chain ID")
                
                return {
                    "status": "error", 
                    "error": f"Missing parameters: {', '.join(missing)}", 
                    "output": ""
                }
        
        elif re.search(r"submit batch", command_text):
            rollapp_match = re.search(r"(?:for) rollapp ['\"]*([a-zA-Z0-9_]+)['\"]*", command_text)
            from_match = re.search(r"from ['\"]*(\w+)['\"]*", command_text)
            da_match = re.search(r"da path ['\"]*([a-zA-Z0-9_/.-]+)['\"]*", command_text)
            height_match = re.search(r"height (?:from|start) ([0-9]+) (?:to|end) ([0-9]+)", command_text)
            chain_match = re.search(r"chain(?:-| )id ['\"]*([a-zA-Z0-9_-]+)['\"]*", command_text)
            
            if rollapp_match and from_match and da_match and height_match and chain_match:
                return self.submit_batch(
                    rollapp_match.group(1),
                    from_match.group(1),
                    da_match.group(1),
                    int(height_match.group(1)),
                    int(height_match.group(2)),
                    chain_match.group(1)
                )
            else:
                missing = []
                if not rollapp_match:
                    missing.append("RollApp ID")
                if not from_match:
                    missing.append("wallet name")
                if not da_match:
                    missing.append("DA path")
                if not height_match:
                    missing.append("height range")
                if not chain_match:
                    missing.append("chain ID")
                
                return {
                    "status": "error", 
                    "error": f"Missing parameters: {', '.join(missing)}", 
                    "output": ""
                }
        
        elif re.search(r"(?:get|check|show) status", command_text):
            return self.get_status()
        
        elif re.search(r"(?:help|show help|show commands|list commands)", command_text):
            return {
                "status": "success",
                "output": self.get_command_help(),
                "error": ""
            }
        
        elif re.search(r"(?:update|add|set) whitelisted relayers?", command_text):
            addresses_match = re.search(r"(?:address(?:es)?|addr) ['\"]*([a-zA-Z0-9,\s]+)['\"]*", command_text)
            from_match = re.search(r"from ['\"]*(\w+)['\"]*", command_text)
            chain_match = re.search(r"chain(?:-| )id ['\"]*([a-zA-Z0-9_-]+)['\"]*", command_text)
            
            if addresses_match and from_match and chain_match:
                # Parse addresses - could be comma-separated list
                addresses = [addr.strip() for addr in addresses_match.group(1).split(',')]
                return self.update_whitelisted_relayers(
                    addresses,
                    from_match.group(1),
                    chain_match.group(1)
                )
            else:
                missing = []
                if not addresses_match:
                    missing.append("relayer addresses")
                if not from_match:
                    missing.append("wallet name (must be sequencer key)")
                if not chain_match:
                    missing.append("chain ID")
                
                return {
                    "status": "error", 
                    "error": f"Missing parameters: {', '.join(missing)}", 
                    "output": ""
                }
            
        else:
            return {
                "status": "error",
                "output": "",
                "error": "Command not recognized. Please try a different command."
            }

    def get_command_help(self) -> Dict:
        """Get a list of available commands and example usage."""
        commands = [
            {
                "name": "Create wallet",
                "description": "Create a new wallet for use with Dymension",
                "example": "Create a new wallet named mywallet"
            },
            {
                "name": "Recover wallet",
                "description": "Recover a wallet using mnemonic phrase",
                "example": "Recover wallet named mywallet"
            },
            {
                "name": "List wallets",
                "description": "List all available wallets",
                "example": "List all wallets"
            },
            {
                "name": "Check balance",
                "description": "Check balance of an address",
                "example": "Check balance for address dym12345..."
            },
            {
                "name": "Transfer tokens",
                "description": "Transfer tokens to another address",
                "example": "Transfer 10adym from mywallet to dym12345... chain-id dymension_1100-1"
            },
            {
                "name": "Create RollApp",
                "description": "Create a new RollApp on Dymension",
                "example": "Create rollapp named myapp_1234 from mywallet chain-id dymension_1100-1"
            },
            {
                "name": "Register sequencer",
                "description": "Register a sequencer for a RollApp",
                "example": "Register sequencer for rollapp myapp_1234 with address dym456... from mywallet dym account dym456... pubkey ABC123... chain-id dymension_1100-1"
            },
            {
                "name": "Update whitelisted relayers",
                "description": "Update the list of whitelisted relayers for gas-free IBC transactions",
                "example": "Update whitelisted relayers address dym123456,dym654321 from sequencerkey chain-id dymension_1100-1"
            },
            {
                "name": "Query RollApp",
                "description": "Get information about a specific RollApp",
                "example": "Show rollapp with id myapp_1234"
            },
            {
                "name": "List RollApps",
                "description": "List all RollApps on the network",
                "example": "List all rollapps"
            },
            {
                "name": "Query sequencers",
                "description": "List sequencers for a RollApp",
                "example": "Show sequencers for rollapp myapp_1234"
            },
            {
                "name": "Claim settlement",
                "description": "Claim a settlement",
                "example": "Claim settlement with id s123 from mywallet chain-id dymension_1100-1"
            },
            {
                "name": "Submit batch",
                "description": "Submit a batch of transactions for a RollApp",
                "example": "Submit batch for rollapp myapp_1234 from mywallet da path /path/to/proof height start 100 end 200 chain-id dymension_1100-1"
            },
            {
                "name": "Check status",
                "description": "Check the status of the Dymension node",
                "example": "Get status"
            }
        ]
        
        return commands

# Helper function to format output
def format_output(result: Dict) -> str:
    """Format command result for display.
    
    Args:
        result: Command execution result
        
    Returns:
        Formatted string for display
    """
    if result["status"] == "error":
        return f"Error: {result['error']}"
    
    if isinstance(result["output"], dict):
        return json.dumps(result["output"], indent=2)
    
    return result["output"] 