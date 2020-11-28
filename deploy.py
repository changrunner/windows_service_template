from subprocess import Popen, PIPE
import os
from shutil import copy, rmtree
from zeppos_application.app_config import AppConfig
from zeppos_root.root import Root
from zeppos_logging.app_logger import AppLogger


def copy_config_file(root_dir, service_name):
    AppLogger.logger.debug("=> Copy config.json files")
    base_directory = os.path.join(os.path.expanduser('~'), '.config')
    os.makedirs(base_directory, exist_ok=True)
    source_file = os.path.join(root_dir, 'environment_files/local/config.json')
    destination_file = os.path.join(base_directory, f"config_{service_name}.json")
    AppLogger.logger.debug(f"Copying [{source_file}] to [{destination_file}]")
    copy(source_file, destination_file)
    AppLogger.logger.debug(f"Copied file [{source_file}] to [{destination_file}]")
    AppLogger.logger.debug("-" * 80)


def get_directories():
    AppLogger.logger.debug("====> Get directories")
    root_dir = Root.find_root_of_project(__file__)  # this will use the .root file.
    AppLogger.logger.debug(f"root_dir: {root_dir}")

    current_dir = os.path.join(root_dir, "windows_service")
    AppLogger.logger.debug(f"current_dir: {current_dir}")

    return root_dir, current_dir


def get_config_values(root_dir):
    AppLogger.logger.debug("====> Get config values")
    config_dict = AppConfig.get_json_config_dict(root_dir)  # this will use the config.json in the
    service_name = config_dict['SERVICE_NAME']
    AppLogger.logger.debug(f"======> service_name: {service_name}")
    return service_name


def test_passed():
    AppLogger.logger.debug("====> Run tests")

    p = Popen(['pipenv', 'run', 'pytest'], stdout=PIPE)
    out, err = p.communicate()
    if out:
        out_array = out.decode("utf-8").split('\r\n')

        if "passed" in out_array[len(out_array) - 2]:
            AppLogger.logger.debug("======> Test Passed")
            return True

    AppLogger.logger.debug("======> Test Failed")
    return False


def remove_previous_deploy_directories(root_dir):
    AppLogger.logger.debug("====> Remove directories")
    AppLogger.logger.debug("======> Remove directory dist")
    if os.path.exists(os.path.join(root_dir, 'dist')):
        rmtree(os.path.join(root_dir, 'dist'))

    AppLogger.logger.debug("======> Remove directory build")
    if os.path.exists(os.path.join(root_dir, 'build')):
        rmtree(os.path.join(root_dir, 'build'))


def build_windows_service(current_dir, service_name):
    AppLogger.logger.debug("====> Build the windows service")
    p = Popen(['pipenv', 'run', 'pyinstaller', '-F', '--hidden-import=win32timezone', os.path.join(current_dir, service_name + '.py')], stdout=PIPE)
    p.communicate()


def main():
    AppLogger.logger.debug("==> ***** DEPLOY WINDOWS SERVICE - STARTED ***** <==")

    root_dir, current_dir = get_directories()
    service_name = get_config_values(root_dir)

    copy_config_file(root_dir, service_name)

    remove_previous_deploy_directories(root_dir)

    if test_passed():
        build_windows_service(current_dir, service_name)

    AppLogger.logger.debug("==> ***** DEPLOY WINDOWS SERVICE - COMPLETED ***** <==")


if __name__ == '__main__':
    AppLogger.configure_and_get_logger('deploy')
    AppLogger.set_debug_level()
    main()