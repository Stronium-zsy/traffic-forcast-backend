from flask import Flask, request, jsonify
from flask_cors import CORS
import redis
import json
from geopy.distance import geodesic

app = Flask(__name__)
CORS(app)

# 初始化 Redis 连接
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

# 加载 reachable_sensors 数据
with open('reachable_sensors.json', 'r') as file:
    reachable_sensors = json.load(file)


@app.route('/search_route', methods=['POST'])
def search_route():
    data = request.json
    start_point = data.get('startPoint')
    end_point = data.get('endPoint')

    if not start_point or not end_point:
        return jsonify({'error': 'Invalid start or end point'}), 400

    route = find_route(start_point, end_point)

    if not route:
        return jsonify({'route': None}), 404

    return jsonify({'route': route})

def find_route(start, end):
    open_set = {start}
    came_from = {}

    g_score = {start: 0}
    f_score = {start: heuristic_cost_estimate(start, end)}

    while open_set:
        current = min(open_set, key=lambda x: f_score.get(x, float('inf')))
        print(f"Current node: {current}")

        if current == end:
            return reconstruct_path(came_from, current)

        open_set.remove(current)

        # 从 reachable_sensors 获取邻居传感器的数据
        neighbors = reachable_sensors.get(current, [])
        for neighbor in neighbors:
            neighbor_id = neighbor['sensor_id']
            neighbor_distance = neighbor['distance']
            neighbor_speed = float(redis_client.hget(f"sensor:{neighbor_id}", 'speed') or 1)  # 如果没有找到速度，默认值为1
            print(f"Neighbor ID: {neighbor_id}, Distance: {neighbor_distance}, Speed: {neighbor_speed}")

            tentative_g_score = g_score[current] + neighbor_distance / neighbor_speed
            print(f"Tentative g_score for {neighbor_id}: {tentative_g_score}")

            if tentative_g_score < g_score.get(neighbor_id, float('inf')):
                came_from[neighbor_id] = current
                g_score[neighbor_id] = tentative_g_score
                f_score[neighbor_id] = tentative_g_score + heuristic_cost_estimate(neighbor_id, end)
                open_set.add(neighbor_id)
                print(f"Updated g_score for {neighbor_id}: {g_score[neighbor_id]}")
                print(f"Updated f_score for {neighbor_id}: {f_score[neighbor_id]}")

    return []

def heuristic_cost_estimate(start, end):
    start_pos = get_position(start)
    end_pos = get_position(end)
    distance = geodesic(start_pos, end_pos).kilometers
    avg_speed = float(redis_client.hget(f"sensor:{start}", 'speed') or 1)  # 如果没有找到速度，默认值为1
    heuristic = distance / avg_speed
    print(f"Heuristic cost estimate from {start} to {end}: {heuristic}")
    return heuristic

def get_position(sensor_id):
    sensor_data = redis_client.hgetall(f"sensor:{sensor_id}")
    if sensor_data:
        position = (float(sensor_data[b'latitude']), float(sensor_data[b'longitude']))
        print(f"Position for sensor {sensor_id}: {position}")
        return position
    return None

def reconstruct_path(came_from, current):
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.insert(0, current)
    print(f"Reconstructed path: {total_path}")
    return total_path

if __name__ == '__main__':
    app.run(debug=True, port=4999)
