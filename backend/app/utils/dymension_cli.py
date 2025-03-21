import subprocess
import json
import os
import re
import shutil
from typing import Dict, List, Optional, Tuple, Union
import platform

class DymensionCLI:
    """Wrapper for Dymension CLI commands"""
    
    def __init__(self):
        """Initialize the DymensionCLI handler."""
        # Find paths to binaries
        self.dymd_path = self._find_binary('dymd')
        self.roller_path = self._find_binary('roller')
        
        # Initialize OS detection
        self.os = platform.system()  # 'Windows', 'Linux', or 'Darwin' (macOS)
        self.is_windows = self.os == 'Windows'
        self.is_mac = self.os == 'Darwin'
        self.is_linux = self.os == 'Linux'
        
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
    
    def simulate_install(self, what="all"):
        """Simulate installation of different components based on OS"""
        what = what.lower()

        if self.is_windows:
            if what == "essentials":
                return {
                    "status": "success",
                    "output": "# Install essential dependencies (Windows)\n"
                             "# Install Chocolatey first (if not installed)\n"
                             "@powershell -NoProfile -ExecutionPolicy Bypass -Command \"iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))\"\n\n"
                             "# Install dependencies using Chocolatey\n"
                             "choco install -y git wget curl jq",
                    "error": ""
                }
            elif what == "go":
                return {
                    "status": "success", 
                    "output": "# Install Go (Windows)\n"
                              "# Download Go installer\n"
                              "wget -O go_installer.msi https://golang.org/dl/go1.23.0.windows-amd64.msi\n\n"
                              "# Run installer\n"
                              "start /wait go_installer.msi /quiet\n\n"
                              "# Add to PATH (may require restarting terminal)\n"
                              "setx PATH \"%PATH%;C:\\Go\\bin;%USERPROFILE%\\go\\bin\" -m\n\n"
                              "# Verify installation\n"
                              "go version",
                    "error": ""
                }
            elif what == "roller":
                return {
                    "status": "success",
                    "output": "# Install Roller CLI (Windows)\n"
                             "# Download and run the Windows installer script\n"
                             "curl -sSL https://raw.githubusercontent.com/dymensionxyz/roller/main/install-windows.ps1 -o install-roller.ps1\n"
                             "powershell -ExecutionPolicy Bypass -File .\\install-roller.ps1\n\n"
                             "# Add to PATH if needed\n"
                             "setx PATH \"%PATH%;%USERPROFILE%\\.roller\\bin\" -m\n\n"
                             "# Verify installation\n"
                             "roller version",
                    "error": ""
                }
            else:  # all
                return {
                    "status": "success",
                    "output": "# Complete Dymension Setup Script (Windows)\n\n"
                             "# Install Chocolatey (if not installed)\n"
                             "@powershell -NoProfile -ExecutionPolicy Bypass -Command \"iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))\"\n\n"
                             "# Install dependencies\n"
                             "choco install -y git wget curl jq\n\n"
                             "# Install Go\n"
                             "wget -O go_installer.msi https://golang.org/dl/go1.23.0.windows-amd64.msi\n"
                             "start /wait go_installer.msi /quiet\n"
                             "setx PATH \"%PATH%;C:\\Go\\bin;%USERPROFILE%\\go\\bin\" -m\n\n"
                             "# Install Roller CLI\n"
                             "curl -sSL https://raw.githubusercontent.com/dymensionxyz/roller/main/install-windows.ps1 -o install-roller.ps1\n"
                             "powershell -ExecutionPolicy Bypass -File .\\install-roller.ps1\n\n"
                             "# Add Roller to PATH\n"
                             "setx PATH \"%PATH%;%USERPROFILE%\\.roller\\bin\" -m\n\n"
                             "# Install Dymension\n"
                             "git clone https://github.com/dymensionxyz/dymension.git\n"
                             "cd dymension\n"
                             "git checkout v1.0.2-beta\n"
                             "go build -o %USERPROFILE%\\go\\bin\\dymd.exe ./cmd/dymd\n\n"
                             "# Verify installation\n"
                             "roller version\n"
                             "dymd version\n\n"
                             "# Note: After installation, restart your terminal to apply PATH changes\n",
                    "error": ""
                }
        else:  # macOS or Linux
            if what == "essentials":
                if self.is_mac:
                    return {
                        "status": "success",
                        "output": "# Install essential dependencies (macOS)\n"
                                "# Install Homebrew if not installed\n"
                                "/bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"\n\n"
                                "# Install dependencies\n"
                                "brew install git wget curl jq",
                        "error": ""
                    }
                else:  # Linux
                    return {
                        "status": "success",
                        "output": "# Install essential dependencies (Linux)\n"
                                "sudo apt update\n"
                                "sudo apt install -y build-essential git wget curl jq",
                        "error": ""
                    }
            elif what == "go":
                return {
                    "status": "success", 
                    "output": "# Install Go\n"
                              "wget -O go.tar.gz https://golang.org/dl/go1.23.0.linux-amd64.tar.gz\n"
                              "sudo rm -rf /usr/local/go\n"
                              "sudo tar -C /usr/local -xzf go.tar.gz\n"
                              "rm go.tar.gz\n"
                              "echo 'export PATH=$PATH:/usr/local/go/bin:$HOME/go/bin' >> ~/.bashrc\n"
                              "source ~/.bashrc\n"
                              "go version",
                    "error": ""
                }
            elif what == "roller":
                return {
                    "status": "success",
                    "output": "# Install Roller CLI\n"
                             "curl https://raw.githubusercontent.com/dymensionxyz/roller/main/install.sh | bash\n"
                             "# Verify installation\n"
                             "roller version",
                    "error": ""
                }
            else:  # all
                base_cmd = "# Install Homebrew if not installed\n/bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"\n\n# Install dependencies\nbrew install git wget curl jq\n\n" if self.is_mac else "# Install essential dependencies\nsudo apt update\nsudo apt install -y build-essential git wget curl jq\n\n"
                
                return {
                    "status": "success",
                    "output": f"# Complete Dymension RollApp setup script\n\n"
                              f"{base_cmd}"
                              "# Install Go\n"
                              "wget -O go.tar.gz https://golang.org/dl/go1.23.0.linux-amd64.tar.gz\n"
                              "sudo rm -rf /usr/local/go\n"
                              "sudo tar -C /usr/local -xzf go.tar.gz\n"
                              "rm go.tar.gz\n"
                              "echo 'export PATH=$PATH:/usr/local/go/bin:$HOME/go/bin' >> ~/.bashrc\n"
                              "source ~/.bashrc\n\n"
                              "# Install Roller CLI\n"
                              "curl https://raw.githubusercontent.com/dymensionxyz/roller/main/install.sh | bash\n\n"
                              "# Install Dymension Chain\n"
                              "git clone https://github.com/dymensionxyz/dymension.git\n"
                              "cd dymension\n"
                              "git checkout v1.0.2-beta\n"
                              "make install\n\n"
                              "# Verify installation\n"
                              "roller version\n"
                              "dymd version\n\n"
                              "# Note: After installation, you can create a RollApp with:\n"
                              "# roller create my_rollapp mytoken\n\n"
                              "echo 'Dymension environment setup complete!'\n",
                    "error": ""
                }
    
    def extract_multi_command(self, command_text: str) -> Dict:
        """Extract multiple commands from a natural language instruction.
        
        Args:
            command_text: Natural language command with potentially multiple instructions
            
        Returns:
            Dict with combined commands and instructions
        """
        command_text = command_text.lower()
        commands_to_execute = []
        found_commands = []
        
        # Check for installation sequence
        if "install" in command_text:
            # Check for essentials/dependencies
            if any(term in command_text for term in ["essential", "essentials", "dependencies"]):
                found_commands.append("essentials")
                
            # Check for Go installation
            if any(term in command_text for term in ["go", "golang"]):
                version_match = re.search(r"go (?:version )?([0-9]+\.[0-9]+\.[0-9]+)", command_text)
                go_version = version_match.group(1) if version_match else "1.23.0"
                found_commands.append(f"go_{go_version}")
                
            # Check for roller installation
            if any(term in command_text for term in ["roller", "roller cli"]):
                found_commands.append("roller")
                
            # Check for dymd installation
            if any(term in command_text for term in ["dymd", "dymension chain"]):
                found_commands.append("dymd")
        
        # RollApp management commands
        if "create rollapp" in command_text or "new rollapp" in command_text:
            rollapp_name_match = re.search(r"(?:named|called|with name|id) ['\"]*([a-zA-Z0-9_-]+)['\"]*", command_text)
            if rollapp_name_match:
                found_commands.append(f"create_rollapp_{rollapp_name_match.group(1)}")
        
        # Wallet management commands
        if "create wallet" in command_text or "new wallet" in command_text:
            wallet_name_match = re.search(r"(?:named|called|with name) ['\"]*([a-zA-Z0-9_-]+)['\"]*", command_text)
            if wallet_name_match:
                found_commands.append(f"create_wallet_{wallet_name_match.group(1)}")
        
        # Now build the actual commands for each identified action
        essential_cmd = "sudo apt install -y build-essential clang curl aria2 wget tar jq libssl-dev pkg-config make"
        
        for cmd in found_commands:
            if cmd == "essentials":
                commands_to_execute.append({
                    "description": "Install essential dependencies",
                    "command": essential_cmd,
                    "sudo_required": True
                })
            elif cmd.startswith("go_"):
                go_version = cmd.split("_")[1]
                commands_to_execute.append({
                    "description": f"Install Go {go_version}",
                    "command": f"wget -O go.tar.gz https://golang.org/dl/go{go_version}.linux-amd64.tar.gz && sudo rm -rf /usr/local/go && sudo tar -C /usr/local -xzf go.tar.gz && rm go.tar.gz",
                    "sudo_required": True
                })
                commands_to_execute.append({
                    "description": "Add Go to your PATH",
                    "command": "echo 'export PATH=$PATH:/usr/local/go/bin:$HOME/go/bin' >> ~/.profile && source ~/.profile",
                    "sudo_required": False
                })
            elif cmd == "roller":
                commands_to_execute.append({
                    "description": "Install Roller CLI",
                    "command": "curl https://raw.githubusercontent.com/dymensionxyz/roller/main/install.sh | bash",
                    "sudo_required": False
                })
            elif cmd == "dymd":
                commands_to_execute.append({
                    "description": "Clone Dymension repository",
                    "command": "git clone https://github.com/dymensionxyz/dymension.git",
                    "sudo_required": False
                })
                commands_to_execute.append({
                    "description": "Build and install dymd",
                    "command": "cd dymension && git checkout v1.0.2-beta && make install",
                    "sudo_required": False
                })
            elif cmd.startswith("create_rollapp_"):
                rollapp_name = cmd.split("_", 2)[2]
                commands_to_execute.append({
                    "description": f"Initialize RollApp {rollapp_name}",
                    "command": f"roller create {rollapp_name} {rollapp_name}token",
                    "sudo_required": False
                })
            elif cmd.startswith("create_wallet_"):
                wallet_name = cmd.split("_", 2)[2]
                commands_to_execute.append({
                    "description": f"Create wallet {wallet_name}",
                    "command": f"dymd keys add {wallet_name}",
                    "sudo_required": False
                })
        
        # If no commands were found, return empty result
        if not commands_to_execute:
            return {
                "status": "error",
                "output": "",
                "error": "No specific commands could be extracted from your description. Please try a more specific request."
            }
        
        # Format the output as a shell script with comments
        script_output = "#!/bin/bash\n# Commands to execute based on your request\n\n"
        
        for cmd_info in commands_to_execute:
            script_output += f"# {cmd_info['description']}\n{cmd_info['command']}\n\n"
        
        # Add a note about sudo permissions if needed
        if any(cmd["sudo_required"] for cmd in commands_to_execute):
            script_output += "# Note: Some commands require sudo privileges. You may be prompted for your password.\n"
        
        return {
            "status": "success",
            "output": script_output,
            "raw_output": commands_to_execute,
            "error": ""
        }
    
    def parse_command(self, command_text: str) -> Dict:
        """Parse a command string provided by the user and execute the appropriate Dymension command.
        
        Args:
            command_text: Natural language command description
            
        Returns:
            Dict with command result
        """
        command_text = command_text.lower().strip()
        
        # Check for OS detection command
        if re.search(r"(?:detect|check|show) (?:my )?(?:os|operating system|platform)", command_text):
            return self.detect_os()
            
        # Installation commands
        if re.search(r"install all|install everything|setup everything", command_text):
            return self.simulate_install("all")
        
        elif re.search(r"install (?:the )?essentials", command_text) or re.search(r"install (?:the )?dependencies", command_text):
            return self.simulate_install("essentials")
        
        elif re.search(r"install (?:go|golang)", command_text):
            return self.simulate_install("go")
        
        elif re.search(r"install (?:the )?roller", command_text):
            return self.simulate_install("roller")

        # ... rest of the parse_command method ...

    def detect_os(self) -> Dict:
        """Return information about the detected operating system"""
        return {
            "status": "success",
            "output": f"Detected operating system: {self.os}\n"
                     f"Is Windows: {self.is_windows}\n"
                     f"Is macOS: {self.is_mac}\n"
                     f"Is Linux: {self.is_linux}",
            "error": ""
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