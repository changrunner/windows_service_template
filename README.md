# simple_windows_service
## Purpose
Simple windows service with a virtual environment and AWS Cloud Logging.
This is the third configuration and final production to figure the steps that are needed
for a completely working windows service.

## Steps to working code
Note: make sure you are in the step3 directory

$ python -V
```
Python 3.8.5
```
$ pip install pipenv

$ pip freeze
```
appdirs==1.4.4
certifi==2020.12.5
distlib==0.3.1
filelock==3.0.12
pipenv==2020.11.15
six==1.15.0
virtualenv==20.4.2
virtualenv-clone==0.5.4
```

$ pipenv install

$ notepad Change_me.py

Change the service_name, service_display_name, and service_debug_mode (True or False)
Then safe the changes.

$ pipenv shell

(step2-xyz)$ python deploy.py

This will create:
- dist/windows_service.exe
- c:\users\{current user}\.config\config_{service_name}.json
- c:\windows\system32\{service_name}_app_start_me.bat

NOTE:

The config_{service_name}.json has the values from the "chang_me.py" file

The {service_name}_app_start_me.bat file has the script to start the application you want the windows service
to start. This file will be created once and points to {root_dir of project}\app\run_server.py"
Feel free to change this in the bat file. Upon next deployments this will not be overwritten.

(step2-xyz)$ dist\windows_service.exe install

```
Installing service simple_windows_service
Service installed
```

Configure security on the service.
```Goto "Windows Start",
Type "service"
Click the "windows service"
In the windows service window find the new service by "service_display_name" from "change_me.py"
Right click,
Click "Properties"
Select the "Logon" tab
Click "This Account"
Click "Browse"
Enter the name of the account you want this service to run under. 
====> This is the same user as in the above c:\users\{current user}
Click check names
Click OK
Enter Password and confirm password
Click OK 
```

--
If you running under local host. The service will throw an error that it times out.

```
Error 1053: The service did not respond ....
```
--

create a .aws directory under the "c:\users\{service user}\.aws"

Follow the instructions from the internet to install AWS CLI 2 for windows or copy your previous .aws directory.

(step2-xyz)$ dist\simple_windows_service.exe start
```
Starting service simple_windows_service
```

(step2-xyz)$ dist\simple_windows_service.exe stop
```
Stopping service simple_windows_service
```

(step2-xyz)$ dist\simple_windows_service.exe remove
```
Removing service simple_windows_service
Service removed
```

(step2-xyz)$ exit

To exit the pipenv shell. You want see the (step2-xyz) anymore.


## Common Issues
### 1) Error Message when running "dist\simple_windows_service.exe install"
```buildoutcfg
Traceback (most recent call last):
  File "simple_windows_service.py", line 1, in <module>
    import servicemanager
ModuleNotFoundError: No module named 'servicemanager'
[6692] Failed to execute script simple_windows_service
```

Resolution: 
```
pipenv shell
pip install pywin32
pyinstaller -F --hidden-import=win32timezone simple_windows_service.py
dist\simple_windows_service.exe install
```

### 2) Windows service deleting issue
Resolution:
```
sc delete zzz_simple_windows_service
```

### 3) Getting windows service start up timeout
This is caused by an error on startup in the application.
More than likely by the AWS Cloudwatch logging.

Resolution:
- So make sure the pypi packages are there
- Make sure you are running your service under a user account and not local system
- Make sure the .aws configuration is present.

NOTE: A 'C:\log\windows_service.log' file might be present with more details. 

### 4) Application did not start

If the appliation you want the windows service to start did not start do the following:

Resolution:
- When running in debug_mode=True, you can check 'c:\log\{application_name}_log.txt' file 
  with more details if the application did not start.
- Check the aws cloud watch logs.

### 5) Can find the logs in AWS Cloudwatch.

Resolution:
- Goto AWS Cloudwatch
- Select the region specified in the C:\users\{current_user}\.aws\config
```
[default]
region = us-east-2
output = json
```
- Select the log_group "windows_service"
- Select the stream with the "windows_service" name as specified in the change_me.py

### 6) Application is running but the windows running=False in AWS Logs

This is caused by the pid file the windows server looks for is not matched up with what the app created.
Look in the c:\users\{current_user}\.pid directory. There should be a file with the pattern
{service_name}_app.pid where the service_name comes from the change_me.py.

Resolution:
When using the run_server.py and run_app_base.py pattern from the app directory, 
make sure the application name "APPLICATION_NAME" is set to {service_name}_app
where the service_name comes from the change_me.py.

Impact of the issue:
- If this issue occures the windows service does not know how to shutdown the app when the service is stopped.