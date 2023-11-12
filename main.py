import ast
import pika
import concurrent.futures
from db_conn import db
from table_models import LogTable
from datetime import datetime

class Consumer:
    def __init__(self, queue_name):
        self.__url = '192.168.222.116'
        self.__port = 5672
        self.__vhost = 'alwayswas'
        self.__cred = pika.PlainCredentials('admin', 'Admin2023!)')
        self.__queue =  queue_name
        self.connection = None
        self.channel = None

    def connect(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.__url, self.__port, self.__vhost, self.__cred))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.__queue, durable=True)

    def callback(self, ch, method, properties, body):
        print(f"Received message: {body.decode('utf8')}")
        input_string = body.decode('utf8')
        ast_node = ast.parse(input_string, mode='eval')
        # AST 노드를 딕셔너리로 변환
        result_dict = ast.literal_eval(ast_node.body)
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y%m%d%H%M%S.%f")

        session = next(db.session())
        log = LogTable(
            logtime=formatted_datetime,
            log_user=result_dict.get("client",'').get("user"),
            log_desc=input_string,
            api_uri=result_dict.get("url"),
        )
        session.add(log)
        session.commit()

    def start_consuming(self):
        self.channel.basic_consume(queue=self.__queue, on_message_callback=self.callback, auto_ack=True)
        self.channel.start_consuming()

    def close_connection(self):
        if self.connection and self.connection.is_open:
            self.connection.close()

def consume(queue_name):
    consumer = Consumer(queue_name)
    consumer.connect()
    try:
        consumer.start_consuming()
    except KeyboardInterrupt:
        consumer.close_connection()

if __name__ == "__main__":
    queue_name = 'always_log'  # 적절한 queue 이름으로 수정

    # 멀티프로세스로 컨슈머 실행
    with concurrent.futures.ProcessPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(consume, queue_name) for _ in range(3)]  # 3개의 프로세스로 실행

        # 프로세스가 완료될 때까지 대기
        try:
            concurrent.futures.wait(futures)
        except KeyboardInterrupt:
            pass
