import os
import asyncio
import cognee
from dotenv import load_dotenv

load_dotenv()

async def run_ingestion():
    print("--- Starting: Ingestion Pipeline ---")
    
    # Prune existing data so we can run this script multiple times safely
    print("Cleaning the slate...")
    await cognee.prune.prune_data()
    await cognee.prune.prune_system()
    
    # Path to our initial 2025 policy file
    file_path = "data/policy_2025.txt"
    
    if not os.path.exists(file_path):
        print(f"Error: Could not find {file_path}. Make sure you created the data folder and file!")
        return

    print(f"1. Adding {file_path} to Cognee ingestion queue...")
    await cognee.add(file_path)
    
    print("2. Running cognify() to process data into a knowledge graph...")
    print("   (This might take a moment as Gemini reads the text and maps the nodes...)")
    await cognee.cognify()
    
    print("\nSuccess! Ingestion pipeline executed.")
    print("Cognee has successfully mapped the 2025 policy into its memory layer.")

if __name__ == "__main__":
    asyncio.run(run_ingestion())