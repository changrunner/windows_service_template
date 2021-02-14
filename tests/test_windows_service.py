import unittest
from windows_service import WindowsService
from zeppos_logging.app_logger import AppLogger
import os


class TestTheProjectMethods(unittest.TestCase):
    def test_windows_service_name_method(self):
        self.assertEqual("zzz_windows_service_template", WindowsService.get_service_name())

    def test_constructor_method(self):
        AppLogger.configure_and_get_logger("windows_service")
        windows_service = WindowsService(None)
        self.assertEqual("zzz_windows_service_template_app", windows_service.application_name)
        self.assertEqual("zzz_windows_service_template_app_start_me.bat", windows_service.app_to_start_cmd)
        self.assertEqual(True, windows_service.debug_mode)

    def test__pid_full_file_name_method(self):
        self.assertEqual(['.pidfile'],
                         WindowsService.get_pid_full_file_name('zzz_windows_service_template').replace('\\', '/').split(
                             '/')[3:4]
                         )
        self.assertEqual(['C:', 'Users'],
                         WindowsService.get_pid_full_file_name('zzz_windows_service_template').replace('\\', '/').split(
                             '/')[0:2]
                         )
        self.assertEqual(5,
                         len(WindowsService.get_pid_full_file_name('zzz_windows_service_template').replace('\\',
                                                                                                           '/').split(
                             '/'))
                         )
        self.assertEqual("zzz_windows_service_template.pid",
                         os.path.basename(WindowsService.get_pid_full_file_name('zzz_windows_service_template')))

    def test_get_proc_object_method(self):
        self.assertEqual(None, WindowsService.get_proc_object("zzz_windows_service_template"))

    def test_kill_app_method(self):
        WindowsService.kill_app("zzz_windows_service_template")
        self.assertEqual(True, 1 == 1)

    def test_is_running_method(self):
        self.assertEqual(False, WindowsService.is_running("zzz_windows_service_template"))

    def test_stop_the_process_method(self):
        WindowsService.stop_the_process("zzz_windows_service_template")
        self.assertEqual(True, 1 == 1)


if __name__ == '__main__':
    unittest.main()
