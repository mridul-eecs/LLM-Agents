from phi.agent import Agent
from phi.model.groq import Groq
from ivr_flows import handle_user_input
from llama_handler import interpret_user_input

# Initialize the Agent with the Groq-hosted Llama model
agent = Agent(
    model=Groq(id="Llama-3.3-70b-versatile")
)

def interpret_response(agent_reply):
    """
    Interpret the agent's reply to identify intent and entities.
    """
    intent = "unknown"
    entities = {}

    if "bill" in agent_reply.lower():
        intent = "billing"
        # Check if the LLM is requesting account details
        if "account number" in agent_reply.lower():
            print("IVR: Please provide your account number to proceed.")
            account_number = input("You: ")
            entities["account_number"] = account_number
        else:
            # Assume LLM provides account-related entities directly
            # Extend this logic based on response patterns
            entities["account_type"] = "phone"

    elif "tech support" in agent_reply.lower():
        intent = "tech_support"

    return intent, entities


def main():
    print("Welcome to XYZ Telecom IVR!")
    print("Say something like 'I want to know my bill' or 'Connect me to tech support.'")

    # Initialize the agent
    agent = Agent(model=Groq(id="Llama-3.3-70b-versatile"))

    # Session loop
    entities = {}
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("IVR: Thank you for using XYZ Telecom IVR. Goodbye!")
            break

        # Prepare messages for the model
        messages_for_model = [
            {"role": "system", "content": "You are a helpful IVR assistant."},
            {"role": "user", "content": user_input}
        ]

        # Call agent with messages passed to the model
        response = agent.run(input_data=user_input, messages=messages_for_model)
        print(f"Response from Agent: {response.content}")

        # Interpret the response and handle entities
        intent, new_entities = interpret_response(response.content)
        entities.update(new_entities)

        # Handle user input based on intent and entities
        reply = handle_user_input(intent, entities)
        print(f"IVR: {reply}")

        # If billing intent and account number is provided, exit the loop
        if intent == "billing" and "account_number" in entities:
            break



if __name__ == "__main__":
    main()