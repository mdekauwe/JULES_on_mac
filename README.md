# JULES_on_mac

## To compile

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
These are set in the files, so you don't need to do anything below except add "$JULES_NETCDF{?} = netcdf" and "$JULES_NETCDF_PATH{?} = /opt/local". This is just for my notes

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

You don't need the below, but alternatively you can set these on the cmd line and skip setting things in files

export JULES_NETCDF=netcdf
export JULES_NETCDF_PATH=/opt/local
export JULES_BUILD=normal
export JULES_REMOTE=local
export JULES_OMP=noomp
export JULES_COMPILER=gfortran
export JULES_MPI=nompi
export JULES_PLATFORM=custom


## To Build...

```
$ fcm make -f etc/fcm-make/make.cfg
```

## To extract the namelists from a suite

I made a directory called "namelists"

Then ran

```
$ rose app-run -i -C path_to_suite_to_extract_namelists_from../test/app/jules
```

e.g.

```
$ rose app-run -i -C ../test/app/jules
```

## To run JULES

Change into that namelist directory

```
$ ~/research/JULES/src/jules-vn7.0/build/bin/jules.exe
```
