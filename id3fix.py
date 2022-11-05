# Script to remove Detriti as artist from flacs

import music_tag
import re
from pathlib import Path
from dataclasses import dataclass


DETRITI_DIR = "/mnt/d/detriti"


@dataclass
class AlbumInfo:
    artist: str
    name: str

def process_song(p, album_info):
    f = music_tag.load_file(str(p))
    f["artist"] = album_info.artist
    f["album"] = album_info.name
    f.save()
    

def parse_album_dir_name(n):
    parts = n.split(" - ")
    return AlbumInfo(parts[1], parts[2])


def move_fixed(p):
    fixed_dir = Path( p.parent / "_fixed" / p.name )
    p.rename(fixed_dir)


def process_dir(p):
    print(f"Processing {p}")

    try:
        album_info = parse_album_dir_name(p.name)
    except IndexError:
        return

    songs = list(p.glob("*.flac"))
    print(album_info)

    for s in songs:
        process_song(s, album_info)

    move_fixed(p)


def main():
    p = Path(DETRITI_DIR)
    album_dirs = [x for x in p.iterdir() if x.is_dir()]

    for d in album_dirs:
        process_dir(d)


if __name__ == "__main__":
    print("Detriti fixer")
    main()
