from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'hellso this me blog'

if __name__ == '__main__':
    app.run(debug=True)