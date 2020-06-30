from wand.image import Image
from wand.exceptions import BlobError
from json.decoder import JSONDecodeError
import os
import json
import argparse
import pathlib

argparser = argparse.ArgumentParser(description='DCS livery building utility')
argparser.add_argument('desc_json', type=argparse.FileType('r'), help='livery description JSON file')
argparser.add_argument('--out', type=pathlib.Path, help='name of output dir. "build/{livery_name}" is default')

args = argparser.parse_args()

try:
    desc = json.load(args.desc_json)
except JSONDecodeError as exception:
    print('Failed to parse', args.desc_json.name)
    print(exception)
    exit(1)
desc_dir = pathlib.Path(args.desc_json.name).parent
livery_name = desc['name']
materials_desc = desc['textures']
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

converted = set()

def add_entry(node, texture_desc, material_property='DIFFUSE'):
    texture_file, compression = texture_desc
    image_name, _ = os.path.splitext(texture_file)
    image_name = pathlib.Path(f'{image_name}_{compression}')
    if texture_desc not in converted:
        try:
            image = Image(filename=texture_file)
        except BlobError:
            print(f'Failed to load {texture_desc} for {node}[{material_property}]')
            exit(2)
        print(f'Converting {texture_desc} for {node}[{material_property}]')
        texture = image.convert('dds')
        texture.compression = compression
        # texture.options['dds:weight-by-alpha'] = 'false'
        # texture.options['dds:mipmaps'] = '0'
        texture.save(filename=(livery_dir / image_name).with_suffix('.dds'))
        converted.add(texture_desc)
    else:
        print(f'Already converted {texture_desc} for {node}[{material_property}]')
    print(f'  {{"{node}", {material_property}, "{image_name}", false}},', file=description_lua)

for node in materials_desc:
    material_desc = materials_desc[node]
    if isinstance(material_desc, list):
        add_entry(node, tuple(material_desc))
    elif isinstance(material_desc, dict):
        for material_property in material_desc:
            add_entry(node, tuple(material_desc[material_property]),
                      material_property=material_property)

print('}', file=description_lua)
