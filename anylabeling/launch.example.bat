@echo off
setlocal

rem Set ANYLABELING_EXE if AnyLabeling is not already on PATH.
if not defined ANYLABELING_EXE set "ANYLABELING_EXE=anylabeling"

set "PROJECT_ROOT=%~dp0.."
set "IMAGE_DIR=%~1"
if "%IMAGE_DIR%"=="" set "IMAGE_DIR=%PROJECT_ROOT%\data\images"

if not exist "%PROJECT_ROOT%\outputs\annotations" (
  mkdir "%PROJECT_ROOT%\outputs\annotations"
)

"%ANYLABELING_EXE%" ^
  --config "%PROJECT_ROOT%\anylabeling\anylabeling_config.example.yaml" ^
  --output "%PROJECT_ROOT%\outputs\annotations" ^
  --autosave ^
  --nodata ^
  "%IMAGE_DIR%"

endlocal

