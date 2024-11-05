import openai
from datetime import datetime, timedelta
from typing import List

# Set your OpenAI API key
openai.api_key = "YOUR_API_KEY"

# Define the number of days in the "week" (e.g., 7 for a standard week)
DAYS_IN_WEEK = 7

# Fetch messages from the past week
def fetch_interactions(user_id: str) -> List[str]:
    messages = []
    end_date = datetime.now()
    start_date = end_date - timedelta(days=DAYS_IN_WEEK)
    
    # Using a hypothetical API call to retrieve conversations.
    # Replace this with the actual API call if available.
    response = openai.ChatCompletion.retrieve_conversations(user=user_id, start_date=start_date.isoformat(), end_date=end_date.isoformat())
    
    for conversation in response.get('conversations', []):
        for message in conversation.get('messages', []):
            # Collect messages based on timestamp
            timestamp = datetime.fromisoformat(message['timestamp'])
            if start_date <= timestamp <= end_date:
                messages.append(message['content'])
    return messages

# Summarize a single message
def summarize_text(text: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "Summarize the following text into a few key points."},
            {"role": "user", "content": text}
        ]
    )
    return response['choices'][0]['message']['content']

# Generate weekly summary
def generate_weekly_summary(messages: List[str]) -> str:
    summaries = [summarize_text(msg) for msg in messages]
    weekly_summary_prompt = "\n".join(summaries)

    # Summarize all weekly summaries into one
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "Create a weekly summary based on the following points."},
            {"role": "user", "content": weekly_summary_prompt}
        ]
    )
    return response['choices'][0]['message']['content']

# Main function to summarize a user's week
def summarize_week(user_id: str):
    messages = fetch_interactions(user_id)
    if not messages:
        print("No messages found for the past week.")
        return

    weekly_summary = generate_weekly_summary(messages)
    print("Weekly Summary:")
    print(weekly_summary)

# Replace 'user_id_here' with the actual user ID or identifier
summarize_week("user_id_here")
