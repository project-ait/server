@echo off
:: Check for admin rights
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
:: If error flag set, we do not have admin.
if '%errorlevel%' NEQ '0' (
    echo Requesting admin rights...
    goto UACPrompt
) else ( goto gotAdmin )

:UACPrompt
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"
    "%temp%\getadmin.vbs"
    exit /B

:gotAdmin
    if exist "%temp%\getadmin.vbs" ( del "%temp%\getadmin.vbs" )

setlocal enabledelayedexpansion

set /p user=AIT_DB_USER: 
set /p pw=AIT_DB_PW: 
set /p db=AIT_DB_NAME: 

echo setting environments...
:: ���� ���� ���� �����Ѵٸ� ����
:: set "AIT_DB_USER="
:: ����� �Է��� ȯ�� ������ ����
setx AIT_DB_USER %user%
setx AIT_DB_PW %pw%
setx AIT_DB_NAME %db%
echo setup complete
pause