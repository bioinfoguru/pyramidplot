@echo off
echo Initializing Git repository...
git init

echo Adding files...
git add .

echo Committing changes...
git commit -m "Update pyramidplot"

echo Renaming branch to main...
git branch -M main

echo Adding remote origin...
:: git remote add origin git@github.com:bioinfoguru/pyramidplot.git
:: If remote already exists, set url instead
git remote set-url origin git@github.com:bioinfoguru/pyramidplot.git

echo Pushing to GitHub...
git push -u origin main

echo Done.
pause
