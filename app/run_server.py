import sys
import traceback
from datetime import datetime
import time
import os
import psutil
from zeppos_logging.app_logger import AppLogger
from zeppos_logging.app_logger_json_conifg_name import AppLoggerJsonConfigName
from zeppos_application.app_config import AppConfig


class RunServer:
    def __init__(self):
        AppLogger.logger.debug("******* STARTING APP *******")
        AppLogger.logger.debug("Initializing application.")
        self._application_name = RunServer.get_config_values()

    @staticmethod
    def get_config_values():
        AppLogger.logger.debug("Get config values.")
        config_dict = AppConfig.get_json_config_dict(__file__)
        application_name = config_dict['APPLICATION_NAME']
        AppLogger.logger.debug(f"Application Name: {application_name}")
        return application_name

    def run_waitress_server(self):
        AppLogger.logger.debug('Entering run_waitress_server')
        try:
            if not self._is_app_running():
                AppLogger.logger.debug(f"The app is not running! Let's start it")
                self._create_pid_file()

                while True:
                    date_string = datetime.now().strftime("%m/%d/%YT%H:%M:%S")
                    AppLogger.logger.debug(f'still alive: {date_string}')
                    time.sleep(3)
        except Exception as e:
            AppLogger.logger.error(
                f'Error run_waitress_server: [{e}] - LineNo: [{sys.exc_info()[-1].tb_lineno}] \n\r '
                f'{traceback.print_exc(file=sys.stdout)}')

        AppLogger.logger.debug('Exiting run_waitress_server')

    def __del__(self):
        AppLogger.logger.debug("__del__")
        AppLogger.logger.debug("******* ENDING APP *******")

    def _is_app_running(self):
        proc_object = self._get_proc_object()
        if proc_object:
            return proc_object.status().upper() == "RUNNING"
        return False

    def _get_pid_full_file_name(self):
        current_user_directory = os.path.expanduser("~")
        directory = os.path.join(current_user_directory, ".pidfile")
        pid_file_name = f'{self._application_name}.pid'
        full_file_name = os.path.join(directory, pid_file_name)
        os.makedirs(os.path.dirname(full_file_name), exist_ok=True)
        return full_file_name

    def _create_pid_file(self):
        pid_id = os.getpid()
        pid_full_file_name = self._get_pid_full_file_name()
        AppLogger.logger.debug(f"creating pid_file [{pid_full_file_name}] with pid_id [{pid_id}]")
        with open(pid_full_file_name, 'w') as fl:
            fl.writelines(str(pid_id))

    def _get_proc_object(self):
        proc_object = None
        pid_full_file_name = self._get_pid_full_file_name()
        if os.path.exists(pid_full_file_name):
            try:
                with open(pid_full_file_name, 'r') as fl:
                    pid_str = fl.readline()  # separate lines for easier debugging thru logs
                    pid = int(pid_str)

                for proc in psutil.process_iter():
                    if proc.pid == pid:
                        proc_object = proc
            except Exception as error:
                AppLogger.logger.error(f"Application | {self._application_name} | {error}")
        return proc_object


if __name__ == '__main__':
    AppLogger.configure_and_get_logger(
        'run_server',
        AppLoggerJsonConfigName.default_with_watchtower_format_1(),
        watchtower_log_group="windows_service_template",
        watchtower_stream_name="local"
    )
    AppLogger.set_debug_level()
    RunServer().run_waitress_server()
