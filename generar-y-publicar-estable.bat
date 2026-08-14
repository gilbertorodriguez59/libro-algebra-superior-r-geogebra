@echo off
setlocal EnableExtensions
chcp 65001 >nul
title Algebra Superior con R y GeoGebra - estable
pushd "%~dp0" >nul 2>&1
if errorlevel 1 goto :error

if not exist "_quarto.yml" (
  echo ERROR: Este BAT debe estar junto a _quarto.yml.
  goto :error_carpeta
)
where quarto >nul 2>&1 || (
  echo ERROR: Windows no encuentra Quarto.
  goto :error_carpeta
)

set "PDF_NOMBRE=Algebra-Superior-R-GeoGebra-Capitulos-1-5.pdf"
set "PDF_TEMP=%TEMP%\%PDF_NOMBRE%"

echo Generando el PDF...
quarto render --to pdf
if errorlevel 1 goto :error_render
if not exist "docs\%PDF_NOMBRE%" (
  echo ERROR: No se genero docs\%PDF_NOMBRE%.
  goto :error_carpeta
)
copy /Y "docs\%PDF_NOMBRE%" "%PDF_TEMP%" >nul
if errorlevel 1 goto :error_render

echo Generando la web multipagina con menus laterales...
quarto render --to html
if errorlevel 1 goto :error_render
copy /Y "%PDF_TEMP%" "docs\%PDF_NOMBRE%" >nul
if errorlevel 1 goto :error_render
if exist "%PDF_TEMP%" del /Q "%PDF_TEMP%" >nul 2>&1
if not exist "docs\.nojekyll" type nul > "docs\.nojekyll"
if not exist "docs\index.html" (
  echo ERROR: No se genero docs\index.html.
  goto :error_carpeta
)
if not exist "docs\01-logica-conjuntos.html" (
  echo ERROR: No se genero la pagina del capitulo 1.
  goto :error_carpeta
)
if not exist "docs\02-enteros-reales.html" (
  echo ERROR: No se genero la pagina del capitulo 2.
  goto :error_carpeta
)
if not exist "docs\03-numeros-complejos.html" (
  echo ERROR: No se genero la pagina del capitulo 3.
  goto :error_carpeta
)
if not exist "docs\04-polinomios.html" (
  echo ERROR: No se genero la pagina del capitulo 4.
  goto :error_carpeta
)
if not exist "docs\05-metodos-raices.html" (
  echo ERROR: No se genero la pagina del capitulo 5.
  goto :error_carpeta
)
if not exist "docs\notebooks\capitulo-05-metodos-raices-R.ipynb" (
  echo ERROR: No se copio el cuaderno del capitulo 5.
  goto :error_carpeta
)
if not exist "docs\interactivos\geogebra-secante-newton.html" (
  echo ERROR: No se copiaron las construcciones GeoGebra del capitulo 5.
  goto :error_carpeta
)
if not exist "docs\notebooks\capitulo-04-polinomios-R.ipynb" (
  echo ERROR: No se copio el cuaderno del capitulo 4.
  goto :error_carpeta
)
if not exist "docs\interactivos\geogebra\funciones-racionales.ggb" (
  echo ERROR: No se copiaron las construcciones GeoGebra del capitulo 4.
  goto :error_carpeta
)
if not exist "docs\%PDF_NOMBRE%" (
  echo ERROR: El PDF no quedo disponible para descarga.
  goto :error_carpeta
)

echo.
echo Libro generado correctamente.
start "" "docs\index.html"
echo.
choice /C SN /N /M "Deseas subir esta version al repositorio estable? [S/N]: "
if errorlevel 2 goto :fin

where git >nul 2>&1 || (
  echo ERROR: Windows no encuentra Git.
  goto :error_carpeta
)
git rev-parse --is-inside-work-tree >nul 2>&1 || (
  echo ERROR: Esta carpeta no es un repositorio Git clonado.
  goto :error_carpeta
)
git remote get-url origin | findstr /I /C:"libro-algebra-superior-r-geogebra" >nul || (
  echo ERROR: El remoto origin no corresponde al repositorio estable esperado.
  git remote -v
  goto :error_carpeta
)

git add .
git diff --cached --quiet
if not errorlevel 1 (
  echo No hay cambios nuevos para subir.
  goto :fin
)
git commit -m "Agrega capitulo 5 y construcciones GeoGebra"
if errorlevel 1 goto :error_git
git push origin main
if errorlevel 1 goto :error_git
echo.
echo Publicacion terminada correctamente.
goto :fin

:error_render
echo ERROR: Quarto detuvo la generacion. Revisa las lineas anteriores.
goto :error_carpeta
:error_git
echo ERROR: Git no pudo completar la publicacion. No se borraron archivos.
:error_carpeta
popd >nul 2>&1
:error
pause
exit /b 1
:fin
popd >nul 2>&1
pause
exit /b 0
