@echo off

SET MAGICK_HOME=%~dp0ImageMagicWin
SET PATH=%PATH%;%MAGICK_HOME%
SET MAGICK_CODER_MODULE_PATH=%MAGICK_HOME%\modules\coders
SET MAGICK_CODER_FILTER_PATH=%MAGICK_HOME%\modules\filters
SET MAGICK_CONFIGURE_PATH=%MAGICK_HOME%

IF NOT EXIST .venv (
	python -m virtualenv .venv
	.venv\Scripts\pip install -r requirements.txt
)

.venv\Scripts\python build.py %*
