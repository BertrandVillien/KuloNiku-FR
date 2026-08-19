@echo off
setlocal
set "BASE=%~dp0"
set /p "GAME=Chemin du dossier KuloNiku : "

"%BASE%KuloNiku-FR.exe" install "%GAME%" --translations "%BASE%translations\fr.csv"
echo.
set /p "ANSWER=Installer apres cette simulation ? Tapez O pour confirmer : "
if /I "%ANSWER%"=="O" (
  "%BASE%KuloNiku-FR.exe" install "%GAME%" --translations "%BASE%translations\fr.csv" --apply
) else (
  echo Aucune modification effectuee.
)
pause
