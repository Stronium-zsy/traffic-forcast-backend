from http import HTTPStatus
from dashscope import Application
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/call_agent', methods=['GET'])
def call_agent():
    prompt = request.args.get('user_prompt')
    response = Application.call(app_id='<your_app_id>',
                                prompt=prompt,
                                api_key=<your_api_key>)

    if response.status_code != HTTPStatus.OK:
        print('request_id=%s, code=%s, message=%s\n' % (response.request_id, response.status_code, response.message))
    else:
        print(response.output.text)
        return jsonify(response.output.text)


if __name__ == '__main__':
    app.run(host='127.0.0.1',port='5002')
    # 2024年3月4日晚上18点，我想从Ames Research Center 前往 San Jose的火车站，如何规划路线？
