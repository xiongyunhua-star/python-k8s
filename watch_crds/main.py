from kubernetes import client, config, watch

# 配置Kubernetes客户端
config.load_kube_config("./kube/kubeconfig.json")
v1 = client.CoreV1Api()
crd_client = client.CustomObjectsApi()

# 自定义资源组、版本和资源类型
group = 'vmapp.apphub.epscp.com'
version = 'v1'
resource = 'vmdeploys'

def node_set_lable(nodeName:list[str], body:dict):
    for ip_str in nodeName:
        try:
            response = v1.patch_node(ip_str, body)
        except Exception as e:
            print(e)
        else:
            if response :
                print(f'节点 {ip_str} 已被设置部署标签')
def process_custom_resource(event):
    # print(event)
    obj = event['object']
    # print(obj)
    object_name = obj['metadata']['name']
    object_namespace = obj['metadata']['namespace']

    if event['type'] == 'ADDED':

        # 处理自定义资源创建
        # 可以在这里执行你的业务逻辑或对其他Kubernetes资源进行操作
        node_ip = obj['spec']['nodeSelector']['nodeNames']

        print(f'Added Custom Resource: {object_name} in namespace {object_namespace}, NodeIp: {node_ip}.')
        # 实现node打标签label
        body = {
            "metadata": {
                "labels": {
                    "has_deployed": "true"
                }
            }
        }
        node_set_lable(node_ip,body)
    elif event['type'] == 'MODIFIED':
        print(f'Modified Custom Resource: {object_name} in namespace {object_namespace}.')

    elif event['type'] == 'DELETED':
        print(f'Deleted Custom Resource: {object_name} in namespace {object_namespace}.')
        # 处理自定义资源删除
        # 可以在这里执行你的业务逻辑或对其他Kubernetes资源进行操作
# 创建自定义资源监听器
def watch_custom_resource():
    resource_api_version = f'{group}/{version}'
    print(resource_api_version)
    w = watch.Watch()
    for event in w.stream(crd_client.list_cluster_custom_object, group, version, resource):
        process_custom_resource(event)

# 启动自定义资源监听
if __name__ == '__main__':
    watch_custom_resource()
