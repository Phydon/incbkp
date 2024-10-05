from blake3 import blake3
from pathlib import Path


TESTPATH1: str = "test1.txt"
TESTPATH2: str = "test2.txt"


def main() -> None:
    pass


def read_file(path: Path) -> bytes:
    with open(path, "rb") as f:
        content = f.read()

    return content


# def comparision_mode() -> str:
#     # TODO
#     mode1 = "metadata"
#     mode2 = "filehash"
#     mode3 = "fullcontent"


def verify_fullcontent(content1: str, content2: str) -> bool:
    return True if content1 == content2 else False


def metadata(path: Path) -> list[str]:
    # use lstat => don't follow symbolic links
    return [
        # File mode: file type and file mode bits (permissions)
        path.lstat().st_mode,
        # User identifier of the file owner
        path.lstat().st_uid,
        # Group identifier of the file owner
        path.lstat().st_gid,
        # Size of the file in bytes, if it is a regular file or a symbolic link. The size of a symbolic link is the length of the pathname it contains, without a terminating null byte
        path.lstat().st_size,
        # Time of most recent content modification expressed in seconds
        path.lstat().st_mtime,
    ]


def verify_metadata(path1: str, path2: str) -> bool:
    # INFO returns False if 2 files have the same content but where last modified at different times
    return True if metadata(Path(path1)) == metadata(Path(path2)) else False


def create_hash(content: bytes) -> str:
    # FIXME hashes differ to reading bytes via read_file function
    # if isinstance(content, str):
    #     content = content.encode()

    # Workaround for ERROR above
    assert isinstance(content, bytes), "File content not converted to bytes properly"

    return blake3(content, max_threads=blake3.AUTO).hexdigest()


def verify_hash(hash1: str, hash2: str) -> bool:
    # INFO returns True if content is the same, even when files where last modified at different times
    return True if hash1 == hash2 else False


def verify_file_hashes(path1: Path, path2: Path) -> bool:
    content1 = read_file(TESTPATH1)
    content2 = read_file(TESTPATH2)
    hash1 = create_hash(content1)
    hash2 = create_hash(content2)

    return verify_hash(hash1, hash2)


def compare_files(file1: Path, file2: Path) -> bool:
    # first check file metadata
    # if they are the same -> return true
    # if not, compare file hashes
    # if they are the same -> return true
    # if not, return false
    # (optionally compare file content directly)

    if verify_metadata(file1, file2):
        print(f"Checking metadata of:\n\t{file1}\n\t{file2}")
        return True
    elif verify_file_hashes(file1, file2):
        print(f"Checking hashes of:\n\t{file1}\n\t{file2}")
        return True
    # elif full_mode:
    #     # optional if full_mode flag is set
    #     return True if verify_fullcontent(read_file(file1), read_file(file2)) else False
    else:
        return False


def test() -> None:
    content1 = read_file(TESTPATH1)
    print(content1)
    content2 = read_file(TESTPATH2)
    print(content2)

    print("=" * 20)

    print(verify_fullcontent(content1, content2))

    print("=" * 20)

    hash = create_hash(content1)
    print(hash)
    hash = create_hash(content2)
    print(hash)

    print("=" * 20)

    print(verify_file_hashes(TESTPATH1, TESTPATH2))

    print("=" * 20)

    meta1 = metadata(Path(TESTPATH1))
    meta2 = metadata(Path(TESTPATH2))
    print(meta1)
    print(meta2)

    print("=" * 20)

    print(verify_metadata(TESTPATH1, TESTPATH2))

    print("=" * 20)


def test2():
    compare_files(TESTPATH1, TESTPATH2)


if __name__ == "__main__":
    # main()
    test()
    test2()
