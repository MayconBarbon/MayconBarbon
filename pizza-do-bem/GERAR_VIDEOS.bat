@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"
echo ============================================================
echo   Pizza do Bem 2018-2025 - geracao dos videos
echo ============================================================
echo.
where python >nul 2>nul || (echo [ERRO] Python nao encontrado. Instale pelo python.org marcando "Add python.exe to PATH". & pause & exit /b 1)
where ffmpeg >nul 2>nul || (echo [ERRO] ffmpeg nao encontrado. Instale com:  winget install Gyan.FFmpeg  e abra este arquivo de novo. & pause & exit /b 1)

set "FOTOS=%~1"
if "%FOTOS%"=="" set /p "FOTOS=Arraste aqui a pasta das fotos (ou cole o caminho) e tecle Enter: "
set "FOTOS=%FOTOS:"=%"
if not exist "%FOTOS%\" (echo [ERRO] Pasta nao encontrada: %FOTOS% & pause & exit /b 1)

set "SAIDA=%~dp0SAIDA"
if not exist "%SAIDA%" mkdir "%SAIDA%"

echo.
echo [1/4] Instalando bibliotecas (so na primeira vez)...
python -m pip install --quiet --disable-pip-version-check pillow numpy opencv-python-headless || (echo [ERRO] Falha ao instalar bibliotecas. & pause & exit /b 1)

echo [2/4] Classificando e tratando as fotos...
python prep.py "%FOTOS%" "%SAIDA%\trabalho" || (echo [ERRO] Falha no tratamento das fotos. & pause & exit /b 1)

echo.
echo [3/4] Renderizando o video PRINCIPAL (pode levar 20-60 min)...
python render.py "%SAIDA%\trabalho" principal "%SAIDA%\PizzaDoBem_Retrospectiva_2018-2025.mp4" || (echo [ERRO] Falha na renderizacao. & pause & exit /b 1)

echo [4/4] Renderizando a versao LOOP (pode levar 20-60 min)...
python render.py "%SAIDA%\trabalho" loop "%SAIDA%\PizzaDoBem_Retrospectiva_2018-2025_LOOP.mp4" || (echo [ERRO] Falha na renderizacao. & pause & exit /b 1)

rmdir /s /q "%SAIDA%\PizzaDoBem_Retrospectiva_2018-2025.mp4.parts" 2>nul
rmdir /s /q "%SAIDA%\PizzaDoBem_Retrospectiva_2018-2025_LOOP.mp4.parts" 2>nul
echo.
echo Pronto! Os videos estao em: %SAIDA%
explorer "%SAIDA%"
pause
