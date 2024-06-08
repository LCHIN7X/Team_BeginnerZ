import openai
openai.api_key="sk-proj-uJqoM1gyXzNM16es4nnXT3BlbkFJXwEqUFJMVy7f7lCYHfsy"
def generate_financial_literacy_content(prompt):
    response = openai.Completion.create(
        engine="text-davinci-004",
        prompt=prompt,
        max_tokens=500,
        temperature=0.7
    )
    return response.choices[0].text.strip()

# Example usage
prompt = "Explain the concept of compound interest and its benefits."
content = generate_financial_literacy_content(prompt)
print(content)

