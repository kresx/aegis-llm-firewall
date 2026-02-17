import random

def mutate_prompt(prompt: str) -> str:
    """Simple fuzzer to create adversarial variants of a prompt."""
    leet_swap = {'a': '4', 'e': '3', 'i': '1', 'o': '0', 's': '5'}
    new_prompt = list(prompt)
    
    for i, char in enumerate(new_prompt):
        if char.lower() in leet_swap and random.random() > 0.7:
            new_prompt[i] = leet_swap[char.lower()]
            
    return "".join(new_prompt)