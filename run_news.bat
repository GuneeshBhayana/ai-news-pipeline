@REM @echo off
@REM cd /d C:\Users\GUNEESH BHAYANA\Documents\PROJECTS\ai_news_pipeline
@REM call .venv\Scripts\activate
@REM python generator.py

@echo off
cd /d C:\Users\GUNEESH BHAYANA\Documents\PROJECTS\ai_news_pipeline
call .venv\Scripts\activate
echo Pipeline started >> log.txt
python generator.py >> log.txt 2>&1
echo Pipeline finished >> log.txt