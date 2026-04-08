import os
from dotenv import load_dotenv
import anthropic

# load_dotenv() reads your .env file and puts keys into os.environ
# Just like process.env in Node
load_dotenv()

# Initialize the client — this is like new Anthropic() in TS
client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)

def ask_claude(prompt: str) -> str:
    """
    Send a prompt to Claude and get the text response back.
    The type hint ': str' and '-> str' are optional but good practice.
    """
    message = client.messages.create(
        model="claude-haiku-4-5",      # the model to use
        max_tokens=1024,               # max length of response
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    # message.content is a list of blocks — we want the text of the first one
    return message.content[0].text

# Test it
if __name__ == "__main__":
    response = ask_claude("Say hello in 10 words.")
    print(response)