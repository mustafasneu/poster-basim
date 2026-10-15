@echo off
rem Masaustune "Poster Basim" kisayolu koyar. Cift tiklayin, bir kez calistirmak yeter.
setlocal
cd /d "%~dp0"

where py >nul 2>&1
if %errorlevel%==0 (
    py -3 "kurulum.py"
    goto bitti
)

where python >nul 2>&1
if %errorlevel%==0 (
    python "kurulum.py"
    goto bitti
)

echo.
echo Python bulunamadi.
echo python.org adresinden Python 3 kurun; kurulum sirasinda
echo "Add python.exe to PATH" ve "tcl/tk and IDLE" secenekleri isaretli kalsin.
echo Sonra bu dosyaya tekrar cift tiklayin.

:bitti
echo.
pause

rem powered by Ömer ÖZTÜRK & Mustafa ŞEKER
