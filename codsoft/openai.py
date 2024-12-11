import random
from datetime import datetime
import openai
import os

# Set your OpenAI API key from an environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

def chatbot():
    print("Chatbot: Hi! I’m a chatbot powered by AI. Ask me anything! Type 'exit' to end the conversation.")

    while True:
        user_input = input("You: ").strip()

        # Exit condition
        if user_input.lower() == "exit":
            print("Chatbot: Goodbye! Feel free to chat with me anytime!")
            break

        # Predefined responses for specific intents
        elif "time" in user_input.lower():
            now = datetime.now()
            print(f"Chatbot: The current time is {now.strftime('%H:%M:%S')}.")
        elif "joke" in user_input.lower():
            jokes = [
                "Why don't scientists trust atoms? Because they make up everything!",
                "What do you call fake spaghetti? An impasta!",
                "Why did the scarecrow win an award? Because he was outstanding in his field!"
            ]
            print(f"Chatbot: {random.choice(jokes)}")
        elif "name" in user_input.lower():
            print("Chatbot: I'm Chatbot, your virtual assistant!")
        elif "weather" in user_input.lower():
            print("Chatbot: I can't check the weather right now, but you can use a weather app for accurate updates!")
        elif "love" in user_input.lower():
            print("Chatbot: Love is a beautiful emotion! What do you think about it?")
        elif "help" in user_input.lower():
            print("Chatbot: Sure, I'm here to help! Please specify what you need assistance with.")
        elif "favorite" in user_input.lower():
            print("Chatbot: I don't have favorites, but I enjoy chatting with you!")
        elif "you" in user_input.lower() and "do" in user_input.lower():
            print("Chatbot: I’m here to chat and assist you with your questions. What can I help you with today?")
        else:
            # Use OpenAI API for more complex responses
            try:
                response = openai.Completion.create(
                    engine="text-davinci-003",
                    prompt=f"The user asked: {user_input}\nProvide a helpful response:",
                    max_tokens=150,
                    n=1,
                    stop=None,
                    temperature=0.7,
                )
                print(f"Chatbot: {response['choices'][0]['text'].strip()}")
            except Exception as e:
                print("Chatbot: I'm sorry, I couldn't process that request right now. Please try again later.")

# Run the chatbot
if __name__ == "__main__":
    chatbot()
