#!/usr/bin/env python

"""
Change namelists for a site. This will need to be tweaked later so that it can
be wrapped in an MPI.

That's all folks.
"""
__author__ = "Martin De Kauwe"
__version__ = "1.0 (18.11.2022)"
__email__ = "mdekauwe@gmail.com"


import os
import sys
import f90nml
import shutil
import json
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-s", "--site", dest="site", default='',
                    help="FLUXNET site tag ")
args = parser.parse_args()

site = args.site
if len(sys.argv)==1:
    print("Expecting you to pass the site name ./setup_site.py -h")
    sys.exit()


# Unpack Jasmin file
f = open('jules_inputs_jasmin.json')
json_data = json.load(f)

met_fname = json_data[site]['drive_file']
run_end = json_data[site]['main_run_end']
run_start = json_data[site]['main_run_start']
lat = json_data[site]['latitude']
lon = json_data[site]['longitude']
spin_end = json_data[site]['spinup_end']
spin_start = json_data[site]['spinup_start']
timestep_length = json_data[site]['data_period']
z1_tq = json_data[site]['z1_tq_in']
z1_uv = json_data[site]['z1_uv_in']
output_dir = '../../outputs'


"""
met_fname = "AU-Tum_2002-2017_OzFlux_Met.nc"
run_end = "2018-01-01 00:00:00"
run_start = "2002-01-01 00:00:00"
lat = -35.6566
lon = 148.1517
spin_end = "2018-01-01 00:00:00"
spin_start = "2002-01-01 00:00:00"
timestep_length = 3600
z1_tq = 43.2
z1_uv = 43.2
output_dir = '../../outputs'
"""

#
### Change all paths, site names, timesteps, etc
#


# Copy over all the files...
src_dir = 'namelists_template'
dest_dir = 'namelists/%s' % (site)
if os.path.isdir(dest_dir):
    shutil.rmtree(dest_dir)
shutil.copytree(src_dir, dest_dir)

#
## Ancillaries file
#

fn = "%s/ancillaries.nml" % (src_dir)
ofn = "%s/ancillaries.nml" % (dest_dir)

frac_fname = '../../../../data/PLUMBER2/ancillaries/site_igbp_class/frac_9tile/%s_frac.txt' % (site)
soil_fname ='../../../../data/PLUMBER2/ancillaries/site_hwsd_soil/%s_soils.txt' % (site)

nml = f90nml.read(fn)
nml['jules_frac']['file'] = frac_fname
nml['jules_soil_props']['file'] = soil_fname

os.remove(ofn)
nml.write(ofn)


#
## Drive file
#

fn = "%s/drive.nml" % (src_dir)
ofn = "%s/drive.nml" % (dest_dir)

met_fpath ='../../../../data/PLUMBER2/met/%s' % (met_fname)

nml = f90nml.read(fn)
nml['jules_drive']['file'] = met_fpath
nml['jules_drive']['data_period'] = timestep_length
nml['jules_drive']['data_start'] = run_start
nml['jules_drive']['data_end'] = run_end

os.remove(ofn)
nml.write(ofn)


#
## Output.nml file
#

fn = "%s/output.nml" % (src_dir)
ofn = "%s/output.nml" % (dest_dir)


run_id='%s_fluxnet2015' % (site)

nml = f90nml.read(fn)
nml['jules_output']['output_dir'] = output_dir
nml['jules_output']['run_id'] = run_id
nml['jules_output_profile']['profile_name'] = "out"
os.remove(ofn)
nml.write(ofn)


#
## timesteps.nml file
#

fn = "%s/timesteps.nml" % (src_dir)
ofn = "%s/timesteps.nml" % (dest_dir)

run_id='%s_fluxnet2015' % (site)

nml = f90nml.read(fn)
nml['jules_time']['main_run_end'] = run_end
nml['jules_time']['main_run_start'] = run_start
nml['jules_time']['timestep_len'] = timestep_length

nml['jules_spinup']['spinup_end'] = spin_end
nml['jules_spinup']['spinup_start'] = spin_start
os.remove(ofn)
nml.write(ofn)




#
## prescribed_data.nml file
#

fn = "%s/prescribed_data.nml" % (src_dir)
ofn = "%s/prescribed_data.nml" % (dest_dir)

lai_fname ='../../../../data/PLUMBER2/ancillaries/site_lai_pft/lai_5pft/%s_modis_lai_pft.nc' % (site)

nml = f90nml.read(fn)
nml['jules_prescribed_dataset']['file'] = lai_fname
nml['jules_prescribed_dataset']['data_period'] = timestep_length
nml['jules_prescribed_dataset']['data_end'] = run_end
nml['jules_prescribed_dataset']['data_start'] = run_start
os.remove(ofn)
nml.write(ofn)

#
## rose-app-run.conf
#

fn = "%s/rose-app-run.conf" % (src_dir)
ofn = "%s/rose-app-run.conf" % (dest_dir)

with open(fn, 'r') as fp :
  data = fp.read()

drive_file = "AT-Neu_2002-2012_FLUXNET2015_Met.nc"
new_drive_file = "%s" % (met_fname)
data = data.replace(drive_file, new_drive_file)

expt_id = "AT-Neu"
new_expt_id = "%s" % (site)
data = data.replace(expt_id, new_expt_id)

jules_out="/Users/xj21307/research/JULES/runs/fluxnet/AT_NEU_fluxnet/outputs/AT-Neu"
new_jules_out="jules_out = %s/%s" % (output_dir, site)
data = data.replace(jules_out, new_jules_out)

data_end = 'data_end="2013-01-01 00:00:00"'
new_data_end = 'data_end="%s"' % (run_end)
data = data.replace(data_end, new_data_end)

data_start = 'data_start="2002-01-01 00:00:00"'
new_data_start = 'data_start="%s"' % (run_start)
data = data.replace(data_start, new_data_start)

main_run_end = 'main_run_end="2013-01-01 00:00:00"'
new_main_run_end = 'main_run_end="%s"' % (run_end)
data = data.replace(main_run_end, new_main_run_end)

main_run_start = 'main_run_start="2002-01-01 00:00:00"'
new_main_run_start = 'main_run_start="%s"' % (run_start)
data = data.replace(main_run_start, new_main_run_start)

site_lat = 'site_lat=47.1167'
new_site_lat = "%d" % (lat)
data = data.replace(site_lat, new_site_lat)

site_lon = 'site_lon=11.3175'
new_site_lon = "%d" % (lon)
data = data.replace(site_lon, new_site_lon)

spinup_end = 'spinup_end="2013-01-01 00:00:00"'
new_spinup_end = "spinup_end %s" % (spin_end)
data = data.replace(spinup_end, new_spinup_end)

spinup_start = 'spinup_start="2002-01-01 00:00:00"'
new_spinup_start = "spinup_start=%s" % (spin_start)
data = data.replace(spinup_start, new_spinup_start)

timestep_len = 'timestep_len = 1800'
new_timestep_len = "timestep_len = %d" % (timestep_length)
data = data.replace(timestep_len, new_timestep_len)

z1_tq_in = 'z1_tq_in=2.33'
new_z1_tq_in = "%d" % (z1_tq)
data = data.replace(z1_tq_in, new_z1_tq_in)

z1_uv_in = 'z1_uv_in=2.33'
new_z1_uv_in = "%d" % (z1_uv)
data = data.replace(z1_uv_in, new_z1_uv_in)

data_period = 'data_period=1800'
new_tdata_period = "data_period = %d" % (timestep_length)
data = data.replace(data_period, new_tdata_period)

os.remove(ofn)
with open(ofn, 'w') as file:
  file.write(data)
