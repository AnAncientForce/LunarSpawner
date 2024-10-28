@echo off

set VENV=.venv

if not exist %VENV%\Scripts\activate (
    python -m venv %VENV%
)

call %VENV%\Scripts\activate

pip install -r requirements.txt

echo Dependencies installed successfully.
