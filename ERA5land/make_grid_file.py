import pathlib as pl

grid_out = pl.Path('5arcmin_grid.txt')

resolution = 5 / 60 # 5 arc-minutes
west = 0
north = 90
east = 360
south = -90

xfirst = west + resolution / 2
yfirst = north - resolution / 2
xsize = int((east - west) / resolution)
ysize = int((north - south) / resolution)
gridsize = xsize * ysize

grid_lines = ['gridtype  = lonlat']
grid_lines += [f'gridsize  = {gridsize}']
grid_lines += [f'xsize     = {xsize}']
grid_lines += [f'ysize     = {ysize}']
grid_lines += ['xname     = longitude']
grid_lines += ['xlongname = "longitude"']
grid_lines += ['xunits    = "degrees_east"']
grid_lines += ['yname     = latitude']
grid_lines += ['ylongname = "latitude"']
grid_lines += ['yunits    = "degrees_north"']
grid_lines += [f'xfirst    = {xfirst}']
grid_lines += [f'xinc      = {resolution}']
grid_lines += [f'yfirst    = {yfirst}']
grid_lines += [f'yinc      = {-resolution}']

with open(grid_out, 'w') as f:
    f.write('\n'.join(grid_lines))
