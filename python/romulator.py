import os
import re
import xml.etree.ElementTree as ET

# Global vars
romdir = './roms'
datdir = "./dats"
tosortdir = './tosort'

# make sure subfolders still exist
def make_dirs():
    try:
        os.makedirs(tosortdir, mode=0o777, exist_ok=True)
        os.makedirs(romdir, mode=0o777, exist_ok=True)
        os.makedirs(datdir, mode=0o777, exist_ok=True)
    except:
        print("Couldn't create directories!")    
        exit(100)

def search_namespace(line):
    ns = re.search(r"xmlns:(\w+)=\"(.*)\"\s", line)
    if ns is not None:
        return ns

def open_dat_file():
    try:
        for root, subdirs, datfiles in os.walk(datdir):
            # Probing namespace on dat files
            # TODO folder zip etc...
            for dat in datfiles:
                with open(f'./{datdir}/{dat}', 'r') as input_file:
                    xml = [ input_file.read() ]
                    # Go through xml file and return namespace
                    for element in xml:
                        if 'datafile' in element:
                            ns = search_namespace(element)
                            namespace1 = ns[1]
                            namespace2 = ns[2]

                tree = ET.parse(f"./{datdir}/{dat}")
                root = tree.getroot()
                ET.register_namespace(namespace1, namespace2)

                # create subfolders for rom sets
                for romset in root.findall('.//header/name'):
                    rset = f"./{romdir}/{romset.text}"
                    os.makedirs(rset, mode=0o777, exist_ok=True)
                
                items = list(tree.iter())
                for i, item in enumerate(items):
                    print(i)
                    print(item.tag)
                    if item.tag == "game":
                        item.values()
#                        next_item = items[i + 1]

#                for game_name in root:
                    #for game in game_name.items():
                        # Adding name
                        #if 'name' in game[0]:
                        #    print("Game name: {}".format(game[1]))
                        #if 'id' in game[0]:
                        #    print("Game id: {}".format(game[1]))

                        #print(game_name.attrib.values())
#                        for rom_name in root.iter():
###                            for rom in rom_name.items():
  #                              if 'name' in rom[0]:
  #                                  print(rom[0])
  #                                  print("ROM name: {}".format(rom[1]))
                                #if 'size' in rom[0]:
                                #    print("ROM size: {}".format(rom[1]))
                                #if 'crc' in rom[0]:
                                #    print("ROM CRC: {}".format(rom[1]))
                                #if 'md5' in rom[0]:
                                #    print("ROM MD5: {}".format(rom[1]))
                                #if 'sha1' in rom[0]:
                                #    print("ROM SHA1: {}".format(rom[1]))


    except:
        print("Couldn't read dat files ...")
        exit(200)

make_dirs()
open_dat_file()

