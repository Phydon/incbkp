import os
from blake3 import blake3
from icecream import ic
from pathlib import Path, PurePath


TESTPATH1: str = "test1.txt"
TESTPATH2: str = "test2.txt"
TESTDIR1: str = "testdiroriginal"
TESTDIR2: str = "testdirbackup"


def main() -> None:
    # get structure of original directory
    (odires, ofiles) = walkdir(TESTDIR1)

    # get structure of backup directory
    (bdires, bfiles) = walkdir(TESTDIR2)

    # compare both structures


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
    # HINT returns False if 2 files have the same content but where last modified at different times
    return True if metadata(Path(path1)) == metadata(Path(path2)) else False


def create_hash(content: bytes) -> str:
    # FIXME hashes differ to reading bytes via read_file function
    # if isinstance(content, str):
    #     content = content.encode()

    # Workaround for ERROR above
    assert isinstance(content, bytes), "File content not converted to bytes properly"

    return blake3(content, max_threads=blake3.AUTO).hexdigest()


def verify_hash(hash1: str, hash2: str) -> bool:
    # HINT returns True if content is the same, even when files where last modified at different times
    return True if hash1 == hash2 else False


def verify_file_hashes(path1: Path, path2: Path) -> bool:
    content1 = read_file(path1)
    content2 = read_file(path2)
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

    print(f"Comparing files:\n  {file1}\n  {file2}")

    if verify_metadata(file1, file2):
        return True
    elif verify_file_hashes(file1, file2):
        return True
    # elif full_mode:
    #     # optional if full_mode flag is set
    #     return True if verify_fullcontent(read_file(file1), read_file(file2)) else False
    else:
        return False


def walkdir(directory: str) -> (list[str], list[str]):
    dirlist = []
    filelist = []
    for root, dirs, files in Path(directory).walk(on_error=print):
        for dir in dirs:
            dirlist.append(os.path.join(root, dir))
        for file in files:
            filelist.append(os.path.join(root, file))

    return (dirlist, filelist)


def strip_root_from_file(file: str) -> str:
    path = [c for c in PurePath(file).parts[1:]]

    # if only filename is given return filename
    if len(path) < 1:
        return file

    fullpath = PurePath("")
    for c in path:
        fullpath = fullpath.joinpath(c)

    return fullpath


def find_corresponding_counterpart(file: Path, dirs: list[str]) -> bool:
    # find corresponding counterpart (filename) in other directory and return the whole path to that file in the other directory
    file = strip_root_from_file(file)
    for f in dirs:
        f = strip_root_from_file(f)

        if file.match(Path(f)):
            return True

    return False


def store_path_and_hash(path: Path, hash: str):
    # TODO store the filepath and the corresponding hash of the filecontent in a separate file
    # To check whether a file has change or not, calculate the hash for the filecontent and compare to stored hash
    return


def test() -> None:
    content1 = read_file(TESTPATH1)
    ic(content1)
    content2 = read_file(TESTPATH2)
    ic(content2)

    print("=" * 20)

    ic(verify_fullcontent(content1, content2))

    print("=" * 20)

    hash = create_hash(content1)
    ic(hash)
    hash = create_hash(content2)
    ic(hash)

    print("=" * 20)

    ic(verify_file_hashes(TESTPATH1, TESTPATH2))

    print("=" * 20)

    meta1 = metadata(Path(TESTPATH1))
    meta2 = metadata(Path(TESTPATH2))
    ic(meta1)
    ic(meta2)

    print("=" * 20)

    ic(verify_metadata(TESTPATH1, TESTPATH2))

    print("=" * 20)

    ic(compare_files(TESTPATH1, TESTPATH2))

    print("=" * 20)


def test2():
    dirs1, files1 = walkdir(TESTDIR1)
    ic(dirs1)
    ic(files1)

    print("=" * 20)

    dirs2, files2 = walkdir(TESTDIR2)
    ic(dirs2)
    ic(files2)

    print("=" * 20)

    ic("Processing ...")

    for file1, file2 in zip(files1, files2):
        # TODO FIXME what if new file detected in one directory?
        if compare_files(file1, file2):
            print("=> Nothing changed")
        else:
            print("=> Files changed -> backup needed")


def test3() -> None:
    print("=" * 20)
    dirs1, files1 = walkdir(TESTDIR1)
    dirs2, files2 = walkdir(TESTDIR2)
    print("=" * 20)
    # ic(find_corresponding_counterpart(Path("new.txt"), files1))
    # print("=" * 20)
    # ic(find_corresponding_counterpart(Path(TESTPATH1), files1))
    # print("=" * 20)

    for file in files1:
        if not find_corresponding_counterpart(file, files2):
            print(f"Do backup: {file}")
        else:
            print("compare file hashes -> check if data has changed")


if __name__ == "__main__":
    # main()
    # test()
    # test2()
    test3()
