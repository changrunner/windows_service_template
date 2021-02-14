import unittest
from windows_service import WindowsService


class TestTheProjectMethods(unittest.TestCase):
    def test_get_configuration_values_method(self):
        debug_mode, application_name, app_to_start_cmd = \
            WindowsService.get_config_values()
        self.assertEqual("zzz_windows_service_template_app", application_name)
        self.assertEqual("zzz_windows_service_template_app_start_me.bat", app_to_start_cmd)
        self.assertEqual(True, debug_mode)


if __name__ == '__main__':
    unittest.main()
