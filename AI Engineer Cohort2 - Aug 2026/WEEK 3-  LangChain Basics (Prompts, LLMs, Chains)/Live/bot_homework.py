"""
Homework: Build Your Own Chatbot
=================================

Fill in each function below according to its docstring.
Do NOT change the function names or the overall structure (main() calls the
other functions in order) - that's what keeps this an executable script.

Pick ONE persona for your bot before you start (translator, recipe helper,
study buddy, trip planner, etc.) and design your system message and
guardrail around that persona.

Run with: 
"""

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.messages import SystemMessage, HumanMessage

load_dotenv()


def get_chat_model():
    """
    TODO: Initialize and return a LangChain chat model with init_chat_model().

    Use the same model/provider you used in class (e.g. gpt-4o-mini / openai).
    """
    pass


def get_system_message():
    """
    TODO: Return a SystemMessage that locks the bot into ONE persona/job.

    This is where your guardrail lives: explicitly tell the model what it
    should refuse to do, and how it should respond when the user asks for
    something outside its job (e.g. "I'm a translator, please give me
    translation tasks only!").
    """
    pass


def print_welcome():
    """
    TODO: Print a short welcome message explaining what this bot does and
    how to use it (what kind of input the user should type).
    """
    pass


def get_user_input():
    """
    TODO: Prompt the user for input and return what they typed.

    Think about what should happen if the user just presses Enter
    (empty input) - don't let that crash the script.
    """
    pass


def is_exit_command(user_input):
    """
    TODO: Return True if the user typed something that means "end the chat"
    (e.g. quit / exit / bye), False otherwise.

    A real chatbot doesn't ask "do you want to continue?" after every single
    message - the user just keeps typing until they say they're done.
    """
    pass


def call_chatbot(chat_model, system_message, user_input, conversation_history=None):
    """
    TODO: Send the system message + user_input to the chat model using
    .invoke() and return the response text.

    conversation_history is what gives the bot memory - pass in the earlier
    turns (not just the latest user_input) so the model has context from
    the rest of the conversation, not just a single isolated message.

    Wrap the model call in a try/except so an API failure doesn't crash
    the script - return a friendly error message instead.
    """
    pass


def main():
    """
    TODO: Tie everything together:
      1. Set up the chat model and system message (once, before the loop)
      2. Print the welcome message
      3. Keep a running conversation_history (starts empty)
      4. Loop:
         - get user input
         - stop the loop if is_exit_command(user_input) is True
         - call the chatbot with the conversation_history included, print
           the response
         - add this turn (user_input + response) to conversation_history
      5. Print a goodbye message when the loop ends
    """
    pass


if __name__ == "__main__":
    main()
