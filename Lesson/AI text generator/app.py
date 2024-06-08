from flask import Flask, render_template, request
import openai

app = Flask(__name__)

# Configure OpenAI API key
openai.api_key = 'https://console.groq.com/playground'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    topic = request.form['topic']
    response = openai.Completion.create(
        engine="davinci-codex", # Use the appropriate model
        prompt=f"Write an article about {topic}",
        max_tokens=500
    )
    generated_content = response.choices[0].text.strip()
    return render_template('result.html', topic=topic, content=generated_content)

if __name__ == '__main__':
    app.run(debug=True)
