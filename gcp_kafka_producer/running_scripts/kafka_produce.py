import threading
from threading import Thread
from datetime import datetime
import time as t
# pip3 install kafka-python
from kafka import KafkaProducer
import json
import random
from argparse import ArgumentParser


parser = ArgumentParser()
parser.add_argument("--host", help="kafka server host", dest="host", default="kafka.mlytics.us")
parser.add_argument("--topic", help="topic of the kafka", dest="topic", default="wafaccess")
parser.add_argument("--thread", help="thread number", dest="thread", default=1, type=int)
parser.add_argument("--timeunit", help="per (time unit) seconds", dest="timeunit", default=0.5, type=float)
parser.add_argument("--messages", help="send (messages) messages in (timeunit) seconds", dest="messages", default=100, type=int)
parser.add_argument("--duration", help="duration count", dest="duration", default=40, type=int)

args = parser.parse_args()

# kafka_server = 'kafka.mlytics.us:9092'
kafka_server = args.host + ':9092'

kafka_topic = args.topic

thread_count = args.thread

# unit: seconds; send <message_per_run> messages per <message_burst_time_unit>, with total <message_burst_duration> times
message_burst_time_unit = args.timeunit

message_per_run = args.messages

message_burst_duration = args.duration


sample = {
    '@timestamp': '2018-09-06T10:38:18.366Z',
    '@metadata': {
        'beat': 'filebeat',
        'type': 'doc',
        'version': '6.2.3',
        'topic': 'wafaccess'
    },
    'request_time': 0.004,
    'query_string': 'rnd=0-1-20591-1-20591-37484-4099331167-_CgJqMRAUGF8iBggBEO-gASjfqNuiDzDm4V04mIfE3AVAw5ns6QVKEQgDENsBGIj8AiAAKP2RgKAEUABaCggAEAAYACAAKABgAWoaYnV0dG9uLXdvcmtlcjEuYW1zLmh2LnByb2SCAREIAxDbARjJxQwgACj9kYCgBIgBuf3e1AmQAQCYAQA',
    'sender': 'wafaccess',
    'upstream_response_time': '0.004',
    'prospector': {
        'type': 'log'
    },
    'request_length': '1051',
    'server_protocol': 'HTTP/1.1',
    'upstream_addr': '52.175.21.175:443',
    'source': '/usr/local/nginx/logs/access.log',
    'bytes_sent': 543,
    'scheme': 'https',
    'http_user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    'sent_http_content_type': 'text/html',
    'request_host': 'test-mlytics-cdn.fjla37itnf5dpsen.com',
    'http_referer': 'https://www.188bet.com/en-gb/sports/getbanner?id=sbk-right',
    'host': 'hk-wafnginx-3',
    'upstream_status': '200',
    'upstream_connect_time': '0.000',
    'server_addr': '10.80.3.227',
    'zone_id': 'test-mlytics-cdn.fjla37itnf5dpsen.com',
    'cdn_node_ip': '35.158.136.232',
    'offset': 8267558,
    'upstream_response_length': '327',
    'uri': '/inav.html',
    'remote_addr': '35.158.136.232',
    'realip_remote_addr': '35.158.136.232',
    'upstream_header_time': '0.004',
    'beat': {
        'name': 'hk-wafnginx-3',
        'hostname': 'hk-wafnginx-3',
        'version': '6.2.3'
    },
    'request_method': 'GET',
    'body_bytes_sent': 339,
    'status': '200',
    'time': '2018-09-06T18:38:18+08:00',
    'http_x_forwarded_for': '185.190.151.154',
    'request_id': 'c642c910cf814db3e646f950639be50f'
}

# Send data to kafka

dest_pool = [
    '1.1.1.1',
    '1.1.1.2',
    '1.1.1.3',
    '1.1.1.4',
    '1.1.1.5',
    '1.1.1.6'
]

source_pool = [
    '2.1.1.1',
    '2.1.1.2',
    '2.1.1.3',
    '2.1.1.4',
    '2.1.1.5',
    '2.1.1.6',
    '2.1.1.7',
    '2.1.1.8'
]



def mock_data(upstream_addr, http_x_f, time):
    d = sample.copy()
    d['http_x_forwarded_for'] = http_x_f
    d['upstream_addr'] = upstream_addr
    d['time'] = time
    return d


def now_iso():
    return datetime.now().strftime('%Y-%m-%dT%H:%M:%S+08:00')



def get_rand_from_list(list_data):
    r = random.randint(0, len(list_data) - 1)
    return list_data[r]

def thread_handler(topic, sleep_time, loop_count):
    current_id = threading.get_ident()
    kafka_producer = KafkaProducer(bootstrap_servers=kafka_server)
    c = 0
    while c < loop_count:
        start_p_time = datetime.now()
        up_addr = get_rand_from_list(dest_pool)
        http_x_f = get_rand_from_list(source_pool)
        time = now_iso()
        mock = mock_data(up_addr, http_x_f, time)

        for i in range(0, message_per_run):
            kafka_producer.send(topic, json.dumps(mock).encode())
        end_p_time = datetime.now()

        c += 1
        remaining_time = (end_p_time - start_p_time).total_seconds()
        # print('id', current_id, 'time', remaining_time)
        t.sleep(max(sleep_time - remaining_time, 0))

    print('Thread leaves')

# up_addr = get_rand_from_list(dest_pool)
# http_x_f = get_rand_from_list(source_pool)
# time = now_iso()
# mock = mock_data(up_addr, http_x_f, time)

# thread_handler(producer, 'wafaccess', json.dumps(mock).encode())


for i in range(thread_count):
    thread = Thread(target = thread_handler, args = [kafka_topic, message_burst_time_unit, message_burst_duration])
    thread.start()
