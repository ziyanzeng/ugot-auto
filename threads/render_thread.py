import threading
from config import shared_data

class RenderFrame(threading.Thread):
    def __init__(self, thread_name, render_queue):
        threading.Thread.__init__(self, name=thread_name)
        self.render_queue = render_queue

    def run(self):
        while True:
            with shared_data["lock"]:
                if shared_data["exit"]:
                    break

                frame = shared_data["frame"]
                if frame is not None:
                    self.render_queue.put(frame)
