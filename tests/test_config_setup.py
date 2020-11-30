import unittest
from zeppos_root.root import Root
from zeppos_application.app_config import AppConfig
import os
import tests.config_values as cv

class TestTheProjectMethods(unittest.TestCase):
    def test_environment_files(self):
        all_good = True
        all_good = all_good & self.service_environment_files_verification(
            'local', 'environment_files', 'windows_service_config.json',
            keys={'SERVICE_NAME': cv.service_name, 'APPLICATION_NAME': cv.application_name,
                  'APP_TO_START_CMD': cv.app_to_start_cmd, 'DEBUG_MODE': 'True'}
        )
        all_good = all_good & self.service_environment_files_verification(
            'development', 'environment_files', 'windows_service_config.json',
            keys={'SERVICE_NAME': cv.service_name, 'APPLICATION_NAME': cv.application_name,
                  'APP_TO_START_CMD': cv.app_to_start_cmd, 'DEBUG_MODE': 'True'}
        )
        all_good = all_good & self.service_environment_files_verification(
            'production', 'environment_files', 'windows_service_config.json',
            keys={'SERVICE_NAME': cv.service_name, 'APPLICATION_NAME': cv.application_name,
                  'APP_TO_START_CMD': cv.app_to_start_cmd, 'DEBUG_MODE': 'False'}
        )
        all_good = all_good & self.service_environment_files_verification(
            'local', 'environment_files', 'app_config.json',
            keys={'APPLICATION_NAME': cv.application_name, 'DEBUG_MODE': 'True', 'ENVIRONMENT': 'local' }
        )
        all_good = all_good & self.service_environment_files_verification(
            'development', 'environment_files', 'app_config.json',
            keys={'APPLICATION_NAME': cv.application_name, 'DEBUG_MODE': 'True', 'ENVIRONMENT': 'development'}
        )
        all_good = all_good & self.service_environment_files_verification(
            'production', 'environment_files', 'app_config.json',
            keys={'APPLICATION_NAME': cv.application_name, 'DEBUG_MODE': 'False', 'ENVIRONMENT': 'production'}
        )
        all_good = all_good & self.service_environment_files_verification(
            "", "", 'config.json',
            keys={'SERVICE_NAME': cv.service_name}
        )
        all_good = all_good & self.windows_service_py_verification()

        if all_good:
            print("\n\n***** All Good *****")

    def service_environment_files_verification(self, directory, sub_directory, config_file_name, keys):
        root_dir = Root.find_root_of_project(__file__)
        environment_files_directory = os.path.join(root_dir, sub_directory, directory)
        environment_full_file_name = os.path.join(environment_files_directory, config_file_name)
        error_message = ""
        error_json_config = ""
        if not os.path.exists(environment_full_file_name):
            error_message += f'\tPlease make sure the config file exists [{environment_full_file_name}]\n'
        else:
            try:
                config_dict = \
                    AppConfig.get_json_config_dict(current_module_filename=environment_files_directory,
                                                   config_file_name=config_file_name)
            except:
                config_dict = None


            for key, value in keys.items():
                if config_dict is None or key not in config_dict:
                    error_json_config += f"\tMissing json config value: {key}\n"

            if len(error_json_config) == 0:
                for key, value in keys.items():
                    if value != config_dict[key]:
                        error_message += f'\t[{key}] not equal to "{value}"\n'

        if len(error_json_config) > 0:
            error_message += error_json_config
            error_message += "\n\tExpected something like:\n"
            error_message = "{\n"
            for key, value in keys.items():
                error_message += f'"{key}": "{value}",\n'
            error_message += "}\n"
        if len(error_message) != 0:
            print(f"\n!!!!! Error in [{environment_full_file_name}] !!!!!:\n{error_message}")
            return False
        return True

    def windows_service_py_verification(self):
        root_dir = Root.find_root_of_project(__file__)
        windows_service_full_file_name = os.path.join(root_dir, "windows_service", "windows_service.py")
        error_message = ""
        if not os.path.exists(windows_service_full_file_name):
            error_message += f'\tPlease make sure the windows_service file exists [{windows_service_full_file_name}]\n'
        else:
            with open(windows_service_full_file_name, 'r') as fl:
                lines = fl.read()

            svc_name = None
            svc_display_name = None
            for line in lines.split("\n"):
                if '_svc_name_ =' in line:
                    try:
                        svc_name = line.strip().split('=')[1].split("#")[0].replace('"', '').strip()
                    except:
                        pass
                if '_svc_display_name_ =' in line:
                    try:
                        svc_display_name = line.strip().split('=')[1].split("#")[0].replace('"', '').strip()
                    except:
                        pass

            if not svc_name:
                error_message += f"\tMissing _svc_name_ = in [{windows_service_full_file_name}]\n"

            if not svc_display_name:
                error_message += f"\tMissing _svc_display_name_ = in [{windows_service_full_file_name}]\n"

            if svc_name and svc_name != cv.service_name:
                error_message += f"\t_svc_name_ is '{svc_name}' and must be equal to '{cv.service_name}' in [{windows_service_full_file_name}]\n"

            if svc_display_name and svc_display_name != cv.service_display_name:
                error_message += f"\t_svc_display_name_ is '{svc_display_name}' must be equal to '{cv.service_display_name}' in [{windows_service_full_file_name}]\n"

        if len(error_message) != 0:
            print(f"\n!!!!! Error in [{windows_service_full_file_name}] !!!!!:\n{error_message}")
            return False
        return True



if __name__ == '__main__':
    unittest.main()