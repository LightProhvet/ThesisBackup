# https://learnopencv.com/paddlepaddle/

# see also https://learnopencv.com/segment-anything/
#paddleseg and paddle docs are available in their github
# import paddle
from PIL import Image as PILImage
import numpy as np
import cv2
import pyrealsense2 as rs
import time
from RealSense.file_management import png_save_lib as png_lib
# paddle imports
from paddleseg.deploy.infer import DeployConfig
from paddle.inference import create_predictor
from paddle.inference import Config as PredictConfig
from paddleseg import models as PaddleModels
from paddleseg.core import predict


def get_pseudo_color_map(pred, name, color_map=None):
    pred_mask = PILImage.fromarray(pred.astype(np.uint8), mode='P')
    if color_map is None:
        color_map = get_color_map_list(256)
    pred_mask.putpalette(color_map)
    pred_mask.save(name)


def get_color_map_list(num_classes, custom_color=None):
    num_classes += 1
    color_map = num_classes * [0, 0, 0]
    for i in range(0, num_classes):
        j = 0
        lab = i
        while lab:
            color_map[i * 3] |= (((lab >> 0) & 1) << (7 - j))
            color_map[i * 3 + 1] |= (((lab >> 1) & 1) << (7 - j))
            color_map[i * 3 + 2] |= (((lab >> 2) & 1) << (7 - j))
            j += 1
            lab >>= 3
    color_map = color_map[3:]

    if custom_color:
        color_map[:len(custom_color)] = custom_color
    return color_map


class Predictor:
    def __init__(self, config, name='segmentation_map.png'):
        self.name = name
        self.cfg = DeployConfig(config)
        self._init_base_config()
        self._init_gpu_config()
        self.predictor = create_predictor(self.pred_cfg)

    def _init_base_config(self):
        self.pred_cfg = PredictConfig(self.cfg.model, self.cfg.params)
        self.pred_cfg.enable_memory_optim()
        self.pred_cfg.switch_ir_optim(True)

    def _init_gpu_config(self):
        self.pred_cfg.enable_use_gpu(100, 0)

    def run(self, img_path):
        input_names = self.predictor.get_input_names()
        input_handle = self.predictor.get_input_handle(input_names[0])
        output_names = self.predictor.get_output_names()
        output_handle = self.predictor.get_output_handle(output_names[0])
        results = []
        frame = img_path
        data = np.array([self._preprocess(frame)])
        input_handle.reshape(data.shape)
        input_handle.copy_from_cpu(data)
        self.predictor.run()
        results = output_handle.copy_to_cpu()
        self._postprocess(results)

        return cv2.imread(self.name)

    def _preprocess(self, img):
        data = {}
        data["img"] = img
        return self.cfg.transforms(data)["img"]

    def _postprocess(self, results):
        get_pseudo_color_map(results[0], self.name)


def video_inference(video, seg_weight, PaddleEngine, video_name):
    video = cv2.VideoCapture(video)
    i = 0
    while True:
        ret, frame = video.read()
        if not ret:
            break
        if i == 0:
            shape = frame.shape
            out = cv2.VideoWriter(
                video_name,
                cv2.VideoWriter_fourcc(*"mp4v"),
                video.get(cv2.CAP_PROP_FPS),
                (shape[1], shape[0]),
            )

        segPred = PaddleEngine.run(frame)
        frame_resized = frame
        predBlend = cv2.addWeighted(
            frame_resized, 1 - seg_weight, segPred, seg_weight, 0
        )
        out.write(predBlend)
        i += 1

    video.release()
    out.release()


# praegu töötab, aga mitte veel piisavalt kiiresti ning antud mudel ei sobi üldse sisetingimustesse.
if __name__ == '__main__':
    # set variables
    save = True
    path = "../data/realsense/"
    CONFIG = "paddlepaddle_data/deploy.yaml"
    seg_weight = 0.3

    height = 1280
    width = 720
    color_format = rs.format.bgr8
    depth_format = rs.format.z16
    frame_rate = 30


    # start stream

    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.color, height, width, color_format, frame_rate)
    config.enable_stream(rs.stream.depth, height, width, depth_format, frame_rate)

    profile = pipeline.start(config)

    # get model:
    PaddleEngine = Predictor(CONFIG)
    # backbone = False  # this should be smth
    # model = PaddleModels.pp_liteseg.PPLiteSeg(num_classes=30, backbone=backbone)
    # predict(
    #         model,
    #         model_path='output/best_model/model.pdparams',# Model path
    #         transforms=transforms, # Transform.Compose， Preprocess the input image
    #         image_list=image_list, # List of image paths to be predicted。
    #         image_dir=image_dir, # The directory where the picture to be predicted is located
    #         save_dir='output/results' # Output path
    #     )
    path = "../data/paddlepaddle/"
    png_lib.make_clean_folder(path, check=False)
    try:
        while True:
            get_start = time.time()
            # for delay in range(10):
            frames = pipeline.wait_for_frames()
            eval_start = time.time()
            color_frame = frames.get_color_frame()
            depth_frame = frames.get_depth_frame()
            # support = color_frame.supports_frame_metadata()
            # rs.frame_metadata_value.__annotations__
            # if support:
            #     metadata = color_frame.get_frame_metadata(np.)
            color_image = np.asanyarray(color_frame.get_data())
            depth_image = np.asanyarray(depth_frame.get_data())

            color_image = cv2.resize(color_image, (960, 720))
            resized_color_image = color_image[..., ::-1]
            # file_saved = save_png(color_image, path, make_path=False)

            # # resize images to match for hstack
            # color_colormap_dim = color_image.shape
            # if segmentated_image_dim != color_colormap_dim:
            #     resized_color_image = cv2.resize(resized_color_image,
            #                                      dsize=(segmentated_image_dim[1], segmentated_image_dim[0]),
            #                                      interpolation=cv2.INTER_AREA)
            # images = np.hstack((resized_color_image, segmentated_image))

            shape = color_image.shape
            # out = cv2.VideoWriter(
            #     video_name,
            #     cv2.VideoWriter_fourcc(*"mp4v"),
            #     video.get(cv2.CAP_PROP_FPS),
            #     (shape[1], shape[0]),
            # )

            segPred = PaddleEngine.run(color_image)
            frame_resized = color_image
            predBlend = cv2.addWeighted(
                frame_resized, 1 - seg_weight, segPred, seg_weight, 0
            )
            end = time.time()
            print("eval time: " + str(end-eval_start))
            print("full time: " + str(end-get_start))
            png_lib.save_png(color_image, path, make_path=False)
            png_lib.save_png(segPred, path, make_path=False)
            png_lib.save_png(predBlend, path, make_path=False)
            # Show images
            cv2.namedWindow('RealSense', cv2.WINDOW_NORMAL)
            cv2.imshow('RealSense', predBlend)
            key = cv2.waitKey(1)
            if key & 0xFF == ord('q') or key == 27:
                cv2.destroyAllWindows()
                break
    finally:
        pipeline.stop()