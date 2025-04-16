from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, World from the Compensation API!"

@app.route('/api/jobs/upload', methods=['POST'])
def upload_job_description():
    return "Upload endpoint reached"

@app.route('/api/jobs/search', methods=['GET'])
def search_jobs():
    return "Search endpoint reached"

if __name__ == '__main__':
    app.run(debug=True)
