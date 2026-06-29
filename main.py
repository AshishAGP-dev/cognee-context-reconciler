import os
import asyncio
import cognee
from dotenv import load_dotenv

# Load the API key from the .env file
load_dotenv()

async def setup_test():
    print("Initializing Cognee Environment with Gemini...")
    
    # Verify the Gemini API key is loaded
    api_key = os.getenv("LLM_API_KEY")
    if not api_key or api_key == "your_actual_gemini_api_key":
        print("Error: Invalid or missing LLM_API_KEY in .env file.")
        return

    print("Gemini API Key detected.")
    
    # Clean the slate for our hackathon project
    print("Pruning previous graph data (if any)...")
    await cognee.prune.prune_data()
    await cognee.prune.prune_system()
    
    print("Success! Cognee is initialized and ready for Sprint 2.")

if __name__ == "__main__":
    # Run the async setup function
    asyncio.run(setup_test())