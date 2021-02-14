from subprocess import Popen, PIPE
import os
import sys
from shutil import copy, rmtree
from zeppos_application.app_config import AppConfig
from zeppos_root.root import Root
from zeppos_logging.app_logger import AppLogger
from glob import glob
import chang_me
from zeppos_git.branch import Branch


def create_config_file():
    AppLogger.logger.debug(f"=> Create config_{chang_me.service_name}.json file")
    base_directory = os.path.join(os.path.expanduser('~'), '.config')
    os.makedirs(base_directory, exist_ok=True)
    destination_file = os.path.join(base_directory, f"config_{chang_me.service_name}.json")
    AppLogger.logger.debug(f"Creating content for [{destination_file}]")

    content = f'{{\n'
    content += f'\t"ENVIRONMENT": "{Branch.get_current()}",\n'
    content += f'\t"DEBUG_MODE": "{chang_me.service_debug_mode}"\n'
    content += f'}}\n'

    with open(destination_file, 'w') as fl_w:
        fl_w.write(content)

    with open(destination_file, 'r') as fl_r:
        AppLogger.logger.debug(f"content: \n{fl_r.read()}\n")

    AppLogger.logger.debug(f"=> Created config_{chang_me.service_name}.json file")
    AppLogger.logger.debug("-" * 80)


def create_bat_file():
    AppLogger.logger.debug(f"=> Create {chang_me.service_name}_app_start_me.bat file if not exist")
    base_directory = "c:\\windows\\system32"
    destination_file = os.path.join(base_directory, f"{chang_me.service_name}_app_start_me.bat")
    if not os.path.exists(destination_file):
        AppLogger.logger.debug(f"Creating content for [{destination_file}]")
        root_dir = Root.find_root_of_project(__file__)

        content = f'{root_dir.split(":")[0]}:\n'
        content += f'cd {root_dir.split(":")[1]}\\app\n'
        content += f'pipenv run python run_server.py'

        with open(destination_file, 'w') as fl_w:
            fl_w.write(content)
        AppLogger.logger.debug(f"=> Created {chang_me.service_name}_app_start_me.bat file")

    with open(destination_file, 'r') as fl_r:
        AppLogger.logger.debug(f"content: \n{fl_r.read()}")

    AppLogger.logger.debug("-" * 80)


def remove_previous_deploy_directories():
    AppLogger.logger.debug("====> Remove directories")

    root_dir = Root.find_root_of_project(__file__)
    AppLogger.logger.debug(f"====> Root dir: {root_dir}")

    AppLogger.logger.debug("======> Remove directory dist")
    if os.path.exists(os.path.join(root_dir, 'dist')):
        rmtree(os.path.join(root_dir, 'dist'))

    AppLogger.logger.debug("======> Remove directory build")
    if os.path.exists(os.path.join(root_dir, 'build')):
        rmtree(os.path.join(root_dir, 'build'))


def build_windows_service():
    AppLogger.logger.debug("====> Build the windows service")
    root_dir = Root.find_root_of_project(__file__)
    command = ['pyinstaller', '-F', '--hidden-import=win32timezone',
               os.path.join(root_dir, 'windows_service.py')]
    AppLogger.logger.debug(f"Run: {' '.join(command)}")
    p = Popen(command, stdout=PIPE)
    p.communicate()


def main(args):
    AppLogger.logger.debug("==> ***** DEPLOY WINDOWS SERVICE - STARTED ***** <==")

    create_config_file()
    create_bat_file()

    remove_previous_deploy_directories()

    build_windows_service()

    AppLogger.logger.debug("==> ***** DEPLOY WINDOWS SERVICE - COMPLETED ***** <==")


if __name__ == '__main__':
    AppLogger.configure_and_get_logger('deploy')
    AppLogger.set_debug_level()
    main(sys.argv)
