import random
import re
import spacy
from word2number import w2n  # Import word-to-number converter

nlp = spacy.load("en_core_web_sm")

def extract_math_info(user_input):
    # Convert text input to spaCy document
    doc = nlp(user_input)
    numbers = []
    operation = None

    for token in doc:
        # Check for numbers (like "five", "ten")
        if token.like_num:
            numbers.append(float(token.text))
        elif token.lemma_ in ["add", "plus", "sum"]:
            operation = "+"
        elif token.lemma_ in ["subtract", "minus", "less"]:
            operation = "-"
        elif token.lemma_ in ["multiply", "times", "product"]:
            operation = "*"
        elif token.lemma_ in ["divide", "over", "quotient"]:
            operation = "/"

    # Try to convert word numbers into actual numbers
    for token in doc:
        if token.text.lower() in ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]:
            numbers.append(w2n.word_to_num(token.text.lower()))  # Convert words like "seven" to 7

    if len(numbers) == 2 and operation:
        expression = f"{numbers[0]} {operation} {numbers[1]}"
        try:
            answer = eval(expression)
            return f"{expression} = {answer}"
        except:
            return "Hmm, I couldn't compute that."
    elif len(numbers) < 2:
        return "I need two numbers to work with!"
    else:
        return "I'm not sure what operation to use."

def tutor_response(user_input):
    if any(op in user_input for op in "+-*/"):
        return calculate_expression(user_input)
    elif any(keyword in user_input.lower() for keyword in ["what", "how", "sum", "product", "difference", "quotient"]):
        return extract_math_info(user_input)
    elif "quiz" in user_input.lower():
        question, answer = generate_quiz()
        return f"{question} (Answer: {answer})"
    elif "help" in user_input.lower():
        return "You can ask questions like 'What is the sum of 10 and 5?' or '12 * 4'."
    else:
        return "Try asking a math question or type 'quiz me'!"

def calculate_expression(expr):
    try:
        if re.fullmatch(r"[0-9+\-*/ ().]+", expr):
            result = eval(expr)
            return f"The answer is {result}"
        else:
            return "That doesn't look like a valid math expression."
    except:
        return "I couldn't solve that one."

def generate_quiz():
    ops = ['+', '-', '*']
    num1 = random.randint(1, 12)
    num2 = random.randint(1, 12)
    op = random.choice(ops)
    question = f"What is {num1} {op} {num2}?"
    answer = eval(f"{num1}{op}{num2}")
    return question, answer

def main():
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Bot: See you next time!")
            break
        print("Bot:", tutor_response(user_input))

if __name__ == "__main__":
    main()
