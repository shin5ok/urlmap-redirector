from google.cloud import pubsub_v1
from concurrent import futures

class Pub():

    def __init__(self, project_id, topic_id):
        publisher = pubsub_v1.PublisherClient()
        self.topic_path = publisher.topic_path(project_id, topic_id)
        self.publisher = publisher
        self.publish_futures = []

    def get_callback(self, publish_future, data):
        def callback(publish_future):
            try:
                print(publish_future.result(timeout=60))
            except publish_future.TimeoutError:
                print(f"Publishing {data} timed out.")
        return callback


    def run(self, message):
        import asyncio
        data = message.encode("utf-8")
        try:
            publish_future = self.publisher.publish(
                self.topic_path, data, invoker=__file__,
            )
            publish_future.add_done_callback(self.get_callback(publish_future, data))
            self.publish_futures.append(publish_future)
            futures.wait(self.publish_futures, return_when=futures.ALL_COMPLETED)
        except Exception as e:
            print(str(e))
            return False
        print(f"Published messages with custom attributes to {self.topic_path}.")
        return True