 #! /bin/sh 
JEMALLOC_VERSION = "3.6.0" 
ARCHS = ("i386" "armv7" "armv7s" "arm64" "x86_64") 
SDK_VERSION = "9.1" 
ROOT_DIR = `pwd` 
BUILD_DIR = "build/jemalloc" 
LIPO_CMD = "lipo -create -output libjemalloc.a" 

if [-d "${BUILD_DIR}/download"]; then 
rm -rf "${BUILD_DIR}/download" 
fi 
if [-d "${BUILD_DIR}/source"]; then 
rm -rf "${BUILD_DIR}/source" 
fi 
mkdir -p "${BUILD_DIR}/download" 
mkdir -p "${BUILD_DIR}/source" 
echo "Downloading: jemalloc" 
curl -Lo "${BUILD_DIR}/download/jemalloc-${JEMALLOC_VERSION}.tar.bz2" "http://www.canonware.com/download/jemalloc/jemalloc-${JEMALLOC_VERSION}.tar.bz2" 1> &/dev/null 
if [$-eq 0?]; then 
echo "Downloaded: jemalloc" 
echo "Uncompressing: jemalloc" 
tar xjf "${BUILD_DIR}/download/jemalloc-${JEMALLOC_VERSION}.tar.bz2" -C ${BUILD_DIR}/source 
if [$-eq 0?]; then 
echo "Uncompressed: jemalloc" 
for ARCH in "${ARCHS[@]}"; do 
echo "" 
cd "${ROOT_DIR}" 
if [-d "${BUILD_DIR}/output/${ARCH}"]; then 
rm -rf "${BUILD_DIR}/output/${ARCH}" 
fi 
mkdir -p "${BUILD_DIR}/output/${ARCH}" 
cp -R "${BUILD_DIR}/source/jemalloc-${JEMALLOC_VERSION}/" "${BUILD_DIR}/output/${ARCH}" 
if [-d "${BUILD_DIR}/install/${ARCH}"]; then 
rm -rf "${BUILD_DIR}/install/${ARCH}" 
fi 
mkdir -p "${BUILD_DIR}/install/${ARCH}" 
if [$ARCH == "i386"] || [$ARCH == "x86_64"]; then 
PLATFORM = "iPhoneSimulator" 
else 
PLATFORM = "iPhoneOS" 
fi 
BUILD_SDKROOT = "/Applications/Xcode.app/Contents/Developer/Platforms/${PLATFORM}.platform/Developer/SDKs/${PLATFORM}${SDK_VERSION}.sdk" 
export LDFLAGS = "-arch ${ARCH} -pipe -isysroot ${BUILD_SDKROOT} -miphoneos-version-min = 6.0 -Os" 
export CFLAGS = "-arch ${ARCH} -pipe -isysroot ${BUILD_SDKROOT} -miphoneos-version-min = 6.0 -Os" 
export CPPFLAGS = "${CFLAGS}" 
export CXXFLAGS = "${CFLAGS}" 
export CC = clang 
export CCXX = clang ++ 
cd "${ROOT_DIR}/${BUILD_DIR}/output/${ARCH}" 
if [-d "${BUILD_DIR}/download"]; then 
rm -rf "${BUILD_DIR}/download" 
fi 
if [$ARCH == "arm64" ]; then 
HOST = "aarch64" 
else 
HOST = "${ARCH}" 
fi 
echo "Configuring: jemalloc ${ARCH}" 
./configure --host = "${HOST} -apple-darwin" \ 
--prefix = "${ROOT_DIR}/${BUILD_DIR}/install/${ARCH}" \ 
--disable-valgrind \ 
--disable-utrace \ 
--disable-debug 1> &/dev/null 
if [$-eq 0?]; then 
echo "Configured: jemalloc ${ARCH}" 
echo "Compiling: jemalloc ${ARCH}" 
make 1> &/dev/null 
if [$-eq 0?]; then 
echo "Compiled: jemalloc ${ARCH}" 
echo "Installing: jemalloc ${ARCH}" 
make install 1> &/dev/null 
if [$-eq 0?]; then 
echo "Installed: jemalloc ${ARCH }" 
LIPO_CMD = "${LIPO_CMD} ${ROOT_DIR}/${BUILD_DIR}/install/${ARCH}/lib/jemalloc.a" 
else 
echo "Error installation jemalloc ${ARCH}" 
fi 
else 
echo "Error compilation jemalloc ${ARCH}" 
fi 
else 
echo "Error configuration jemalloc ${ARCH}" 
fi 
done 
echo "" 
cd "${ROOT_DIR}/${BUILD_DIR}" 
if [-f "libjemalloc.a"]; then 
rm -f "libjemalloc.a" 
fi 
echo "Creating Flat Lib: libjemalloc" 
LIPO_CMD = "lipo -create" 
for ARCH in "${ARCHS[@]}"; do 
if [-f "${ROOT_DIR}/${BUILD_DIR}/install/${ARCH}/lib/libjemalloc.a"]; then 
LIPO_CMD = "$LIPO_CMD ${ROOT_DIR}/${BUILD_DIR}/install/${ARCH}/lib/libjemalloc.a" 
fi 
done 
LIPO_CMD = "$LIPO_CMD -output libjemalloc.a 1 > &/dev/null" 
eval $LIPO_CMD 
if [$-eq 0?]; then 
echo "Created Flat Lib: libjemalloc" 
else 
echo "Error creation flat libjemalloc" 
fi 
else 
echo "Error uncompress libjemalloc" 
fi 
else 
echo "Error download libjemalloc" 
fi 