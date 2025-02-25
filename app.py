from chatbot import get_bot_reply
from tts_utils import tts_output
import uuid

if __name__ == "__main__":
    session_id = str(uuid.uuid4())
    print("=== Gemini Chatbot (Text Input + Voice Output) ===")
    print("Type 'exit' or 'quit' to end.\n")

    while True:
        user_text = input("You: ")
        if user_text.lower() in ["exit", "quit"]:
            print("Exiting chat...")
            break

        # Get AI response
        result = get_bot_reply(user_text, session_id)
        bot_reply = result["output"]

        # Generate TTS audio
        audio_file = tts_output(bot_reply)

        # Print AI response
        print("Bot:", bot_reply)
        print("Audio saved to:", audio_file)

        # Print conversation history
        print("\n--- Conversation History ---")
        for msg in result["messages"]:
            print(f"{msg.role.capitalize()}: {msg.content}")
        print("----------------------------\n")