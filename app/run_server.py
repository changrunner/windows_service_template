from datetime import datetime
import time
from zeppos_logging.app_logger import AppLogger
from run_app_base import RunAppBase


class RunServer(RunAppBase):
    def __init__(self):
        super().__init__()

    def run_server(self):
        if super().start_app():
            # ####################
            while True:
                date_string = datetime.now().strftime("%m/%d/%YT%H:%M:%S")
                AppLogger.logger.debug(f'still alive: {date_string}')
                time.sleep(3)
            # ####################


if __name__ == '__main__':
    RunAppBase.main('run_server')
    RunServer().run_server()

