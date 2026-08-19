@echo off
setlocal
set "BASE=%~dp0"
set /p "GAME=Chemin du dossier KuloNiku : "

"%BASE%KuloNiku-FR.exe" restore "%GAME%"
echo.
set /p "ANSWER=Restaurer la sauvegarde ? Tapez O pour confirmer : "
if /I "%ANSWER%"=="O" (
  "%BASE%KuloNiku-FR.exe" restore "%GAME%" --apply
) else (
  echo Aucune modification effectuee.
)
pause
