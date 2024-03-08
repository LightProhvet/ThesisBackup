from RealSense import sensor as s_h
from RealSense.file_management.png_save_lib import make_clean_folder
from RealSense.sensor_management.png_mode import start_png_pipeline
from ObjectDetection import segmentation
from torch import max
import imageio
import matplotlib.pyplot as plt
from pathlib import Path


def show_img_and_predictions(img_fname):
  """ Show the original RGB image, and then the overlaid predictions. """
  fname_stem = Path(img_fname).stem
  rgb_img = imageio.imread(f'/content/{img_fname}')
  fig = plt.figure(figsize=(14,8))
  plt.imshow(rgb_img)
  plt.axis('off')
  plt.show()
  overlaid_img = imageio.imread(f'/content/{fname_stem}_overlaid_classes.jpg')
  fig = plt.figure(figsize=(14,8))
  plt.imshow(overlaid_img)
  plt.axis('off')
  plt.show()


if __name__ == '__main__':
    path = "../data/realsense/"
    make_clean_folder(path, check=False)

    pipeline, config, profile = start_png_pipeline()
    pipeline, config, profile, files = s_h.run_save_buffer(pipeline, config, profile, path=path, stop_pipeline=True, img_count=1)
    model = segmentation.get_model(2)
    model.eval()

    for image in files:

        result = segmentation.segment_image_input(image, show_original=True)
        # Perform argmax to get the predicted class index for each pixel

        # Convert the tensor to a NumPy array
        print("OK")

