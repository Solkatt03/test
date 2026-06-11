import os
import argparse
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

REGION = os.getenv("ALIYUN_REGION", "cn-hangzhou")

def make_client():
    ak = os.getenv("ALIYUN_ACCESS_KEY_ID")
    secret = os.getenv("ALIYUN_ACCESS_KEY_SECRET")
    if not ak or not secret:
        raise SystemExit("Missing ALIYUN_ACCESS_KEY_ID or ALIYUN_ACCESS_KEY_SECRET")
    return AcsClient(ak, secret, REGION)

def trigger_flow(client, project, flow_id):
    req = CommonRequest()
    req.set_accept_format('json')
    req.set_domain('dataworks-public.cn-hangzhou.aliyuncs.com')
    req.set_method('POST')
    req.set_version('2018-06-01')
    req.set_action_name('CreateFlowInstance')  
    req.add_query_param('ProjectName', project)
    req.add_query_param('FlowId', flow_id)
    resp = client.do_action_with_exception(req)
    print("CreateFlowInstance response:", resp.decode() if isinstance(resp, bytes) else resp)
    return resp

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--flow-id", required=True)
    args = parser.parse_args()
    client = make_client()
    trigger_flow(client, args.project, args.flow_id)

if __name__ == "__main__":
    main()
# ...existing code...
