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


def metadata(path: Path) -> str:
    # use lstat => don't follow symbolic links
    return path.lstat()


def verify_metadata(path1: str, path2: str) -> bool:
    # INFO returns False if 2 files have the same content but where created at different times
    return True if metadata(Path(path1)) == metadata(Path(path2)) else False


def create_hash(content: bytes) -> str:
    # FIXME hashes differ to reading bytes via read_file function
    # if isinstance(content, str):
    #     print("isinstance str -> converting")
    #     content = content.encode()

    # Workaround for ERROR above
    assert isinstance(content, bytes), "File content not converted to bytes properly"

    return blake3(content, max_threads=blake3.AUTO).hexdigest()


def verify_hash(hash1: str, hash2: str) -> bool:
    # INFO returns True if content is the same, even when files where created at different times
    return True if hash1 == hash2 else False


def verify_files(path1: Path, path2: Path) -> bool:
    content1 = read_file(TESTPATH1)
    content2 = read_file(TESTPATH2)
    hash1 = create_hash(content1)
    hash2 = create_hash(content2)

    return verify_hash(hash1, hash2)


def test() -> None:
    content1 = read_file(TESTPATH1)
    print(content1)
    hash = create_hash(content1)
    print(hash)

    content2 = read_file(TESTPATH2)
    print(content2)
    hash = create_hash(content2)
    print(hash)

    print("=" * 20)

    print(verify_files(TESTPATH1, TESTPATH2))

    print("=" * 20)

    meta1 = metadata(Path(TESTPATH1))
    meta2 = metadata(Path(TESTPATH2))
    print(meta1)
    print(meta2)

    print("=" * 20)

    print(verify_metadata(TESTPATH1, TESTPATH2))

    print("=" * 20)


if __name__ == "__main__":
    # main()
    test()
