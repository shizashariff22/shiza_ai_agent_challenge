
def reward_function(answer: str) -> float:
    """Reward function to avoid repetition and nonsense."""
    score = 0
    # Too short → bad
    if len(answer.split()) < 5:
        score -= 1
    # Ends with punctuation → good
    if answer.strip().endswith((".", "?", "!")):
        score += 1
    # Signs of reasoning → good
    if "because" in answer.lower() or "therefore" in answer.lower():
        score += 1
    # Penalize repetition
    if answer.lower().count("rooman") > 3:
        score -= 2
    # Penalize if it just repeats the question
    if answer.lower().startswith("what do you think"):
        score -= 2
    return score
