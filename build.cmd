@echo off

SET MAGICK_HOME=%~dp0ImageMagicWin
SET PATH=%PATH%;%MAGICK_HOME%
SET MAGICK_CODER_MODULE_PATH=%MAGICK_HOME%\modules\coders
SET MAGICK_CODER_FILTER_PATH=%MAGICK_HOME%\modules\filters
SET MAGICK_CONFIGURE_PATH=%MAGICK_HOME%

IF NOT EXIST %~dp0\.venv (
	python -m virtualenv %~dp0\.venv
	%~dp0\.venv\Scripts\pip install -r %~dp0\requirements.txt
)

%~dp0\.venv\Scripts\python %~dp0\build.py %*
