from swarm import Agent
from triage_agent.tools import (
    analyze_vulnerabilities,
    verify_exploit,
    analyze_business_logic,
    format_audit_report
)
from triage_agent.prompts import (
    SECURITY_EXPERT_PROMPT,
    BUSINESS_LOGIC_PROMPT,
    WHITE_HAT_PROMPT,
    DOC_SPECIALIST_PROMPT
)
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class AuditAgents:
    def __init__(self, swarm):
        # Load models from environment variables
        self.openai_model = os.getenv('OPENAI_MODEL', "gpt-4o-2024-08-06")
        self.claude_model = os.getenv('CLAUDE_MODEL', "claude-3-sonnet-20240229")
        self.current_provider = "openai"  # default provider
        self.current_model = self.openai_model  # default model
        self.swarm = swarm
        
        # Register tools
        self.swarm.register_tool("analyze_vulnerabilities", analyze_vulnerabilities)
        self.swarm.register_tool("verify_exploit", verify_exploit)
        self.swarm.register_tool("analyze_business_logic", analyze_business_logic)
        self.swarm.register_tool("format_audit_report", format_audit_report)
    
    def set_provider(self, provider: str, model: str = None):
        """Set the provider and model for all agents"""
        self.current_provider = provider.lower()
        if model:
            self.current_model = model
        else:
            self.current_model = self.openai_model if provider == "openai" else self.claude_model
    
    def security_expert(self):
        return Agent(
            name="Security Expert",
            instructions=SECURITY_EXPERT_PROMPT,
            model=self.current_model,
            provider=self.current_provider,
            tools=["analyze_vulnerabilities", "verify_exploit"]
        )
        
    def business_logic(self):
        return Agent(
            name="Business Logic Expert",
            instructions=BUSINESS_LOGIC_PROMPT,
            model=self.current_model,
            provider=self.current_provider,
            tools=["analyze_business_logic"]
        )
        
    def white_hat(self):
        return Agent(
            name="White Hat",
            instructions=WHITE_HAT_PROMPT,
            model=self.current_model,
            provider=self.current_provider,
            tools=["verify_exploit"]
        )
        
    def doc_specialist(self):
        return Agent(
            name="Documentation Specialist",
            instructions=DOC_SPECIALIST_PROMPT,
            model=self.current_model,
            provider=self.current_provider,
            tools=["format_audit_report"]
        )
