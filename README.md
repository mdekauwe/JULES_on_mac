# JULES_on_mac

At the end of file: "etc/fcm-make/compiler/gfortran.cfg"

Add:

```
build.prop{fc.flags}[jules/src/io/dump/read_dump_mod.F90] = $fflags_common -fallow-argument-mismatch
```

In file: jules-vn7.0/etc/fcm-make/ncdf/netcdf.cfg

Change:

```
$ncdf_ldflags_dynamic{?} = -Wl,--rpath=${JULES_NETCDF_LIB_PATH}
```

to (i.e. --rpath to -rpath):

```
$ncdf_ldflags_dynamic{?} = -Wl,-rpath ${JULES_NETCDF_LIB_PATH}
```

Change args in "etc/fcm-make/platform/envars.cfg"

```
# Default values.
# These will be used if not already set by the user or overrriden later
# in a platform specific configuration file.
$JULES_REMOTE{?}          = local
$JULES_REMOTE_HOST{?}     =
$JULES_REMOTE_PATH{?}     =
$JULES_COMPILER{?}        = gfortran
$JULES_BUILD{?}           = normal
$JULES_OMP{?}             = noomp
$JULES_MPI{?}             = nompi
$JULES_NETCDF{?}          = netcdf
$JULES_NETCDF_PATH{?}     = /opt/local
$JULES_NETCDF_INC_PATH{?} = $JULES_NETCDF_PATH/include
$JULES_NETCDF_LIB_PATH{?} = $JULES_NETCDF_PATH/lib
$JULES_FFLAGS_EXTRA{?}    =
$JULES_LDFLAGS_EXTRA{?}   =
```

Then to build:

```
$ fcm make -f etc/fcm-make/make.cfg
```

# Don't need the below, but alternatively you can set these

export JULES_NETCDF=netcdf
export JULES_NETCDF_PATH=/opt/local
export JULES_BUILD=normal
export JULES_REMOTE=local
export JULES_OMP=noomp
export JULES_COMPILER=gfortran
export JULES_MPI=nompi
export JULES_PLATFORM=custom
