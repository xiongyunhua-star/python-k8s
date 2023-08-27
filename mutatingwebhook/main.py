from flask import Flask, request, jsonify
import base64
import jsonpatch
app = Flask(__name__)
@app.route('/mutate', methods=['POST'])
def mutate_pod():
    print(request.host)
    # 解析请求中的数据
    request_data = request.get_json()
    print(type(request_data))
    for i in request_data:
        print(i, request_data[i])
    for key, val in request_data['request'].items():
        print(key, val)
    pod = request_data['request']['object']
    # 在这里添加您的修改逻辑
    pod['metadata'].setdefault('labels', {})
    pod['metadata']['labels']['my_name'] = 'xiongyunhua'
    # 创建一个JSON Patch对象
    patch = jsonpatch.JsonPatch([
        {"op": "add", "path": "/metadata/labels/my_name", "value": "xiongyunhua"}
    ])
    patch_str = patch.to_string()
    # 返回修改后的Pod对象和JSON Patch
    response = {
        'response': {
            'allowed': True,
            'patchType': 'JSONPatch',
            'patch': base64.b64encode(patch_str.encode()).decode()
        }
    }
    return jsonify(response)
if __name__ == '__main__':
    ssl_context = ("./certs/newcert.crt","./certs/private.key")
    app.run(host='0.0.0.0', port=8080,ssl_context=ssl_context)
