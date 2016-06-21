# Set these variables to suit your needs

CUR_PATH=$(cd `dirname $0`; pwd)

NDK_PATH=${NDK_ROOT}
BUILD_PLATFORM="windows"
TOOLCHAIN_VERSION="4.9"
ANDROID_VERSION=15

source_directory=${CUR_PATH}/../src
build_directory=${CUR_PATH}/android
install_root=${CUR_PATH}/../install/android

if [ ! -d ${CUR_PATH}/../install ]; then
  mkdir ${CUR_PATH}/../install
fi

if [ ! -d ${install_root} ]; then
  mkdir ${install_root}
fi

if [ ! -d ${build_directory} ]; then
  mkdir ${build_directory}
fi

# 32-bit ARMv7 build
HOST=arm-linux-androideabi
PREFIX=arm-linux-androideabi
SYSROOT=${NDK_PATH}/platforms/android-${ANDROID_VERSION}/arch-arm
ANDROID_CFLAGS="-march=armv7-a -mfloat-abi=softfp -fprefetch-loop-arrays --sysroot=${SYSROOT}"
install_directory=${install_root}/armv7

if [ ! -d ${install_directory} ]; then
  mkdir ${install_directory}
fi


TOOLCHAIN=${NDK_PATH}/toolchains/${HOST}-${TOOLCHAIN_VERSION}/prebuilt/${BUILD_PLATFORM}
ANDROID_INCLUDES="-I${SYSROOT}/usr/include -I${TOOLCHAIN}/include"
export CPP=${TOOLCHAIN}/bin/${PREFIX}-cpp
export AR=${TOOLCHAIN}/bin/${PREFIX}-ar
export AS=${TOOLCHAIN}/bin/${PREFIX}-as
export NM=${TOOLCHAIN}/bin/${PREFIX}-nm
export CC=${TOOLCHAIN}/bin/${PREFIX}-gcc
export LD=${TOOLCHAIN}/bin/${PREFIX}-ld
export RANLIB=${TOOLCHAIN}/bin/${PREFIX}-ranlib
export OBJDUMP=${TOOLCHAIN}/bin/${PREFIX}-objdump
export STRIP=${TOOLCHAIN}/bin/${PREFIX}-strip

echo "HOST=${HOST}" 
echo "SYSROOT=${SYSROOT}" 
echo "ANDROID_CFLAGS=${ANDROID_CFLAGS}" 
echo "install_directory=${install_directory}" 
echo "CPP=${CPP}" 
echo "AR=${AR}" 
echo "AS=${AS}" 
echo "NM=${NM}" 
echo "CC=${CC}" 
echo "LD=${LD}" 
echo "RANLIB=${RANLIB}" 
echo "OBJDUMP=${OBJDUMP}" 
echo "STRIP=${STRIP}" 

cd ${source_directory}
sh autoreconf-2.68 -fiv

cd ${build_directory}

sh ${source_directory}/configure --host=${HOST} \
  CFLAGS="${ANDROID_INCLUDES} ${ANDROID_CFLAGS} -O3" \
  CPPFLAGS="${ANDROID_INCLUDES} ${ANDROID_CFLAGS}" \
  LDFLAGS="${ANDROID_CFLAGS}" --with-simd ${1+"$@"} \
  --with-jpeg8 --without-java \
  --prefix=${install_directory} \
  --mandir=${install_directory}/man \
  --docdir=${install_directory}/doc
make
make clean
make install

pause

exit

# 32-bit x86 build
HOST=x86
PREFIX=i686-linux-android
SYSROOT=${NDK_PATH}/platforms/android-${ANDROID_VERSION}/arch-x86
ANDROID_CFLAGS="--sysroot=${SYSROOT}"
install_directory=${install_root}/x86

if [ ! -d ${install_directory} ]; then
  mkdir ${install_directory}
fi


TOOLCHAIN=${NDK_PATH}/toolchains/${HOST}-${TOOLCHAIN_VERSION}/prebuilt/${BUILD_PLATFORM}
ANDROID_INCLUDES="-I${SYSROOT}/usr/include -I${TOOLCHAIN}/include"
export CPP=${TOOLCHAIN}/bin/${PREFIX}-cpp
export AR=${TOOLCHAIN}/bin/${PREFIX}-ar
export AS=${TOOLCHAIN}/bin/${PREFIX}-as
export NM=${TOOLCHAIN}/bin/${PREFIX}-nm
export CC=${TOOLCHAIN}/bin/${PREFIX}-gcc
export LD=${TOOLCHAIN}/bin/${PREFIX}-ld
export RANLIB=${TOOLCHAIN}/bin/${PREFIX}-ranlib
export OBJDUMP=${TOOLCHAIN}/bin/${PREFIX}-objdump
export STRIP=${TOOLCHAIN}/bin/${PREFIX}-strip

echo "HOST=${HOST}" 
echo "SYSROOT=${SYSROOT}" 
echo "ANDROID_CFLAGS=${ANDROID_CFLAGS}" 
echo "install_directory=${install_directory}" 
echo "CPP=${CPP}" 
echo "AR=${AR}" 
echo "AS=${AS}" 
echo "NM=${NM}" 
echo "CC=${CC}" 
echo "LD=${LD}" 
echo "RANLIB=${RANLIB}" 
echo "OBJDUMP=${OBJDUMP}" 
echo "STRIP=${STRIP}" 

cd ${source_directory}
autoreconf -fiv

cd ${build_directory}

sh ${source_directory}/configure --host=${HOST} \
  CFLAGS="${ANDROID_INCLUDES} ${ANDROID_CFLAGS} -O3" \
  CPPFLAGS="${ANDROID_INCLUDES} ${ANDROID_CFLAGS}" \
  LDFLAGS="${ANDROID_CFLAGS}" --with-simd ${1+"$@"} \
  --with-jpeg8 --without-java \
  --prefix=${install_directory} \
  --mandir=${install_directory}/man \
  --docdir=${install_directory}/doc
make
make clean
make install