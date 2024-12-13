@echo off
setlocal

:: Check for python3
where python3 >nul 2>&1
if %errorlevel%==0 (
    set PYTHON_CMD=python3
) else (
    :: Fallback to python
    where python >nul 2>&1
    if %errorlevel%==0 (
        set PYTHON_CMD=python
    ) else (
        echo Python is not installed or not added to PATH.
        exit /b 1
    )
)

:: Run the Python script
set DIR=%~dp0
%PYTHON_CMD% "%DIR%avs" %*
