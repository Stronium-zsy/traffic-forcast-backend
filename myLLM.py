from http import HTTPStatus
from dashscope import Application
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/call_agent', methods=['GET'])
def call_agent():
    prompt = request.args.get('user_prompt')
    response = Application.call(app_id='0d67e26286e54f9b9f20d52175493733',
                                prompt=prompt,
                                api_key='sk-08431a08d23b4ed6a9942277c6c182e3')

    if response.status_code != HTTPStatus.OK:
        print('request_id=%s, code=%s, message=%s\n' % (response.request_id, response.status_code, response.message))
    else:
        print(response.output.text)
        return jsonify(response.output.text)


if __name__ == '__main__':
    app.run(host='127.0.0.1',port='5002')
    # 2024年3月4日晚上18点，我想从Ames Research Center 前往 San Jose的火车站，如何规划路线？
