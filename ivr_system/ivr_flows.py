def handle_user_input(intent, entities):
    """
    Handle the user's input based on the identified intent and entities.
    """
    if intent == "billing":
        account_number = entities.get("account_number")
        if account_number:
            return f"Fetching billing details for account {account_number}."
        else:
            return "It looks like we need more details to retrieve your bill. Please provide your account number."
    elif intent == "tech_support":
        return "Connecting you to tech support. Please hold."
    else:
        return "I'm not sure how to help with that. Could you please rephrase?"
