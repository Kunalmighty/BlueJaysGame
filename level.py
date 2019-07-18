""" Build level objects including maps, tiles, World objects and
    sprite lists """

import globes
import pygame
import world

LVL_FILES = ["lvls/level0.txt", "lvls/level1.txt", "lvls/level2.txt",
             "lvls/level3.txt", "lvls/level4.txt", "lvls/level5.txt"]
LVL_MAPS = ["maps/map0.txt", "maps/map1.txt", "maps/map2.txt",
            "maps/map3.txt", "maps/map4.txt", "maps/map5.txt"]
LVL_TILES = ["tiles/tiles0.txt", "tiles/tiles1.txt", "tiles/tiles2.txt",
             "tiles/tiles3.txt", "tiles/tiles4.txt", "tiles/tiles5.txt"]
LVL_SPRITES = []
LVL_WORLDS = []


def initialize_levels():
    """ load LVL_SPRITES, LVL_WORLDS, LVL_CAMERAS, and tile images
        for each level """

    for lvl in range(len(LVL_FILES)):
        build_level(lvl)
        build_spritelist(lvl)

        # World object created based on Global tiles object
        load_tiles(LVL_TILES[(lvl)])
        LVL_WORLDS.append(world.World(LVL_MAPS[(lvl)]))


def build_level(level_num):
    """ Build sprite list from text file mapping
    @param level_num 0 for level select, else level number """

    level = []
    platlist = []
    spikelist = []
    trigger = None
    wildcards = {}
    doors = {}
    file = open(LVL_FILES[(level_num)])
    for line in file:
        level.append(line)
    tofile = open("sprites.txt", 'w')
    for i in range(0, len(level)):
        if level[i].count("DICTIONARY") > 0:
            # Reached wildcard dictionary definitions, should
            # close file, parse wildcards, and exit the function.
            tofile.close()
            parse_wildcards(wildcards, level)
            parse_doors(doors)
            file.close()
            return
        for j in range(0, len(level[i])):
            symbol = level[i][j]
            if symbol == " ":
                pass
            elif symbol == "P":  # Generic platform (used for floor) start
                platlist.append((j, i))
            elif symbol == "M":  # End generic platform
                x, y = platlist.pop()
                sx, sy = x * 25 - 25, y * 25 + 10
                fx, fy = j * 25, i * 25 + 25 + 10
                tofile.write("%s %d %d %d %d\n" % ("P", sx, sy, fx, fy))
                if len(level[y - 1]) > x and i > 0 and \
                        level[y - 1][x] == "X":
                    tofile.write("PE\n")
            elif symbol == "G":  # Ghost enemy (floats up and down)
                tofile.write("%s %d %d\n" % ("GE", j * 25 - 25, i * 25 + 10))
            elif symbol == "g":  # Trigger ghost trigger position
                if trigger is None:
                    trigger = "%s %d %d" % ("TRGE", j * 25 - 25, i * 25 + 10)
            elif symbol == "x":  # Trigger ghost enemy position
                if trigger is not None:
                    trigger += " %d %d\n" % (j * 25 - 25, i * 25 - 200)
                    tofile.write(trigger)
                    trigger = None
            elif symbol == "B":  # start Book platform
                platlist.append((j, i))
            elif symbol == "K":  # end Book platform
                x, y = platlist.pop()
                l, t = x * 25 - 25, y * 25 + 10
                num = (j - x + 3) / 4
                tofile.write("%s %d %d %d\n" % ("B", l, t, num))
                if len(level[y - 1]) > x and i > 0 and \
                        level[y - 1][x] == "X":
                    tofile.write("PE\n")
            elif symbol == "p":
                platlist.append((j, i))
            elif symbol == "n" or symbol == "l" or symbol == "r":
                x, y = platlist.pop()
                sx, sy = x * 25 - 25, y * 25 + 10
                fx, fy = j * 25, i * 25 + 25 + 10
                tofile.write("%s %d %d %d %d %s\n" %
                             ("P2", sx, sy, fx, fy, symbol))
            elif symbol == "D":  # Door object
                tofile.write("%s %d %d\n" % ("D", j * 25 - 25,
                                             i * 25 + 25 + 10))  # +25 bottom
            elif symbol == "S":  # Player start position
                tofile.write("%s %d %d\n" % ("S", j * 25 - 25,
                                             i * 25 + 25 + 10))
            elif symbol == "<":  # Start spike object
                if j != 0:
                    spikelist.append((j, i))
            elif symbol == ">":  # End spike object
                if len(spikelist) > 0:
                    x, y = spikelist.pop()
                    l, t = x * 25 - 25, y * 25 - 10
                    num = (j - x + 3) / 4
                    tofile.write("%s %d %d %d\n" % ("SP", l, t, num))
            elif symbol == "I":  # Spider!
                tofile.write("%s %d %d\n" % ("I", j * 25 - 25, i * 25 + 10))
            elif symbol == "C":  # Chair
                tofile.write("%s %d %d\n" % ("C", j * 25 - 25,
                                             i * 25 + 10 + 25))
#            elif symbol == "!":  # Trigger enemies
#                key = level[i][j + 1]
#                if key not in triggers:
#                    triggers[key] = {}
#                if level[i][j + 2].isdigit():
#                   triggers[key]['type'] = level[i][j + 2]
#                    triggers[key]['t_pos'] = (j * 25 - 25, i * 25 + 10)
#                else:
#                    triggers[key]['e_pos'] = (j * 25 - 25, i * 25 + 10)
            elif symbol == "T":
                tofile.write("%s\n" % ("T"))
            elif symbol == "V":  # Minigame doors
                counter = 1
                number = ""
                while globes.is_numeric(number + level[i][j + counter]):
                    number += level[i][j + counter]
                    counter += 1
                number = int(number)
                tofile.write("MiniDoor %d %d %d\n" % (number, j * 25 - 25,
                             i * 25 + 10))
            elif symbol == "~":  # Paired doors
                # Use one character key for two doors to link them
                key = level[i][j + 1]
                if key not in doors:
                    doors[key] = []
                doors[key].append((j * 25 - 25, i * 25 + 10))
            elif symbol == "*":  # Wild card
                # Use one character key for the wildcard dictionary
                wildcards[level[i][j + 1]] = (j * 25 - 25, i * 25 + 10)

    tofile.close()
    file.close()


def parse_doors(doors):
    """ Parse a dictionary of tuples in lists of length two such that
        the the door at tuple1 links to the door at tuple2, vice versa """

    tofile = open("sprites.txt", 'a')

    for key, value in doors.items():
        if len(value) != 2:
            continue  # value should be lists of 2 for a door pair
        line = "DoorPr " + str(value[0][0]) + " " + str(value[0][1]) + \
               " " + str(value[1][0]) + " " + str(value[1][1])
        tofile.write(line + "\n")

    tofile.close()


def parse_wildcards(wildcards, level):
    """ Parse a dictionary of tuples given a level file with a
        DICTIONARY heading at the bottom.
        @param wildcards dictionary where key-value pairs represent
            key-(initial position) pairs and the dictionary is defined
            under a 'DICTIONARY' heading
        @param level the level file read into a 2D list with a
            DICTIONARY heading at the bottom """

    line = 0

    # Can assume "DICTIONARY" is present based on function call
    # so list index will not go out of range
    while (level[line].count("DICTIONARY") <= 0):
        line += 1
    line += 1  # Throw away the line containing "DICTIONARY" heading

    tofile = open("sprites.txt", 'a')
    while (line < len(level)):
        key = level[line][0]
        if key in wildcards:
            x_index, y_index = wildcards.pop(key)
            line_parse = level[line].split()
            line_parse.pop(0)  # Discard key at beginning of line
            line_parse.insert(1, str(x_index))
            line_parse.insert(2, str(y_index))
            tofile.write(" ".join(line_parse) + "\n")
        line += 1
    tofile.close()


def load_tiles(filename):
    """ Load tiles from background images in tiles/tile*.txt """

    file = open(filename)
    for line in file:
        code, image = line.strip().split()
        globes.Globals.TILES[code] = pygame.image.load(image).convert()
    file.close()


def build_spritelist(level_num):
    """ Build list of sprite descriptors from the sprite.txt generated by
        build_level call on a level """

    LVL_SPRITES.append([])
    file = open("sprites.txt")
    for line in file:
        LVL_SPRITES[level_num].append(list(line.strip().split()))
    file.close()
