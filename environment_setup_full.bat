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

echo "모든 변수를 설정하는 프로그램 입니다"
echo "관리자만 수행하면 되는 작업입니다"
set /p user=AIT_DB_USER: 
set /p pw=AIT_DB_PW: 
set /p db=AIT_DB_NAME: 
set /p salt=AIT_PW_SALT:
set /p pepper=AIT_PW_PEPPER:
set /p deepl_key=DEEPL_API_KEY:

echo setting environments...
:: 사용자 입력을 환경 변수에 저장
setx AIT_DB_USER %user%
setx AIT_DB_PW %pw%
setx AIT_DB_NAME %db%
setx AIT_PW_SALT %salt%
setx AIT_PW_PEPPER %pepper%
setx DEEPL_API_KEY %deepl_key%
echo setup complete
pause