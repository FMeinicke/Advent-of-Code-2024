from __future__ import annotations

from importlib.resources import files

from . import print_day


def get_input() -> str:
    with (files("solutions.inputs") / "09.txt").open() as file:
        return file.read().strip()


class Region:
    start_block: int
    length: int

    def __init__(self, start_block: int, length: int) -> None:
        self.start_block = start_block
        self.length = length

    def checksum(self) -> int:
        return 0


class FreeSpace(Region):
    def __str__(self):
        return " ".join(["."] * self.length)


class File(Region):
    file_id: int

    def __init__(self, file_id: int, start_block: int, length: int) -> None:
        super().__init__(start_block, length)
        self.file_id = file_id

    def __str__(self):
        return " ".join([str(self.file_id)] * self.length)

    def checksum(self) -> int:
        return sum(
            i * self.file_id
            for i in range(self.start_block, self.start_block + self.length)
        )


class Disk:
    blocks: list[int | None]
    regions: list[Region]

    def __init__(self, disk_map: str) -> None:
        self.blocks = []
        for i, char in enumerate(disk_map):
            if i % 2 == 0:
                self.blocks.extend([i // 2] * int(char))
            else:
                self.blocks.extend([None] * int(char))

        self.regions = []
        file_id = None
        start_block = 0
        length = 0
        for i, block in enumerate(self.blocks):
            if file_id != block:
                if length > 0:
                    self.regions.append(
                        FreeSpace(start_block, length)
                        if file_id is None
                        else File(file_id, start_block, length)
                    )
                file_id = block
                start_block = i
                length = 1
            else:
                length += 1
        self.regions.append(
            FreeSpace(start_block, length)
            if file_id is None
            else File(file_id, start_block, length)
        )

    def block_str(self) -> str:
        return " ".join(
            str(block) if block is not None else "." for block in self.blocks
        )

    def file_str(self) -> str:
        return " ".join(str(region) for region in self.regions)

    def defragment_blocks(self) -> None:
        print("Defragmenting disk by blocks (this may take a while)...")
        for i in range(len(self.blocks) - 1, -1, -1):
            if self.blocks[i] is not None:
                for j in range(i):
                    if self.blocks[j] is None:
                        self.blocks[j] = self.blocks[i]
                        self.blocks[i] = None
                        # print(f"Moving block {self.blocks[i]} from {i} to {j}")
                        # print(self.block_str())
                        break

    def defragment_files(self) -> None:
        print("Defragmenting disk by files (this may take a while)...")

        files = [region for region in self.regions if isinstance(region, File)]

        for file in files[::-1]:
            i = self.regions.index(file)
            # print(f"Processing file {file.file_id} at {file.start_block}")

            for j in range(i):
                if not isinstance(self.regions[j], FreeSpace):
                    continue

                # print(f"{j=}")
                free_space: FreeSpace = self.regions[j]
                if free_space.length == file.length:
                    # print(
                    #     f"Moving file {file.file_id} from {file.start_block} to {free_space.start_block} (full)"
                    # )
                    free_space.start_block, file.start_block = file.start_block, free_space.start_block
                    self.regions[i], self.regions[j] = free_space, file
                    # print(self.file_str())
                    break
                elif free_space.length > file.length:
                    # print(
                    #     f"Moving file {file.file_id} with length {file.length} from {file.start_block} to {free_space.start_block} (partial) -> free space now at {free_space.start_block + file.length} with length {free_space.length - file.length}"
                    # )
                    new_free_space_start_block, file.start_block = file.start_block, free_space.start_block
                    free_space.start_block += file.length
                    free_space.length -= file.length
                    self.regions[i] = FreeSpace(new_free_space_start_block, file.length)
                    self.regions.insert(j, file)
                    # print(self.file_str())
                    break

    def calculate_block_checksum(self) -> int:
        return sum(
            i * int(block) for i, block in enumerate(self.blocks) if block is not None
        )

    def calculate_file_checksum(self) -> int:
        return sum(region.checksum() for region in self.regions)

    def blocks_from_regions(self) -> None:
        self.blocks = []
        for region in self.regions:
            self.blocks.extend([region.file_id if isinstance(region, File) else None] * region.length)

def main():
    print_day(9, "Disk Fragmenter")

    # Part One: Defragment the disk blockwise and calculate the checksum
    disk = Disk(get_input())
    disk.defragment_blocks()
    print(f"Checksum of blockwise-defragmented disk: {disk.calculate_block_checksum()}")

    # Part Two: Defragment the disk by files and calculate the checksum
    disk = Disk(get_input())
    disk.defragment_files()
    disk.blocks_from_regions()
    print(f"Checksum of filewise-defragmented disk: {disk.calculate_file_checksum()} {disk.calculate_block_checksum()}")


if __name__ == "__main__":
    main()
