
echo off

set NMAKE_PATH=%VS140COMNTOOLS%..\..\VC\bin\nmake.exe
set BUILD_PATH=%CD%\..\build\win32\
set INSTALL_PATH=%CD%\..\install\win32\
set SOURCE_PATH=%CD%\..\src\
set BASH=%VS140COMNTOOLS%..\..\VC\vcvarsall.bat

echo NMAKE_PATH = %NMAKE_PATH%
echo BUILD_PATH = %BUILD_PATH%
echo INSTALL_PATH = %INSTALL_PATH%
echo SOURCE_PATH = %SOURCE_PATH%

call "%BASH%" x86

if exist %BUILD_PATH% (
	rm -rf %BUILD_PATH%
)

mkdir %BUILD_PATH%

pushd %BUILD_PATH%
	rem NMake Makefiles
	rem Visual Studio 14 2015
	cmake -G "NMake Makefiles" -DCMAKE_BUILD_TYPE=Release -DWITH_JPEG8=1 -DWITH_JAVA=0 -DCMAKE_INSTALL_PREFIX=%INSTALL_PATH% %SOURCE_PATH%
	%NMAKE_PATH%
	%NMAKE_PATH% install
popd

rem remove build dir
if exist %BUILD_PATH% (
	rm -rf %BUILD_PATH%
)

pause