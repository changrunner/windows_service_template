import unittest
from windows_service.windows_service import WindowsService
import os


class TestTheProjectMethods(unittest.TestCase):
    def test__get_configuration_file_name_method(self):
        self.assertEqual(f"config_{WindowsService.get_service_name()}.json",
                         WindowsService._get_configuration_file_name()
                         )

    def test__get_configuration_directory_method(self):
        self.assertEqual(True, os.path.exists(
            WindowsService._get_configuration_directory()))

    def test_get_configuration_full_file_name_method(self):
        self.assertEqual(True,
                         os.path.exists(
                             WindowsService.get_configuration_full_file_name()
                         )
                         )

    def test__get_config_dict_method(self):
        self.assertEqual(True,
                         isinstance(
                             WindowsService._get_config_dict(),
                             dict
                         )
                         )
        self.assertEqual(4,
                         len(WindowsService._get_config_dict())
                         )
    def test_get_configuration_values_method(self):
        service_name, application_name, app_to_start_cmd, debug_mode = \
            WindowsService.get_configuration_values()
        self.assertEqual(WindowsService.get_service_name(), service_name)
        self.assertEqual(True, len(application_name) > 0)
        self.assertEqual(True, len(app_to_start_cmd) > 0)
        self.assertEqual('True', debug_mode)


if __name__ == '__main__':
    unittest.main()