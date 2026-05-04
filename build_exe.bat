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
REM Build from EML-Math-App.spec — the spec uses Kivy's official PyInstaller
REM hooks (kivy_deps + kivy.tools.packaging.pyinstaller_hooks). Do NOT replace
REM with --collect-all kivy: that crashes on Kivy 2.3 / Python 3.13 because
REM kivy.garden is a legacy namespace package with a non-list __path__.
%PY% -m PyInstaller --noconfirm EML-Math-App.spec

echo.
if exist dist\EML-Math-App.exe (
    echo BUILD OK  --  dist\EML-Math-App.exe
) else (
    echo BUILD FAILED.
    exit /b 1
)
endlocal
