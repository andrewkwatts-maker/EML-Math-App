@echo off
REM ============================================================================
REM build_exe.bat — Windows executable for EML-Math-App via PyInstaller
REM
REM Output: dist\EML-Math-App.exe
REM
REM Prerequisites: a Python 3.11+ with the project's [dev] extras installed.
REM The first run takes ~3 minutes; subsequent ones are faster.
REM ============================================================================
setlocal

set "PY=%PY%"
if "%PY%"=="" set "PY=python"

echo Installing build dependencies and project ...
%PY% -m pip install --upgrade pip pyinstaller
%PY% -m pip install -e .

echo.
echo Running PyInstaller ...
%PY% -m PyInstaller ^
    --noconfirm ^
    --name "EML-Math-App" ^
    --windowed ^
    --onefile ^
    --add-data "src\eml_math_app\kv;eml_math_app\kv" ^
    --add-data "src\eml_math_app\assets;eml_math_app\assets" ^
    --collect-all kivymd ^
    --collect-all kivy ^
    --collect-all eml_math ^
    src\eml_math_app\__main__.py

echo.
if exist dist\EML-Math-App.exe (
    echo BUILD OK  ->  dist\EML-Math-App.exe
) else (
    echo BUILD FAILED.
    exit /b 1
)
endlocal
