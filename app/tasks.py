import time
import rq


def example(seconds):

    def update_meta(msg):
        job.meta['progress'] = msg
        job.save_meta()

    job = rq.get_current_job()
    print('Starting task')
    for i in range(seconds):
        update_meta(100.0  * i / seconds)
        print(i)
        time.sleep(1)
    update_meta(100)
    print('Task completed')

