from datetime import datetime, timedelta
import json
import os

# File to store summarized memory entries
MEMORY_FILE = "summarized_memory.json"
BUFFER_LIMIT = 100  # Conversation lines before summarization

# Initialize conversation buffer
conversation_buffer = []

# Load memory summaries at startup
# Load memory summaries at startup
def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            memory = json.load(f)
            print("Loaded memory:", memory)  # Debug print
            return memory
    return []


# Save summarized memory to file
def save_memory(memory_summaries):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory_summaries, f)

# Add conversation line to buffer
def add_to_memory(name, message):
    memory_summaries = load_memory()
    # Add a summary field if it's available
    memory_summaries.append({"name": name, "message": message, "timestamp": datetime.now().isoformat(), "summary": message})
    save_memory(memory_summaries)



# Summarize conversations in buffer
def summarize_conversations():
    """Summarize the conversations stored in the buffer and save with a timestamp."""
    conversation_text = "\n".join([f"{entry['name']}: {entry['message']}" for entry in conversation_buffer])
    
    # Summarization prompt for MetaAI
    summary_prompt = (
        "Shino, I want you to summarize all these conversations into a single, compact paragraph "
        "to serve as memory. Add a timestamp to this summary, and discard any past timestamps "
        "over a week old:\n\n"
        f"{conversation_text}"
    )

    # Simulating MetaAI summarization response
    response_summary = summarize_with_meta_ai(summary_prompt)  # Assuming a function to get summary

    # Save summary with current timestamp
    memory_summaries = load_memory()
    memory_summaries.append({
        "summary": response_summary,
        "timestamp": datetime.now().isoformat()
    })

    # Clear buffer after summarization
    conversation_buffer.clear()
    # Save updated memory summaries
    save_memory(memory_summaries)

# Simulated summarization function (replace with actual MetaAI call)
def summarize_with_meta_ai(prompt):
    # Placeholder summary
    return "This is a summarized memory entry with updated context."

# Function to get the current memory context (latest summarized memory)
def get_memory_context():
    memory_summaries = load_memory()
    context = ""
    for entry in memory_summaries:
        # Check if 'summary' exists and use it, otherwise fallback to 'message'
        summary = entry.get("summary", entry.get("message", ""))
        context += f"{summary} (Timestamp: {entry['timestamp']})\n"
    return context


# Remove memory entries older than one week
def clean_old_memory():
    """Removes memory summaries that are older than one week."""
    memory_summaries = load_memory()
    one_week_ago = datetime.now() - timedelta(weeks=1)
    filtered_memory = [
        entry for entry in memory_summaries
        if datetime.fromisoformat(entry["timestamp"]) >= one_week_ago
    ]
    save_memory(filtered_memory)  # Update memory file with cleaned summaries
