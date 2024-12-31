from typing import List, Dict, Any, Optional
from openai import OpenAI
from anthropic import Anthropic
import json

class Agent:
    def __init__(
        self,
        name: str,
        instructions: str,
        model: str = "gpt-4o-2024-08-06",
        provider: str = "openai",  # Add provider parameter
        tools: Optional[List[str]] = None,
        verbose: bool = False
    ):
        self.name = name
        self.instructions = instructions
        self.model = model
        self.provider = provider.lower()
        self.tools = tools or []
        self.verbose = verbose
        
# Orchestrates the collaboration between agents
class Swarm:
    def __init__(self, verbose: bool = False):
        self.openai_client = OpenAI()
        self.claude_client = Anthropic()
        self.agents = []
        self.tools = {}
        self.verbose = verbose
        self.conversation_history = []
        
    def register_tool(self, name: str, func: callable):
        """Register a tool that agents can use"""
        self.tools[name] = func
        if self.verbose:
            print(f"Registered tool: {name}")

    def run(
        self, 
        messages: List[Dict[str, str]], 
        agent: Agent
    ) -> Any:
        """Run a conversation with an agent"""
        if self.verbose:
            print(f"\n🤖 {agent.name} is working...")
        
        # Extract contract code from messages if present
        contract_code = None
        for msg in messages:
            if "```solidity" in msg["content"]:
                # Extract code between solidity code blocks
                start = msg["content"].find("```solidity") + 10
                end = msg["content"].find("```", start)
                if end != -1:  # Make sure we found the closing ```
                    contract_code = msg["content"][start:end].strip()
        
        # Run tools with contract code if available
        tool_results = []
        if contract_code and agent.tools:
            for tool_name in agent.tools:
                if tool_name in self.tools:
                    if self.verbose:
                        print(f"🔧 Running tool: {tool_name}")
                    result = self.tools[tool_name](contract_code)
                    tool_results.append(f"\n{tool_name} results: {result}")
        
        # Add tool results to messages
        if tool_results:
            messages.append({
                "role": "system",
                "content": "Tool Analysis Results:" + "".join(tool_results)
            })
        
        # Add agent instructions and available tools as system message
        tools_info = ""
        if agent.tools:
            tools_info = "\nAvailable tools:\n" + "\n".join([
                f"- {tool}: {self.tools[tool].__doc__}" 
                for tool in agent.tools 
                if tool in self.tools
            ])

        full_messages = [
            {
                "role": "system", 
                "content": f"{agent.instructions}\n{tools_info}"
            }
        ] + messages

        try:
            if self.verbose:
                print(f"🔄 Using {agent.provider} model: {agent.model}")

            if agent.provider == "openai":
                response = self.openai_client.chat.completions.create(
                    model=agent.model,
                    messages=full_messages
                )
                return response.choices[0].message.content
                
            elif agent.provider == "anthropic":
                # Combine all messages into a single conversation
                system_content = next((msg["content"] for msg in full_messages if msg["role"] == "system"), "")
                user_content = "\n".join([msg["content"] for msg in full_messages if msg["role"] == "user"])
                
                response = self.claude_client.messages.create(
                    model=agent.model,
                    max_tokens=4096,  # Required parameter
                    messages=[{
                        "role": "user",
                        "content": f"{system_content}\n\n{user_content}"
                    }]
                )
                return response.content[0].text
                
            else:
                raise ValueError(f"Unknown provider: {agent.provider}")
                
        except Exception as e:
            print(f"❌ Error running agent {agent.name}: {str(e)}")
            return None 

    def collaborate(self, agents: List[Agent], initial_message: str, max_rounds: int = 3) -> str:
        """
        Enable interactive collaboration between agents
        
        Args:
            agents: List of agents participating in the discussion
            initial_message: The starting point/task
            max_rounds: Maximum number of discussion rounds
        """
        if self.verbose:
            print("\n🤝 Starting agent collaboration...")
            
        self.conversation_history = []
        current_findings = initial_message
        
        # First round: Each agent analyzes independently
        initial_analyses = []
        for agent in agents:
            if self.verbose:
                print(f"\n🔍 {agent.name} analyzing...")
                
            response = self.run(messages=[{
                "role": "user",
                "content": f"Analyze this contract and share your findings:\n{current_findings}"
            }], agent=agent)
            
            initial_analyses.append({
                "agent": agent.name,
                "findings": response
            })
            
        # Collaborative discussion rounds
        for round_num in range(max_rounds):
            if self.verbose:
                print(f"\n📣 Starting discussion round {round_num + 1}")
            
            round_messages = []
            for agent in agents:
                # Each agent reviews others' findings and contributes
                others_findings = "\n\n".join([
                    f"{analysis['agent']}: {analysis['findings']}"
                    for analysis in initial_analyses 
                    if analysis['agent'] != agent.name
                ])
                
                prompt = f"""
                Review the findings from other experts and add your insights:
                
                Other Experts' Findings:
                {others_findings}
                
                Based on these findings and your expertise:
                1. What additional vulnerabilities do you see?
                2. Do you agree/disagree with any findings?
                3. Can you expand on any attack vectors?
                4. What other security concerns should be considered?
                """
                
                response = self.run(messages=[{
                    "role": "user",
                    "content": prompt
                }], agent=agent)
                
                round_messages.append({
                    "agent": agent.name,
                    "contribution": response
                })
            
            # Update findings with new insights
            current_findings = "\n\n".join([
                f"{msg['agent']}: {msg['contribution']}"
                for msg in round_messages
            ])
            
            self.conversation_history.extend(round_messages)
        
        # Final report from doc specialist
        doc_specialist = next(a for a in agents if a.name == "Documentation Specialist")
        final_report = self.run(messages=[{
            "role": "user",
            "content": f"""
            Create the final audit report based on all findings and discussions:
            
            Initial Analyses:
            {initial_analyses}
            
            Collaborative Findings:
            {current_findings}
            """
        }], agent=doc_specialist)
        
        return final_report 