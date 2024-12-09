from __future__ import annotations

from solutions._09_disk_fragmenter import Disk

input = "2333133121414131402"


def test_09_disk_init():
    disk = Disk(input)
    assert str(disk) == "0 0 . . . 1 1 1 . . . 2 . . . 3 3 3 . 4 4 . 5 5 5 5 . 6 6 6 6 . 7 7 7 . 8 8 8 8 9 9"


def test_09_disk_defragment_blocks_and_checksum():
    disk = Disk(input)
    disk.defragment_blocks()
    assert disk.block_str() == "0 0 9 9 8 1 1 1 8 8 8 2 7 7 7 3 3 3 6 4 4 6 5 5 5 5 6 6 . . . . . . . . . . . . . ."
    assert disk.calculate_block_checksum() == 1928


def test_09_disk_defragment_files_and_checksum():
    disk = Disk(input)
    disk.defragment_files()
    assert disk.file_str() == "0 0 9 9 2 1 1 1 7 7 7 . 4 4 . 3 3 3 . . . . 5 5 5 5 . 6 6 6 6 . . . . . 8 8 8 8 . ."
    assert disk.calculate_file_checksum() == 2858
    disk.blocks_from_regions()
    assert disk.block_str() == "0 0 9 9 2 1 1 1 7 7 7 . 4 4 . 3 3 3 . . . . 5 5 5 5 . 6 6 6 6 . . . . . 8 8 8 8 . ."
    assert disk.calculate_block_checksum() == 2858


def test_09_disk_defragment_files_and_checksum_2():
    disk = Disk("12345")
    assert disk.file_str() == "0 . . 1 1 1 . . . . 2 2 2 2 2"
    disk.defragment_files()
    assert disk.file_str() == "0 . . 1 1 1 . . . . 2 2 2 2 2"
    assert disk.calculate_file_checksum() == 132
    disk.blocks_from_regions()
    assert disk.block_str() == "0 . . 1 1 1 . . . . 2 2 2 2 2"
    assert disk.calculate_block_checksum() == 132
