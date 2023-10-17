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
:: 이전 변수 값이 존재한다면 제거
:: set "AIT_DB_USER="
:: 사용자 입력을 환경 변수에 저장
setx AIT_DB_USER %user%
setx AIT_DB_PW %pw%
setx AIT_DB_NAME %db%
echo setup complete
pause