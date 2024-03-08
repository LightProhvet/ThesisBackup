# import fiftyone as fo
# import fiftyone.zoo as foz
import numpy as np

from .file_management import png_save_lib as png_lib
# from sensor_management import png_mode


def run_save_buffer(pipeline, config, profile, path="../data/realsense/", img_count=10, stop_pipeline=False):
    i = 0
    file_list = []
    try:
        while i < img_count:
            for delay in range(30):
                frames = pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()

            color_image = np.asanyarray(color_frame.get_data())
            print(f"Got shape:{color_image.shape}")
            color_image = color_image[..., ::-1]
            file_saved = png_lib.save_png(color_image, path, make_path=False)
            file_list.append(file_saved)
            i += 1
    finally:
        if stop_pipeline:
            pipeline.stop()
    print(f"Succesfully saved {i} images.")
    return pipeline, config, profile, file_list


def get_next_image(pipeline, config, profile, save=True, path="../data/realsense/", color=True, depth=True):
    color_image = color_frame = False
    depth_image = depth_frame = False
    # try:
    for delay in range(30):
        frames = pipeline.wait_for_frames()

    if color:
        color_frame = frames.get_color_frame()
    if depth:
        depth_frame = frames.get_depth_frame()

    if color_frame:
        color_image = np.asanyarray(color_frame)

    if depth_frame:
        pass

    if save:
        color_image = color_image[..., ::-1]
        # TODO: add this to context or smth?
        file_saved = png_lib.save_png(color_image, path, make_path=False)

    return pipeline, config, profile, color_image, depth_image

# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     path = "../data/realsense/"
#     png_lib.make_clean_folder(path, check=True)
#
#     # TODO: 1) setup:
#     #  a) realsense stream - this should ultimately be a ROS2 talker
#     #       1. Get device 2. Check/choose sensors 3. Start pipeline  4. forward/save data while running
#     #  b) model - this should ultimately be a ROS2 listener.
#     #       1. Get model 2. Check for image / listen 2.5. format image 3. label 4. forward data
#
#     # 1.a)
#     pipeline, config, profile = png_mode.start_png_pipeline()
#     run_save_buffer(pipeline, config, profile, path=path, stop_pipeline=True)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
