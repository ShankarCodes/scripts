#!/usr/bin/env python3
"""
cleandir.py - A script for cleaning a directory by moving related
type of files to separate folders.
"""

# Extensions have to be space separated
import shutil
from pathlib import Path
import sys
import os
extensions = '''ebook:epub mobi azw azw3 iba djvu azw4 azw6 cbr cbz azw1
document:txt rtf md doc docx log odt rst tex wpd wps pdf
spreadsheet:xls xlsx ods csv ics vcf tsv
archive:7z a apk ar bz2 cab cpio deb dmg egg gz iso jar lha mar pea rar rpm s7z shar tar tbz2 tgz tlz war whl xpi zip zipx xz pak
executable: exe msi bin command com sh bat crx cpl dll
image:3dm 3ds max bmp dds gif jpg jpeg png psd xcf tga thm tif tiff yuv ai eps ps svg dwg dxf gpx kml kmz webp
video:3g2 3gp aaf asf avchd avi drc flv m2v m4p m4v mkv mng mov mp2 mp4 mpe mpeg mpg mpv mxf nsv ogg ogv ogm qt rm rmvb roq srt svi vob webm wmv yuv
audio:aac aiff ape au flac gsm it m3u m4a mid mod mp3 mpa pls ra s3m sid wav wma xm
code:c cc class clj cpp cs cxx el go h java lua m m4 php pl po py rb rs sh swift vb vcxproj xcodeproj xml diff patch html js json
web:html htm css js jsx less scss wasm php
font:eot otf ttf woff woff2
slide:ppt odp pptx'''


def parse_extensions(ext):
    """
    Parse the extensions as given in the format and convert it into a dictionary.
    <category>:<ext1> <ext2> <ext3> ....

    Args:
        ext (str): A string containing the extensions as the format given in the top of this file.

    Returns:
        dict: A dictionary representing the extensions with the key being the category
            and the value, a list containing all extensions as str.
    """
    extensions_map = {}
    for line in ext.split('\n'):
        try:
            category, extensions_list = line.split(':')
            extensions_list = extensions_list.split()
            extensions_list = list(
                filter(lambda x: x != '' or x != ' ', extensions_list))
            extensions_map[category] = extensions_list
        except Exception as e:
            print(e)
            print('WARNING: ERRORS WHILE READING EXTENSION LIST')
    return extensions_map


def get_category(extension, extension_map):
    """
    Gets the category of the extension like (ebook for a pdf file).
    Note: The extension must not start with a '.'

    Args:
        extension (str): String for which the category has to be found.
        extension_map (dict): A dictionary containing the category as the key, value is list of extensions.

    Returns:
        str: Returns a string which is the category of the given extension.
    """
    for category, extension_list in extension_map.items():
        if extension in extension_list:
            return category
    return ''


def get_files(path, recurse):
    """
    Lists all the files in a directory.
    Args:
        path (str): absolute path of the required directory to get files.
        recurse (bool): list all files by recursing through each subfolder or not.

    Yields:
        str: a single file name, if no files are left, yields a ''
    """
    files = None
    entries = []
    if path.exists():
        entries = path.glob('**/*' if recurse else '*')
    else:
        print(f'The given input path ({path}) does not exist')
        yield ''
    for entry in entries:
        if entry.is_file():
            yield os.path.abspath(str(entry))
    yield ''


def remove_prefix(string, prefix):
    if string.startswith(prefix):
        return string[len(prefix):]
    return string


def short(path):
    return remove_prefix(str(path), str(Path.cwd()) + '\\')


if __name__ == '__main__':
    """
    Main function of the program
    """

    # Create the extension map.
    ext_map = parse_extensions(extensions)
    errors = {}
    # Checks if enough arguments are provided
    if len(sys.argv) < 3:
        print('Usage: cleandir.py <directory to clean> <output directory>')
        print('OPTIONS')
        print('--recurse - To recursively move files DANGEROUS')
        print('--copy - Copies files instead of moving them')
    else:
        # cleaning_path is the path of the directory to be cleaned.
        cleaning_path = sys.argv[1]
        # out_path is the path of the output directory
        out_path = sys.argv[2]
        copy = recurse = False
        if '--copy' in sys.argv:
            copy = True
        if '--recurse' in sys.argv:
            recurse = True

        clean_path = Path(cleaning_path)
        output_path = Path(out_path)

        # If the paths are not absolute, convert them to absolute.
        if not clean_path.is_absolute():
            clean_path = Path.cwd() / cleaning_path
        if not output_path.is_absolute():
            output_path = Path.cwd() / out_path

        for path in get_files(clean_path, recurse):
            # Find out the extension and then find out the category to which the file belongs.
            extension = Path(path).suffix[1:].lower()
            category = get_category(extension, ext_map)
            if category == '':
                # The category of that extension has not been found.
                # Keept it as misc
                category = 'misc'
            if category.strip() != '' or category.strip() != ' ':
                try:
                    if os.path.isfile(str(clean_path / out_path)):
                        # If a file of the same name exists, directory creation will fail
                        # so ask the user to remove it.
                        print('Cannot create the output folder: '+out_path)
                        print(
                            'Please check if a file by the same name exists, and delete it.')
                        break
                    target_path = output_path / (category+'s')
                except Exception as e:
                    # Any other error has occured while creating output directory.
                    print('Error occured while creating output directory')
                    print('Check if a file by the same name exists')
                    break
                target_path.mkdir(parents=True, exist_ok=True)
                print("Copying" if copy else "Moving",
                      short(path), '=>', short(target_path))
                try:
                    # Move the folder to the target folder
                    if copy:
                        shutil.copy2(path, target_path)
                    else:
                        shutil.move(path, target_path)
                except shutil.Error as e:
                    errors[f'{"Copying" if copy else "Moving"} {short(path)} => {short(target_path)}:'] = str(
                        e)
                except Exception as e:
                    errors[f'{"Copying" if copy else "Moving"} {short(path)} => {short(target_path)}:'] = str(
                        e)
        print()
        print('='*5+' ERRORS '+'='*5)
        print()
        for incident, error in errors.items():
            print(incident, '-', error)
        print()
