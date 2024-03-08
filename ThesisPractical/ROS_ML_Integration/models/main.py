from ObjectDetection import segmentation
import pyrealsense2 as rs
import numpy as np
import cv2

from RealSense.file_management.png_save_lib import make_clean_folder, save_png


if __name__ == '__main__':
    # set variables
    save = True
    path = "../data/realsense/"
    make_clean_folder(path, check=False)

    height = 640
    width = 480
    color_format = rs.format.bgr8
    depth_format = rs.format.z16
    frame_rate = 30

    # TODO: 1) setup:
    #  a) realsense stream - this should ultimately be a ROS2 talker
    #       1. Get device 2. Check/choose sensors 3. Start pipeline  4. forward/save data while running
    #  b) model - this should ultimately be a ROS2 listener.
    #       1. Get model 2. Check for image / listen 2.5. format image 3. label 4. forward data

    # start stream

    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.color, height, width, color_format, frame_rate)
    config.enable_stream(rs.stream.depth, height, width, depth_format, frame_rate)

    profile = pipeline.start(config)

    # get model:
    model = segmentation.get_model(2)  # 2 = deeplab, 1 = fcn, others not supported yet (defaults to 1)
    try:
        while True:
            for delay in range(30):
                frames = pipeline.wait_for_frames()

            color_frame = frames.get_color_frame()
            depth_frame = frames.get_depth_frame()
            # support = color_frame.supports_frame_metadata()
            # rs.frame_metadata_value.__annotations__
            # if support:
            #     metadata = color_frame.get_frame_metadata(np.)
            color_image = np.asanyarray(color_frame.get_data())
            depth_image = np.asanyarray(depth_frame.get_data())


            resized_color_image = color_image[..., ::-1]
            file_saved = save_png(color_image, path, make_path=False)

            segmentated_image = segmentation.segment_image(model, file_saved)

            # resize images to match for hstack
            segmentated_image_dim = segmentated_image.shape
            color_colormap_dim = color_image.shape
            if segmentated_image_dim != color_colormap_dim:
                resized_color_image = cv2.resize(resized_color_image,
                                                 dsize=(segmentated_image_dim[1], segmentated_image_dim[0]),
                                                 interpolation=cv2.INTER_AREA)
            images = np.hstack((resized_color_image, segmentated_image))

            # Show images
            cv2.namedWindow('RealSense', cv2.WINDOW_NORMAL)
            cv2.imshow('RealSense', images)
            key = cv2.waitKey(1)
            if key & 0xFF == ord('q') or key == 27:
                cv2.destroyAllWindows()
                break
    finally:
        pipeline.stop()
