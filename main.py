import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

import cognee
from litellm import completion

async def run_reconciler():
    print("--- Sprint 3: The Context Reconciler Engine ---")

    # 1. Clean the database
    print("\nCleaning database...")
    await cognee.prune.prune_data()
    await cognee.prune.prune_system(metadata=True)
    
    # 2. Add and process the data (REQUIRED after pruning)
    print("Ingesting AP Digital Store Policy History...")
    await cognee.add("data/ap_digital_store_policy_history.txt")
    
    # Import the raw cognify function and the task list
    from cognee.api.v1.cognify.cognify import cognify
    from cognee.modules.pipelines.tasks import get_default_tasks

    # Get the default tasks and filter out the failing graph/summarize task
    default_tasks = get_default_tasks()
    manual_tasks = [task for task in default_tasks if task.__name__ != "extract_graph_and_summarize"]

    # Run cognify with our manually filtered list
    await cognify(tasks=manual_tasks)

#    # Manually execute ONLY the tasks we need, skipping summarization
#     from cognee.api.v1.cognify.cognify import cognify
#     await cognify(tasks=[
#         "classify_documents",
#         "extract_chunks_from_documents",
#         "vector_indexing", 
#     ])
    
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
        model="ollama/qwen2.5:3b", 
        api_base=os.getenv("LLM_ENDPOINT", "http://localhost:11434"),
        messages=[{"role": "user", "content": reconciler_prompt}]
    )
    
    final_answer = response.choices[0].message.content
    print("\n========================================")
    print("🏆 FINAL RECONCILED OUTPUT:")
    print("========================================")
    print(final_answer)

if __name__ == "__main__":
    asyncio.run(run_reconciler())