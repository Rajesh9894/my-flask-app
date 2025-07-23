from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello from Flask on Vercel!"

# Only required if you're testing locally
if __name__ == '__main__':
    app.run(debug=True)

