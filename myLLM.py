from http import HTTPStatus
import dashscope

dashscope.api_key = ''  # 替换为个人的api


def call_with_messages():
    messages = [{'role': 'system',
                 'content': '''你是一个经验丰富的交通规划专家，专注于高速公路交通状态预测。
                 你的任务是利用美国加利福尼亚州交通局发布的交通数据，分析并预测旧金山湾区南湾Sunnyvale和San Jose地区的交通状况。
                 你将使用自2024年1月1日至2024年6月30日期间，325个交通传感器采集的车速和车流量数据。
                 你的目标是提供准确的交通状态预测和优化出行建议，帮助用户在该地区的高速公路上安全、高效地出行。'''},
                {'role': 'user', 'content': '我如何从 Ames Research Center 前往 San Jose？'}]

    response = dashscope.Generation.call(
        dashscope.Generation.Models.qwen_max,
        messages=messages,
        result_format='message',
        workspace=''  # 替换个人工作空间id
    )
    if response.status_code == HTTPStatus.OK:
        print(response)
        content = response["output"]["choices"][0]["message"]["content"]
        print(content)
    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))


if __name__ == '__main__':
    call_with_messages()
