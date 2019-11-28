import os
import zipfile
from zipfile import ZipFile


def zip_file(temp_folder: str, destination_zip_path: str, version_id: str) -> str:
    """Creates a zipfile will all contents of a folder.

    :param temp_folder: The folder that will have all of its contents on the
    first level zipped.
    :param destination_zip_path: Where the zipfile is going to be created.
    :param version_id: The ID of the current version
    :return: The path to the zipped file.
    """

    temp_zipfile = ZipFile(file=destination_zip_path, mode='w', compression=zipfile.ZIP_BZIP2)

    # os.walk returns three values: path to the current folder, folders within
    # this folder and files on this folder. The problem is that the path to the
    # current folder (main_root) is absolute (ie: starts on the main '/'). We
    # need to get rid of this to generate a zipfile starting from the main_root,
    # and not from /.
    # In order to do so, we keep track of main_root and generate a lambda that
    # replaces this part of the path by the model's version ID, as the generated
    # zip will contain only a folder, named with the model ID (hence the
    # replacement) and within it the files generated while training the model.
    main_root = list(os.walk(temp_folder))[0][0]

    format_name = lambda path: os.path.join(version_id, root, filename).replace(
        main_root, version_id)

    for root, dirs, files in os.walk(temp_folder):
        for filename in files:
            original_path = os.path.join(root, filename)
            temp_zipfile.write(original_path, arcname=format_name(filename))

    temp_zipfile.close()
    return temp_zipfile.filename


def unzip_file(zip_path: str, destination_path: str, version_id: str) -> str:
    """
    Inflates the zipfile in a folder created within the destionation_path. This
    folder will have as name the id of the model's version.

    :param self: Self object.
    :param default_path: Default path of saved models
    :param version_id: ID of trained version.
    :return: Unzipped file path.
    """

    import logging
    logging.info('Unzipping {}'.format(zip_path))
    zip_object = ZipFile(zip_path)

    # creates a new folder within the destination path that has as name the
    # id of the model version.
    if version_id:
        destination = os.path.join(destination_path, version_id)
    else:
        destination = destination_path
    zip_object.extractall(destination_path)
    return destination
