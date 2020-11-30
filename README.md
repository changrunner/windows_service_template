# windows_service_template
Template for a windows service

## requirements
-- AWS Cli with configuration for cloud watch

## Changes to be made.
### Guided setup through testing
- In the tests\config_values set the appropriate values for each
 ```
service_name = "zzz_windows_service_template"
service_display_name = "zzz Windows Service Template"
application_name = "windows_service_template"
app_to_start_cmd = "windows_service_template_start_me.bat"
  ``` 
Doing this and then running the test will guide you through setting up the project correctly.

At the command prompt
```
pipenv install
pipenv install --dev
pipenv shell
pytest tests\test_config_setup.py
``` 
If the result is "tests\test_config_setup.py . [100%]",
then the test passed and everything is correct.

## build windows service
pipenv run python deploy.py

## install windows service
This installs and updates the service code
```
dist\windows_service.exe install
```

## run windows service
- Start menu - service - [enter]
- Run windows service as service account

## uninstall windows service
dist\windows_service.exe remove



