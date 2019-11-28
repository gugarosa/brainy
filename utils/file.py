import os
import zipfile
from zipfile import ZipFile


def zip_file(temp_folder, dest_path, _id):
    """Creates a .zip from a specific folder.

    Args:
        temp_folder (str): A temporary folder to have its contents zipped.
        dest_path (str): The destination path of the .zip.
        _id (str): Model's identifier.

    Returns:
        The path to the zipped file.

    """

    # Creates a temproary ZipFile
    temp_zipfile = ZipFile(file=dest_path, mode='w',
                           compression=zipfile.ZIP_BZIP2)

    # Gathering the initial root path
    main_root = list(os.walk(temp_folder))[0][0]

    # Defines a function to format the path's name
    def format_name(path): return os.path.join(
        _id, root, filename).replace(main_root, _id)

    # For every possible directory in the temporary folder
    for root, _, files in os.walk(temp_folder):
        # For every possible file in the files
        for filename in files:
            # Gathers the original path
            original_path = os.path.join(root, filename)

            # Writes the file to the ZipFile
            temp_zipfile.write(original_path, arcname=format_name(filename))

    # Closes the temporary ZipFile
    temp_zipfile.close()

    return temp_zipfile.filename


def unzip_file(zip_path, dest_path, _id):
    """ Inflates the zipfile in a folder created within the destination path.

    The folder will have as name the model's identifier.

    Args:
        zip_path (str): The path to the .zip file.
        dest_path (str): The destination path of the unzipped files.
        _id (str): Model's identifier.

    Returns:
        The path to the unzipped files.

    """

    # Creates a zip object
    zip_object = ZipFile(zip_path)

    # If there is an identifier
    if _id:
        # Joins the path
        final_dest = os.path.join(dest_path, _id)

    # If there is no identifier
    else:
        # Marks the destionation path as the initial variable
        final_dest = dest_path

    # Extracts the zip object
    zip_object.extractall(dest_path)

    return final_dest
