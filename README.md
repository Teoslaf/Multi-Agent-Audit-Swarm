# Smart Contract Security Audit System 🔒

An automated smart contract security audit system powered by AI agents (OpenAI GPT-4 and Anthropic Claude) that collaborate to analyze smart contracts for vulnerabilities.

## Features ✨

- Multi-agent collaboration system
- Support for both OpenAI and Anthropic Claude models
- Automated vulnerability analysis
- Business logic review
- Exploit verification
- Detailed audit reports
- Easy switching between AI providers

## Installation 🛠️

1. Clone the repository:
```bash
git clone https://github.com/Teoslaf/Multi-Agent-Audit-Swarm.git swarm
cd swarm
```

2. Create and activate a virtual environment:
```bash
python -m venv venv

# On Windows:
.\venv\Scripts\activate

# On Unix/MacOS:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root:
```env
OPENAI_API_KEY=your-openai-key-here
ANTHROPIC_API_KEY=your-anthropic-key-here
OPENAI_MODEL=gpt-4-0125-preview
CLAUDE_MODEL=claude-3-sonnet-20240229
```

## Docker Usage 🐳

1. Build the image:
```bash
docker build -t smart-contract-audit .
```

2. Run the audit:
```bash
# Using OpenAI
docker run --env-file .env smart-contract-audit --provider openai --contract test.sol

# Using Claude
docker run --env-file .env smart-contract-audit --provider anthropic --contract test.sol
```

## Project Structure 📁

```
smart-contract-audit/
├── venv/
├── triage_agent/
│   ├── __init__.py
│   ├── agents.py      # Agent definitions
│   ├── prompts.py     # Agent instructions
│   ├── tools.py       # Analysis tools
│   └── run.py         # Main execution script
├── swarm.py           # Agent collaboration system
├── requirements.txt
├── .env
└── README.md
```

## Agents 🤖

- **Security Expert**: Analyzes smart contracts for security vulnerabilities
- **Business Logic Expert**: Reviews contract logic and business implications
- **White Hat**: Verifies potential exploits
- **Documentation Specialist**: Formats and finalizes audit reports

## Environment Variables 🔑

- `OPENAI_API_KEY`: Your OpenAI API key
- `ANTHROPIC_API_KEY`: Your Anthropic API key
- `OPENAI_MODEL`: OpenAI model to use (default: gpt-4-0125-preview)
- `CLAUDE_MODEL`: Claude model to use (default: claude-3-sonnet-20240229)

## Workflow 🔄

### 1. Initial Analysis
- **Security Expert** scans for vulnerabilities
- **Business Logic Expert** reviews contract design
- **White Hat** verifies potential exploits

### 2. Collaborative Rounds
For each round (default: 3 rounds):
1. Each agent reviews others' findings
2. Adds new insights and concerns
3. Validates or challenges previous findings
4. Expands on attack vectors

### 3. Final Report
**Documentation Specialist** compiles:
- Combined findings from all agents
- Results from collaborative rounds
- Prioritized vulnerabilities
- Recommended fixes

Output Example:
```
📊 Final Audit Report
==================================================
[Vulnerability Summary]
- High Risk: Re-entrancy in withdraw function
- Medium Risk: Unchecked return values

[Detailed Analysis]
...

[Recommendations]
...
==================================================
```
