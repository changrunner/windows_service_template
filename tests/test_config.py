import unittest
from windows_service.zzz_windows_service_template import WindowsService
import os


class TestTheProjectMethods(unittest.TestCase):
    def test_get_configuration_file_name_method(self):
        self.assertEqual(f"config_{WindowsService.get_service_name()}.json",
                         WindowsService.get_configuration_file_name())

    def test_get_configuration_directory_method(self):
        self.assertEqual(True, os.path.exists(
            WindowsService.get_configuration_directory()))

    def test_get_configuration_full_file_name_method(self):
        self.assertEqual(True, os.path.exists(
            WindowsService.get_configuration_full_file_name()))

    def test_get_configuration_values_method(self):
        service_name, application_name, app_to_start_cmd, debug_mode = \
            WindowsService.get_configuration_values()
        self.assertEqual(WindowsService.get_service_name(), service_name)
        self.assertEqual(True, len(application_name) > 0)
        self.assertEqual(True, len(app_to_start_cmd) > 0)
        self.assertEqual(True, len(debug_mode) > 0)


if __name__ == '__main__':
    unittest.main()