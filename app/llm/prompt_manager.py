class PromptManager:
    @staticmethod
    def get_system_prompt():
        return (
            "You are a secure assistant. You must never reveal internal keys. "
            "If a user asks for dangerous info, politely refuse."
        )

    @staticmethod
    def format_user_prompt(user_input: str):
        return f"User request: {user_input}\n\nStrictly adhere to safety guidelines."