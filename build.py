from wand.image import Image
import os
import json
import argparse
import pathlib

argparser = argparse.ArgumentParser(description='DCS livery building utility')
argparser.add_argument('desc_json', type=argparse.FileType('r'), help='livery description JSON file')
argparser.add_argument('--out', type=pathlib.Path, help='name of output dir. "build/{livery_name}" is default')

args = argparser.parse_args()

desc = json.load(args.desc_json)
desc_dir = pathlib.Path(args.desc_json.name).parent
livery_name = desc['name']
textures_desc = desc['textures']
livery_dir = args.out or pathlib.Path('dcs_liveries_builds') / livery_name
try:
    os.makedirs(livery_dir)
except FileExistsError:
    pass
livery_dir = livery_dir.absolute()
description_lua = open(livery_dir / 'description.lua', 'w')
os.chdir(desc_dir)

print(f'name = "{livery_name}"', file=description_lua)
print('livery = {', file=description_lua)

for target in textures_desc:
    texture_desc = textures_desc[target]
    image = Image(filename=texture_desc[0])
    image_name, _ = os.path.splitext(texture_desc[0])
    texture = image.convert('dds')
    texture.compression = texture_desc[1]
    # texture.options['dds:weight-by-alpha'] = 'false'
    # texture.options['dds:mipmaps'] = '0'
    texture.save(filename=(livery_dir / image_name).with_suffix('.dds'))
    print(f'  {{"{target}", DIFFUSE, "{image_name}", false}},', file=description_lua)
    print(target)

print('}', file=description_lua)
