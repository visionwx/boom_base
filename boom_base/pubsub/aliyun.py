import sys
import json
from boom_base.mns_python_sdk.mns.account import Account
from boom_base.mns_python_sdk.mns.topic import TopicMessage
from boom_base.mns_python_sdk.mns.mns_exception import MNSExceptionBase
from boom_base.pubsub.base import AbstractPubsubService
from boom_base import config
from typing import Dict


class AliyunPubsubService(AbstractPubsubService):
    def __init__(self):
        accessKeyId = config.get_aliyun_access_key_id()
        accessKeySecret = config.get_aliyun_access_key_secret()
        endpoint = config.get_aliyun_mns_endpoint()
        self.my_account = Account(endpoint, accessKeyId, accessKeySecret)
    
    def publish(self, topicName: str, data: Dict):
        try:
            my_topic = self.my_account.get_topic(topicName)
            msg_body = json.dumps(data)
            msg = TopicMessage(msg_body)
            re_msg = my_topic.publish_message(msg)
            print(f"Publish Message Succeed. MessageBody:{msg_body} MessageID:{re_msg.message_id}")
        except MNSExceptionBase as e:
            if e.type == "TopicNotExist":
                print("Topic not exist, please create it.")
                sys.exit(1)
            print(f"Publish Message Fail. Exception:{e}")


if __name__ == '__main__':
    pubsub = AliyunPubsubService()

    topicName = 'BoomUatVideoCommented'
    data = {
        "userId": "618272744b6103234df1f771",
        "content": {
            "en": "sint",
            "zh": "dolor nisi in"
        },
        "object": {
            "en": "test MNS publish 01",
            "zh": "测试MNS发布消息01"
        },
        "from": {
            "userId": "618272744b6103234df1f772",
            "name": "Hello World",
            "avatarUrl": "http://dummyimage.com/100x100"
        },
        "type": 0,
        "extraData": {
            "action": {
                "code": "videos.get",
                "params": {
                    "videoId": "123123"
                }
            }
        }
    }
    pubsub.publish(topicName, data)
