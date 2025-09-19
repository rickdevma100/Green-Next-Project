# ADK Agent MCP Server

This project demonstrates an Agent Development Kit (ADK) agent Named Green_Next_Shopping_Agent that interacts with a project Called Online Boutique which is following microservices architecture. The interaction is facilitated by a Model Context Protocol (MCP) server that exposes tools to query and modify the database of the System and help end users to buy eco friendly product.


## Project Structure
It's a containerized application deployed on the same cluster where the online boutique is deployed. 

It's using Google ADK
Model Context Protocol
Deployed on Google Kubernetes Engine


## Setup Instructions

### 1. Prerequisites
- Python 3.11 or newer
- Access to a terminal or command prompt
- Access to GCP Cli.


It's highly recommended to use a virtual environment to manage project dependencies.

```bash
# Create a virtual environment (e.g., named .venv)
python3 -m venv .venv
```

Activate the virtual environment:

On macOS/Linux:
```bash
# Activate virtual environment
source .venv/bin/activate
```

On Windows:
```bash
# Activate virtual environment
.venv\Scripts\activate
```

### 3. Install Dependencies

Install all required Python packages using pip:

```bash
# Install all dependencies from requirements.txt
pip install -r requirements.txt
```

### 4. To Run the Project you can follow the deployment.md file for step by step process.
