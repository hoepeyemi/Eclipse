import subprocess
import json
import os
import re
import shutil
from typing import Dict, List, Optional, Tuple, Union

class DymensionCLI:
    """Wrapper for Dymension CLI commands"""
    
    def __init__(self):
        """Initialize the DymensionCLI handler."""
        # Find paths to binaries
        self.dymd_path = self._find_binary('dymd')
        self.roller_path = self._find_binary('roller')
        
    def _find_binary(self, binary_name: str) -> str:
        """Find the full path to a binary, checking common installation locations."""
        # First check if it's in PATH
        path = shutil.which(binary_name)
        if path:
            return path
            
        # Check common installation locations
        common_locations = [
            os.path.expanduser(f"~/.roller/bin/{binary_name}"),
            os.path.expanduser(f"~/go/bin/{binary_name}"),
            os.path.expanduser(f"~/dymension/bin/{binary_name}"),
            f"/usr/local/bin/{binary_name}",
            f"/usr/bin/{binary_name}"
        ]
        
        for location in common_locations:
            if os.path.exists(location) and os.access(location, os.X_OK):
                return location
                
        # Return the binary name and let the OS try to find it
        return binary_name
    
    def run_command(self, args: List[str], parse_json: bool = False) -> Dict:
        """Run a dymd command with the given arguments.
        
        Args:
            args: List of command arguments
            parse_json: Whether to parse the output as JSON
            
        Returns:
            Dict containing command result with status, output, and error fields
        """
        try:
            # Replace first element with full path if available
            if args and (args[0] == 'dymd' and self.dymd_path):
                args[0] = self.dymd_path
            elif args and (args[0] == 'roller' and self.roller_path):
                args[0] = self.roller_path
                
            cmd = args
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
            
        except FileNotFoundError as e:
            binary = args[0] if args else "unknown"
            installation_instructions = ""
            if binary == "dymd" or binary == self.dymd_path:
                installation_instructions = "\nTo install dymd: git clone https://github.com/dymensionxyz/dymension.git && cd dymension && git checkout v1.0.2-beta && make install"
            elif binary == "roller" or binary == self.roller_path:
                installation_instructions = "\nTo install roller: curl https://raw.githubusercontent.com/dymensionxyz/roller/main/install.sh | bash"
            
            return {
                "status": "error",
                "output": f"Error: {str(e)}{installation_instructions}",
                "error": str(e)
            }
        except Exception as e:
            return {
                "status": "error",
                "output": "",
                "error": str(e)
            }
    
    def get_binary_version(self, binary: str = "roller") -> Dict:
        """Get the version of the specified binary."""
        if binary == "roller":
            return self.run_command([binary, "version"])
        elif binary == "dymd":
            return self.run_command([binary, "version"])
        else:
            return {
                "status": "error",
                "output": f"Unsupported binary: {binary}",
                "raw_output": ""
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
    
    def simulate_install(self, what: str) -> Dict:
        """Simulate installation commands by providing instructions.
        
        Args:
            what: What to install ('essentials', 'go', 'roller', or 'all')
            
        Returns:
            Dict with installation instructions
        """
        instructions = {
            "essentials": {
                "command": "sudo apt install -y build-essential clang curl aria2 wget tar jq libssl-dev pkg-config make",
                "description": "Install essential dependencies for Dymension development",
                "notes": "This command installs the basic tools needed for blockchain development"
            },
            "go": {
                "command": "wget -O go.tar.gz https://golang.org/dl/go1.23.0.linux-amd64.tar.gz && sudo rm -rf /usr/local/go && sudo tar -C /usr/local -xzf go.tar.gz && rm go.tar.gz && echo 'export PATH=$PATH:/usr/local/go/bin:$HOME/go/bin' >> ~/.profile && source ~/.profile",
                "description": "Install Go programming language",
                "notes": "Go is required for compiling and running Dymension and Roller"
            },
            "roller": {
                "command": "curl https://raw.githubusercontent.com/dymensionxyz/roller/main/install.sh | bash",
                "description": "Install the Roller CLI",
                "notes": "Roller is the command-line tool for managing Dymension RollApps"
            }
        }
        
        response = {}
        
        if what == "all":
            response = {
                "status": "success",
                "output": "Installation Instructions for Dymension Environment Setup:\n\n"
            }
            
            for item, details in instructions.items():
                response["output"] += f"# {details['description']}\n{details['command']}\n\n"
            
            response["output"] += "\nPlease run these commands in your terminal to set up your environment."
            return response
        elif what in instructions:
            details = instructions[what]
            return {
                "status": "success",
                "output": f"# {details['description']}\n{details['command']}\n\n{details['notes']}"
            }
        else:
            return {
                "status": "error",
                "output": "",
                "error": f"Unknown installation target: {what}"
            }
            
    def translate_to_cli_command(self, command_text: str) -> Dict:
        """Translate natural language intent to actual CLI commands to run.
        
        Args:
            command_text: Natural language description of what the user wants to do
            
        Returns:
            Dict with suggested command and explanation
        """
        command_text = command_text.lower()
        
        # Installation commands
        if re.search(r"install (?:all|everything|full|complete)", command_text):
            return {
                "status": "success",
                "command": [
                    "# Install essential dependencies",
                    "sudo apt install -y build-essential clang curl aria2 wget tar jq libssl-dev pkg-config make",
                    "",
                    "# Install Go",
                    "cd $HOME",
                    "wget \"https://golang.org/dl/go1.23.0.linux-amd64.tar.gz\"",
                    "sudo rm -rf /usr/local/go",
                    "sudo tar -C /usr/local -xzf \"go1.23.0.linux-amd64.tar.gz\"",
                    "rm \"go1.23.0.linux-amd64.tar.gz\"",
                    "echo 'export PATH=$PATH:/usr/local/go/bin:$HOME/go/bin' >> ~/.profile",
                    "source ~/.profile",
                    "",
                    "# Install Roller CLI",
                    "curl https://raw.githubusercontent.com/dymensionxyz/roller/main/install.sh | bash"
                ],
                "explanation": "These commands will install all prerequisites for Dymension development, including system dependencies, Go programming language, and the Roller CLI."
            }
            
        elif re.search(r"install (?:essential|essentials|dependencies)", command_text):
            return {
                "status": "success",
                "command": [
                    "sudo apt install -y build-essential clang curl aria2 wget tar jq libssl-dev pkg-config make"
                ],
                "explanation": "This command installs the basic system dependencies required for Dymension development."
            }
            
        elif re.search(r"install (?:go|golang)", command_text):
            return {
                "status": "success",
                "command": [
                    "cd $HOME",
                    "wget \"https://golang.org/dl/go1.23.0.linux-amd64.tar.gz\"",
                    "sudo rm -rf /usr/local/go",
                    "sudo tar -C /usr/local -xzf \"go1.23.0.linux-amd64.tar.gz\"",
                    "rm \"go1.23.0.linux-amd64.tar.gz\"",
                    "echo 'export PATH=$PATH:/usr/local/go/bin:$HOME/go/bin' >> ~/.profile",
                    "source ~/.profile"
                ],
                "explanation": "These commands download and install Go 1.23.0, which is required for compiling and running Dymension and Roller."
            }
            
        elif re.search(r"install (?:roller|roller cli)", command_text):
            return {
                "status": "success",
                "command": [
                    "curl https://raw.githubusercontent.com/dymensionxyz/roller/main/install.sh | bash"
                ],
                "explanation": "This command installs the Roller CLI, which is used for managing Dymension RollApps."
            }
            
        elif re.search(r"install (?:dym|dymd|dymension)", command_text):
            return {
                "status": "success",
                "command": [
                    "git clone https://github.com/dymensionxyz/dymension.git",
                    "cd dymension",
                    "git checkout v1.0.2-beta",
                    "make install",
                    "dymd version  # Verify installation"
                ],
                "explanation": "These commands clone the Dymension repository, checkout the testnet version, and install the dymd binary."
            }
        
        # Version check
        elif re.search(r"(?:get|show|check) (?:roller|dymd)? ?version", command_text):
            if "dymd" in command_text:
                return {
                    "status": "success",
                    "command": ["dymd version"],
                    "explanation": "This command shows the installed version of the Dymension binary."
                }
            else:
                return {
                    "status": "success",
                    "command": ["roller version"],
                    "explanation": "This command shows the installed version of the Roller CLI."
                }
        
        # Wallet management
        elif re.search(r"create (?:a )?(?:new )?wallet", command_text):
            match = re.search(r"(?:named|called|name) ['\"]*(\w+)['\"]*", command_text)
            if match:
                wallet_name = match.group(1)
                return {
                    "status": "success",
                    "command": [f"dymd keys add {wallet_name}"],
                    "explanation": f"This command creates a new wallet named '{wallet_name}'. Make sure to save the mnemonic phrase that will be displayed."
                }
            else:
                return {
                    "status": "error",
                    "error": "Please specify a wallet name",
                    "suggestion": "Try: Create a new wallet named mywallet"
                }
        
        elif re.search(r"recover (?:a )?wallet", command_text):
            match = re.search(r"(?:named|called|name) ['\"]*(\w+)['\"]*", command_text)
            if match:
                wallet_name = match.group(1)
                return {
                    "status": "success",
                    "command": [f"dymd keys add {wallet_name} --recover"],
                    "explanation": f"This command allows you to recover wallet '{wallet_name}' using a mnemonic phrase. You will be prompted to enter your mnemonic."
                }
            else:
                return {
                    "status": "error",
                    "error": "Please specify a wallet name",
                    "suggestion": "Try: Recover wallet named mywallet"
                }
        
        elif re.search(r"list (?:all )?wallets", command_text):
            return {
                "status": "success",
                "command": ["dymd keys list"],
                "explanation": "This command lists all the wallets in your local keystore."
            }
        
        # Balance and transfers
        elif re.search(r"(?:check|get|show) (?:the )?balance", command_text):
            match = re.search(r"(?:for|of) (?:address )?['\"]*([a-zA-Z0-9]+)['\"]*", command_text)
            if match:
                address = match.group(1)
                return {
                    "status": "success",
                    "command": [f"dymd query bank balances {address}"],
                    "explanation": f"This command shows the token balances for address '{address}'."
                }
            else:
                return {
                    "status": "error",
                    "error": "Please specify an address",
                    "suggestion": "Try: Check balance for address dym12345..."
                }
        
        elif re.search(r"(?:transfer|send) (?:tokens|funds|money)", command_text):
            from_match = re.search(r"from ['\"]*(\w+)['\"]*", command_text)
            to_match = re.search(r"to ['\"]*([a-zA-Z0-9]+)['\"]*", command_text)
            amount_match = re.search(r"([0-9]+(?:\.[0-9]+)?)[\s]*([a-zA-Z]+)", command_text)
            chain_match = re.search(r"chain(?:-| )id ['\"]*([a-zA-Z0-9_-]+)['\"]*", command_text)
            
            if from_match and to_match and amount_match:
                from_wallet = from_match.group(1)
                to_address = to_match.group(1)
                amount = amount_match.group(1) + amount_match.group(2)
                chain_id = chain_match.group(1) if chain_match else "dymension_1100-1"
                
                return {
                    "status": "success",
                    "command": [f"dymd tx bank send {from_wallet} {to_address} {amount} --chain-id {chain_id} --gas auto -y"],
                    "explanation": f"This command transfers {amount} from wallet '{from_wallet}' to address '{to_address}'."
                }
            else:
                missing = []
                if not from_match:
                    missing.append("sender wallet name")
                if not to_match:
                    missing.append("recipient address")
                if not amount_match:
                    missing.append("amount and denomination")
                
                return {
                    "status": "error", 
                    "error": f"Missing parameters: {', '.join(missing)}", 
                    "suggestion": "Try: Transfer 10adym from mywallet to dym12345... chain-id dymension_1100-1"
                }
        
        # RollApp operations
        elif re.search(r"(?:create|init) (?:a )?(?:new )?rollapp", command_text):
            match_name = re.search(r"(?:named|called|name) ['\"]*([a-zA-Z0-9_-]+)['\"]*", command_text)
            match_denom = re.search(r"(?:token|denom) ['\"]*([a-zA-Z0-9]+)['\"]*", command_text)
            
            if match_name and match_denom:
                rollapp_name = match_name.group(1)
                token_denom = match_denom.group(1)
                evm_flag = "--evm" if "evm" in command_text else ""
                
                return {
                    "status": "success",
                    "command": [f"roller create {rollapp_name} {token_denom} {evm_flag}"],
                    "explanation": f"This command initializes a new RollApp named '{rollapp_name}' with token denomination '{token_denom}'{' using EVM' if evm_flag else ''}."
                }
            else:
                missing = []
                if not match_name:
                    missing.append("RollApp name")
                if not match_denom:
                    missing.append("token denomination")
                
                return {
                    "status": "error", 
                    "error": f"Missing parameters: {', '.join(missing)}", 
                    "suggestion": "Try: Create a new rollapp named myrollapp token mydenom"
                }
                
        elif re.search(r"(?:get|show|list) (?:all )?commands", command_text) or re.search(r"(?:help|command list)", command_text):
            return {
                "status": "success",
                "command": ["roller --help", "dymd --help"],
                "explanation": "These commands show the available commands for Roller and Dymension CLIs."
            }
            
        elif re.search(r"register (?:a )?rollapp", command_text):
            rollapp_match = re.search(r"(?:named|called|name|id) ['\"]*([a-zA-Z0-9_-]+)['\"]*", command_text)
            from_match = re.search(r"(?:from|with) (?:wallet )?['\"]*(\w+)['\"]*", command_text)
            
            if rollapp_match and from_match:
                rollapp_id = rollapp_match.group(1)
                from_wallet = from_match.group(1)
                
                return {
                    "status": "success",
                    "command": [f"roller register {rollapp_id} --from {from_wallet}"],
                    "explanation": f"This command registers the RollApp '{rollapp_id}' on the Dymension hub using wallet '{from_wallet}'."
                }
            else:
                missing = []
                if not rollapp_match:
                    missing.append("RollApp ID")
                if not from_match:
                    missing.append("wallet name")
                
                return {
                    "status": "error", 
                    "error": f"Missing parameters: {', '.join(missing)}", 
                    "suggestion": "Try: Register rollapp myrollapp from mywallet"
                }
                
        elif re.search(r"start (?:a )?rollapp", command_text):
            rollapp_match = re.search(r"(?:named|called|name|id) ['\"]*([a-zA-Z0-9_-]+)['\"]*", command_text)
            
            if rollapp_match:
                rollapp_id = rollapp_match.group(1)
                
                return {
                    "status": "success",
                    "command": [f"roller start {rollapp_id}"],
                    "explanation": f"This command starts the RollApp '{rollapp_id}'."
                }
            else:
                return {
                    "status": "error", 
                    "error": "Missing RollApp ID", 
                    "suggestion": "Try: Start rollapp myrollapp"
                }
                
        elif re.search(r"stop (?:a )?rollapp", command_text):
            rollapp_match = re.search(r"(?:named|called|name|id) ['\"]*([a-zA-Z0-9_-]+)['\"]*", command_text)
            
            if rollapp_match:
                rollapp_id = rollapp_match.group(1)
                
                return {
                    "status": "success",
                    "command": [f"roller stop {rollapp_id}"],
                    "explanation": f"This command stops the RollApp '{rollapp_id}'."
                }
            else:
                return {
                    "status": "error", 
                    "error": "Missing RollApp ID", 
                    "suggestion": "Try: Stop rollapp myrollapp"
                }
                
        elif re.search(r"(?:get|show|check) status", command_text):
            rollapp_match = re.search(r"(?:for|of) (?:rollapp )?['\"]*([a-zA-Z0-9_-]+)['\"]*", command_text)
            
            if rollapp_match:
                rollapp_id = rollapp_match.group(1)
                return {
                    "status": "success",
                    "command": [f"roller status {rollapp_id}"],
                    "explanation": f"This command shows the status of RollApp '{rollapp_id}'."
                }
            else:
                return {
                    "status": "success",
                    "command": ["roller status"],
                    "explanation": "This command shows the status of your RollApp."
                }
                
        elif re.search(r"add (?:a )?relayer", command_text):
            rollapp_match = re.search(r"(?:for|to) (?:rollapp )?['\"]*([a-zA-Z0-9_-]+)['\"]*", command_text)
            wallet_match = re.search(r"(?:wallet|address) ['\"]*([a-zA-Z0-9]+)['\"]*", command_text)
            
            if rollapp_match and wallet_match:
                rollapp_id = rollapp_match.group(1)
                wallet = wallet_match.group(1)
                
                return {
                    "status": "success",
                    "command": [f"roller relayer whitelist {rollapp_id} --add {wallet}"],
                    "explanation": f"This command adds wallet '{wallet}' as a whitelisted relayer for RollApp '{rollapp_id}'."
                }
            else:
                missing = []
                if not rollapp_match:
                    missing.append("RollApp ID")
                if not wallet_match:
                    missing.append("wallet address")
                
                return {
                    "status": "error", 
                    "error": f"Missing parameters: {', '.join(missing)}", 
                    "suggestion": "Try: Add relayer dym123... to rollapp myrollapp"
                }
                
        elif re.search(r"register (?:a )?sequencer", command_text):
            rollapp_match = re.search(r"(?:for|to) (?:rollapp )?['\"]*([a-zA-Z0-9_-]+)['\"]*", command_text)
            from_match = re.search(r"(?:from|with) (?:wallet )?['\"]*(\w+)['\"]*", command_text)
            
            if rollapp_match and from_match:
                rollapp_id = rollapp_match.group(1)
                from_wallet = from_match.group(1)
                
                return {
                    "status": "success",
                    "command": [f"roller sequencer register {rollapp_id} --from {from_wallet}"],
                    "explanation": f"This command registers a sequencer for RollApp '{rollapp_id}' using wallet '{from_wallet}'."
                }
            else:
                missing = []
                if not rollapp_match:
                    missing.append("RollApp ID")
                if not from_match:
                    missing.append("wallet name")
                
                return {
                    "status": "error", 
                    "error": f"Missing parameters: {', '.join(missing)}", 
                    "suggestion": "Try: Register sequencer for rollapp myrollapp from mywallet"
                }
        
        else:
            # Return help if command isn't recognized
            return {
                "status": "error",
                "error": "Command not recognized. Please try a different command format.",
                "suggestions": [
                    "Install Roller CLI",
                    "Create a new wallet named mywallet", 
                    "Create a new rollapp named myrollapp token mydenom",
                    "Register rollapp myrollapp from mywallet",
                    "Start rollapp myrollapp",
                    "Check status of rollapp myrollapp",
                    "Help"
                ]
            }

    def parse_command(self, command_text: str) -> Dict:
        """Parse a command string provided by the user and return appropriate CLI commands.
        
        Args:
            command_text: Natural language command description
            
        Returns:
            Dict with command result
        """
        # Instead of trying to execute the command, translate it to CLI commands
        translation = self.translate_to_cli_command(command_text)
        
        if translation["status"] == "success":
            # Format the command output for display
            if isinstance(translation["command"], list):
                command_str = "\n".join(translation["command"])
            else:
                command_str = translation["command"]
                
            return {
                "status": "success",
                "output": f"# CLI Command(s) to execute:\n\n{command_str}\n\n{translation.get('explanation', '')}",
                "raw_output": command_str,
                "error": ""
            }
        else:
            # Return error with suggestions
            suggestions = translation.get("suggestions", [])
            suggestion_text = ""
            if suggestions:
                suggestion_text = "\n\nTry one of these commands:\n- " + "\n- ".join(suggestions)
            
            return {
                "status": "error",
                "output": f"Error: {translation.get('error', 'Unknown error')}{suggestion_text}",
                "error": translation.get('error', 'Unknown error'),
                "suggestion": translation.get('suggestion', '')
            }

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