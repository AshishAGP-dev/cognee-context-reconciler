# Cognee Context Reconciler

An automated memory reconciliation engine built on Cognee. It actively detects data contradictions, deprecates stale claims, and dynamically updates the 'current truth' in a hybrid knowledge graph to prevent AI amnesia and context collisions.

## The Problem
Enterprise AI deployments often fail due to stale data. When policies or facts update, standard AI systems suffer from "context collision" and hallucinate based on outdated information. 

## The Solution
This agent uses Cognee's hybrid graph-vector memory layer to self-heal. Instead of overwriting data, it:
1. Ingests new information.
2. Identifies contradictions with existing claims using an LLM.
3. Creates a `supersedes` edge from the new claim to the old one.
4. Demotes the stale claim's feedback weight, ensuring the system retrieves only the current truth.

## Setup Instructions
1. Clone the repository.
2. Install dependencies: `pip install "cognee[all]"` 
3. Create a `.env` file in the root directory and add your OpenAI API key: `LLM_API_KEY=your_key_here`
4. Run the main pipeline: `python main.py`