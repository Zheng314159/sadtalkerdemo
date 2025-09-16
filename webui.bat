@echo off

IF NOT EXIST .sadenv (
    python -m venv .sadenv
) ELSE (
    echo .sadenv folder already exists, skipping creation...
)

call .\.sadenv\Scripts\activate.bat

set PYTHON=".sadenv\Scripts\Python.exe"
echo venv %PYTHON%

%PYTHON% Launcher.py

echo.
echo Launch unsuccessful. Exiting.
pause
