import unittest
from windows_service.zzz_windows_service_template import WindowsService
from zeppos_logging.app_logger import AppLogger
from testfixtures import LogCapture
import os

class TestTheProjectMethods(unittest.TestCase):
    def test_windows_service_name_method(self):
        self.assertEqual("zzz_windows_service_template", WindowsService.get_service_name())

    def test_constructor_method(self):
        AppLogger.configure_and_get_logger("windows_service")
        windows_service = WindowsService(None)
        self.assertEqual("windows_service_template", windows_service.application_name)
        self.assertEqual("windows_service_test.bat", windows_service.app_to_start_cmd)
        self.assertEqual("True", windows_service.debug_mode)

    # Below tests are not deploy Friendly
    # def test_1_kill_app_method(self):
    #     AppLogger.configure_and_get_logger(logger_name='test_simple')
    #     AppLogger.set_debug_level()
    #     windows_service = WindowsService(None)
    #     pidfile = windows_service._pid_full_file_name
    #     if os.path.exists(pidfile):
    #         os.remove(pidfile)
    #
    #     with LogCapture() as lc:
    #         windows_service.kill_app()
    #         lc.check(
    #             ('test_simple', 'DEBUG', "Entering kill_app"),
    #             ('test_simple', 'DEBUG', "pid_file_not found | windows_service_template.pid"),
    #             ('test_simple', 'DEBUG', "Exiting kill_app"),
    #         )
    #
    # def test_2_kill_app_method(self):
    #     AppLogger.configure_and_get_logger(logger_name='test_simple')
    #     AppLogger.set_debug_level()
    #     windows_service = WindowsService(None)
    #     pidfile = windows_service._pid_full_file_name
    #     if os.path.exists(pidfile):
    #         os.remove(pidfile)
    #     with open(pidfile, 'w') as fl:
    #         fl.write("12")
    #
    #     with LogCapture() as lc:
    #         windows_service.kill_app()
    #         print(lc)
    #
    #         # lc.check(
    #         #     ('test_simple', 'DEBUG', "Entering kill_app"),
    #         #     ('test_simple', 'DEBUG', "pid | 12"),
    #         #     ('test_simple', 'DEBUG', "Exiting kill_app"),
    #         # )
    #
    # def test__pid_full_file_name_method(self):
    #     windows_service = WindowsService(None)
    #     self.assertEqual("windows_service_template.pid", os.path.basename(windows_service._pid_full_file_name))


if __name__ == '__main__':
    unittest.main()