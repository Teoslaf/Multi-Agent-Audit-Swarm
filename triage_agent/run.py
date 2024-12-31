import sys
import os
import argparse
from textwrap import dedent
import logging
from dotenv import load_dotenv

load_dotenv()

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from swarm import Swarm
from triage_agent.agents import AuditAgents

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def read_contract_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run Smart Contract Security Audit')
    parser.add_argument('--provider', 
                       choices=['openai', 'anthropic'],
                       help='Choose AI provider (openai or anthropic)',
                       default='openai')
    parser.add_argument('--contract', 
                       help='Path to smart contract file',
                       default='test.sol')
    
    args = parser.parse_args()
    
    # Set the model based on provider
    model = os.getenv('OPENAI_MODEL') if args.provider == 'openai' else os.getenv('CLAUDE_MODEL')
    
    print("\n🔍 Starting Smart Contract Security Audit")
    print(f"Using {args.provider.upper()} model: {model}")
    print("="*50)
    
    try:
        # Read contract code
        contract_code = read_contract_file(args.contract)
        
        # Initialize Swarm with verbose mode
        swarm = Swarm(verbose=True)
        
        # Initialize agents with specified provider
        agents = AuditAgents(swarm)
        agents.set_provider(args.provider, model)
        
        audit_team = [
            agents.security_expert(),
            agents.business_logic(),
            agents.white_hat(),
            agents.doc_specialist()
        ]
        
        print("\n📋 Initializing audit process...")
        print("🔄 Analysis in progress...\n")
        
        # Run collaborative audit
        final_report = swarm.collaborate(
            agents=audit_team,
            initial_message=f"""
            Analyze this smart contract for security vulnerabilities:
            
            ```solidity
            {contract_code}
            ```
            """,
            max_rounds=3
        )
        
        print("\n📊 Final Audit Report")
        print("="*50)
        print(final_report)
        print("\n" + "="*50)
        
    except FileNotFoundError:
        logger.error(f"Could not find contract file at {args.contract}")
        print(f"❌ Error: Could not find contract file at {args.contract}")
    except Exception as e:
        logger.error(f"Error during audit: {str(e)}")
        print(f"❌ Error: {str(e)}")