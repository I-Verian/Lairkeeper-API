@echo off
setlocal

echo ============================================
echo   Lairkeeper - Build EXE
echo ============================================
echo.

cd /d "%~dp0"

where py >nul 2>nul
if %errorlevel%==0 (
    set PYCMD=py
) else (
    where python >nul 2>nul
    if %errorlevel%==0 (
        set PYCMD=python
    ) else (
        echo ERROR: Python was not found on this machine.
        echo Install Python from https://www.python.org/downloads/ and try again.
        pause
        exit /b 1
    )
)

set MISSING=0
for %%F in (code.py wiki_data.py wiki_icons.py make_icon.py) do (
    if not exist "%%F" (
        echo ERROR: %%F not found in this folder.
        set MISSING=1
    )
)
if %MISSING%==1 (
    echo.
    echo All five files need to be in the same folder together:
    echo   build_exe.bat, code.py, wiki_data.py, wiki_icons.py, make_icon.py
    pause
    exit /b 1
)

echo Using: %PYCMD%
echo.

echo Closing any running copy of Lairkeeper.exe (if open)...
taskkill /IM Lairkeeper.exe /F >nul 2>nul
timeout /t 1 /nobreak >nul
if exist "dist\Lairkeeper.exe" (
    del /F /Q "dist\Lairkeeper.exe" >nul 2>nul
    if exist "dist\Lairkeeper.exe" (
        echo.
        echo ERROR: dist\Lairkeeper.exe is still locked by something ^(antivirus,
        echo an open Explorer window, etc^) and could not be deleted.
        echo Close whatever has it open, then run this script again.
        pause
        exit /b 1
    )
)
echo.

echo [1/4] Installing/updating required packages...
%PYCMD% -m pip install --upgrade pyinstaller requests beautifulsoup4 certifi pillow -q
if errorlevel 1 (
    echo ERROR: Failed to install required packages. Check your internet connection.
    pause
    exit /b 1
)
echo Done.
echo.

echo [2/4] Preparing the app icon...
%PYCMD% make_icon.py
if errorlevel 1 (
    echo WARNING: Could not prepare a custom icon ^(likely no internet right
    echo now^). Continuing without one - the exe will use PyInstaller's
    echo default icon instead. You can re-run this script later to add it.
    set ICON_FLAG=
) else (
    set ICON_FLAG=--icon=dragonhead.ico
)
echo.

echo [3/4] Building Lairkeeper.exe (this can take a minute or two)...
%PYCMD% -m PyInstaller --onefile --windowed --name "Lairkeeper" --collect-data certifi %ICON_FLAG% code.py
if errorlevel 1 (
    echo.
    echo ERROR: The build failed. Scroll up to see what went wrong.
    pause
    exit /b 1
)
echo.

echo [4/4] Done!
echo.
echo Your exe is here:
echo   %cd%\dist\Lairkeeper.exe
echo.
echo You can copy that file anywhere you like ^(e.g. your Desktop^) and run
echo it directly. It will create its own "assets" and "data" folders next
echo to itself the first time it runs.
echo.
pause
