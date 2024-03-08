import os
import shutil
import imageio


def make_clean_folder(path_folder, check=False, overwrite=False):
    if not os.path.exists(path_folder):
        os.makedirs(path_folder)
        return True
    else:
        if check:
            user_input = input("%s not empty. Overwrite? (y/n) : " % path_folder)
            if user_input.lower() == "y":
                shutil.rmtree(path_folder)
                os.makedirs(path_folder)
                return True
            else:
                return False
        elif overwrite:
            shutil.rmtree(path_folder)
            os.makedirs(path_folder)
            return True
        else:
            # print("%s not empty. Folder creation unsuccessful")
            return False


def get_files_in_folder(path):
    onlyfiles = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    return onlyfiles


def save_png(image, path, name="img", count=True, make_path=True):
    if make_path:
        make_clean_folder(path)  # ensures i have a path to write to
    if count:
        name = name + str(len(get_files_in_folder(path)))
    filename = path + name + ".png"
    imageio.imwrite(filename, image)

    return filename
