@echo off
rem Poster Basim - Windows baslaticisi. Cift tiklayin.
rem Eksik bilesenleri program kendisi kurar; burada sadece uygun Python bulunur.
setlocal
cd /d "%~dp0"

rem Kendi ortami hazirsa dogrudan onu kullan (en hizli yol).
if exist ".venv\Scripts\pythonw.exe" (
    start "" ".venv\Scripts\pythonw.exe" "poster_bolme.py" %*
    exit /b 0
)

rem py baslaticisi Windows'ta Python kurulumlarini bulan en guvenilir yoldur.
where py >nul 2>&1
if %errorlevel%==0 (
    start "" py -3 "poster_bolme.py" %*
    exit /b 0
)

where pythonw >nul 2>&1
if %errorlevel%==0 (
    start "" pythonw "poster_bolme.py" %*
    exit /b 0
)

where python >nul 2>&1
if %errorlevel%==0 (
    start "" python "poster_bolme.py" %*
    exit /b 0
)

echo.
echo Python bulunamadi.
echo python.org adresinden Python 3 kurun; kurulum sirasinda
echo "Add python.exe to PATH" ve "tcl/tk and IDLE" secenekleri isaretli kalsin.
echo.
pause
exit /b 1

rem powered by Omer OZTURK
