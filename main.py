import os
import asyncio
import cognee
from litellm import completion
from dotenv import load_dotenv

load_dotenv()

async def run_reconciler():
    print("--- Sprint 3: The Context Reconciler Engine ---")
    
    # 1. The User's Question
    query = "What is the company policy on remote work for software engineers?"
    print(f"\nUser asks: '{query}'")
    
    # 2. Query the Graph Database
    print("\n1. Searching the graph for context...")
    search_results = await cognee.search(query)
    
    # Extract the raw text from the search results
    context_chunks = []
    for result in search_results:
        if 'search_result' in result:
            context_chunks.extend(result['search_result'])
            
    print("\n2. Raw Context Retrieved from Graph:")
    for chunk in context_chunks:
        print(f" - [Memory]: {chunk}")
        
    print("\n3. Pushing to Reconciler LLM for temporal evaluation...")
    
    # 3. The Reconciler Logic (LLM as a judge)
    reconciler_prompt = f"""
    You are a strict internal policy reconciler. 
    You must answer the user's question based strictly on the provided context.
    
    Rules for reconciliation:
    - If there are conflicting policies, you must look for dates.
    - The most recent date is the absolute current truth.
    - Explicitly state that older policies have been superseded.
    
    User Question: {query}
    
    Raw Context:
    {context_chunks}
    """
    
    # 4. Generate the final reconciled answer
    response = completion(
        model=os.getenv("LLM_MODEL", "gemini/gemini-2.5-flash"),
        messages=[{"role": "user", "content": reconciler_prompt}]
    )
    
    final_answer = response.choices[0].message.content
    print("\n========================================")
    print("🏆 FINAL RECONCILED OUTPUT:")
    print("========================================")
    print(final_answer)

if __name__ == "__main__":
    asyncio.run(run_reconciler())