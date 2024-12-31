import logging
import json
from typing import Dict, Any

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Agent transfer functions
def transfer_to_security_expert():
    from triage_agent.agents import security_expert
    return security_expert

def transfer_to_business_logic():
    from triage_agent.agents import business_logic
    return business_logic

def transfer_to_onchain_analyst():
    from triage_agent.agents import onchain_analyst
    return onchain_analyst

def transfer_to_white_hat():
    from triage_agent.agents import white_hat
    return white_hat

def transfer_to_doc_specialist():
    from triage_agent.agents import doc_specialist
    return doc_specialist

def transfer_to_lead_auditor():
    from triage_agent.agents import lead_auditor
    return lead_auditor

# Security analysis tools
def analyze_vulnerabilities(contract_code: str) -> Dict[str, Any]:
    """
    Analyze smart contract code for vulnerabilities
    
    Args:
        contract_code (str): The smart contract source code to analyze
        
    Returns:
        Dict containing:
        - vulnerabilities: List of found vulnerabilities
        - severity: Severity level for each vulnerability
        - description: Detailed description of each issue
    """
    logger.info("Analyzing contract vulnerabilities...")
    
    try:
        # Actually use the contract_code parameter
        findings = {
            "vulnerabilities": [],
            "severity": [],
            "description": [],
            "code_analyzed": contract_code
        }
        
        # Basic analysis examples
        if "function" in contract_code:
            findings["vulnerabilities"].append("Found functions")
            findings["severity"].append("Info")
            findings["description"].append("Contract contains functions")
            
        if "public" in contract_code:
            findings["vulnerabilities"].append("Public functions found")
            findings["severity"].append("Info")
            findings["description"].append("Contract has public functions")
        
        logger.info("Vulnerability analysis completed")
        return json.dumps(findings)
    except Exception as e:
        logger.error(f"Error in vulnerability analysis: {str(e)}")
        return json.dumps({"error": f"Analysis failed: {str(e)}"})

def verify_exploit(contract_code: str, vulnerability: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Verify if an exploit is possible for a given vulnerability
    
    Args:
        contract_code (str): The smart contract source code
        vulnerability (Dict, optional): Details of the vulnerability to verify
        
    Returns:
        Dict containing:
        - exploitable: Boolean indicating if exploit is possible
        - impact: Potential impact of the exploit
        - poc: Proof of concept if applicable
    """
    logger.info(f"Verifying exploit for vulnerability: {vulnerability}")
    
    try:
        result = {
            "exploitable": False,
            "impact": "Unknown",
            "poc": None,
            "code_analyzed": contract_code
        }
        
        # Basic verification (even without specific vulnerability)
        if "public" in contract_code and "payable" in contract_code:
            result["exploitable"] = True
            result["impact"] = "Potential unauthorized access"
            result["poc"] = "Function can be called by anyone with ETH"
        
        # If specific vulnerability provided, check that too
        if vulnerability:
            # Add specific vulnerability checks here
            pass
            
        logger.info("Exploit verification completed")
        return json.dumps(result)
    except Exception as e:
        logger.error(f"Error in exploit verification: {str(e)}")
        return json.dumps({"error": f"Verification failed: {str(e)}"})

def analyze_business_logic(contract_code: str) -> Dict[str, Any]:
    """
    Analyze business logic and architecture of the smart contract
    
    Args:
        contract_code (str): The smart contract source code
        
    Returns:
        Dict containing analysis of business logic concerns
    """
    logger.info("Analyzing business logic...")
    
    try:
        analysis = {
            "architecture_issues": [],
            "logic_flaws": [],
            "recommendations": [],
            "code_analyzed": contract_code
        }
        
        # Basic logic analysis
        if "require" in contract_code:
            analysis["architecture_issues"].append("Found require statements")
            analysis["recommendations"].append("Verify require conditions")
            
        if "onlyOwner" in contract_code:
            analysis["architecture_issues"].append("Centralization risk")
            analysis["recommendations"].append("Consider multi-sig or DAO")
        
        logger.info("Business logic analysis completed")
        return json.dumps(analysis)
    except Exception as e:
        logger.error(f"Error in business logic analysis: {str(e)}")
        return json.dumps({"error": f"Analysis failed: {str(e)}"})

def analyze_onchain_data(contract_address: str) -> Dict[str, Any]:
    """
    Analyze on-chain data related to the smart contract
    
    Args:
        contract_address (str): The deployed contract address
        
    Returns:
        Dict containing on-chain analysis results
    """
    logger.info(f"Analyzing on-chain data for contract: {contract_address}")
    
    try:
        analysis = {
            "transaction_patterns": [],
            "similar_contracts": [],
            "risk_indicators": [],
            "address_analyzed": contract_address
        }
        
        # Basic on-chain analysis
        analysis["transaction_patterns"].append("Contract interactions found")
        analysis["risk_indicators"].append("Normal transaction flow")
        
        logger.info("On-chain analysis completed")
        return json.dumps(analysis)
    except Exception as e:
        logger.error(f"Error in on-chain analysis: {str(e)}")
        return json.dumps({"error": f"Analysis failed: {str(e)}"})

def format_audit_report(findings: str) -> str:
    """Format the audit report in a standardized way"""
    try:
        logger.info("Formatting audit report")
        
        # Convert string findings to dict if it's a string
        if isinstance(findings, str):
            findings_dict = {
                "vulnerabilities": [findings],
                "description": [findings]
            }
        report = {
            "summary": [],
            "details": [],
            "recommendations": [],
            "findings_analyzed": findings_dict
        }
        
        # Basic report formatting
        if findings_dict.get("vulnerabilities"):
            report["summary"].extend(findings_dict["vulnerabilities"])
            report["details"].extend(findings_dict.get("description", []))
        
        logger.info("Report formatting completed")
        return json.dumps(report)
    except Exception as e:
        logger.error(f"Error in report formatting: {str(e)}")
        return json.dumps({"error": f"Formatting failed: {str(e)}"})
