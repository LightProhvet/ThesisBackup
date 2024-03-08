import pyrealsense2 as rs
import numpy as np
import cv2


# static format and frame rate
def start_png_pipeline(height=640, width=480):
    pipeline = rs.pipeline()
    config = rs.config()

    # config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, height, width, rs.format.bgr8, 30)

    profile = pipeline.start(config)
    return pipeline, config, profile

# we cannot access file management here... :O