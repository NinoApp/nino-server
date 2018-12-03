from threading import Thread
from nino_pipeline import NinoPipeline
from nino_object import NinoObject
from nino_utils import *
class RequestThread(Thread):
    # Implement producer consumer here.
    def __init__(self, queue, modules):
        Thread.__init__(self)
        self.queue = queue
        self.modules = modules

    def run(self):
        initial_image = "INITIAL_IMAGE"
        username = "USERNAME"
        request_id = "REQUEST_ID"
        print('Running request for user ' + username +
        " with request id #" + request_id)

        # Create NinoObject with a name and initial image
        no = NinoObject(request_id, initial_image) # Temp solution for com

        # Create NinoPipeline with modules and NinoObject
        np = NinoPipeline(no, self.modules)
        np.run() # Start processsing

        self.queue.put(no)
