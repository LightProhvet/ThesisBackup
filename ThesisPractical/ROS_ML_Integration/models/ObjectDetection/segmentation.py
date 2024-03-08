# Example based on:
# https://colab.research.google.com/github/spmallick/learnopencv/blob/master/PyTorch-Segmentation-torchvision/intro-seg.ipynb#scrollTo=shnC_YQLeQ1v

from torchvision import models
from torchvision import transforms as torchT
import torch
import numpy as np
# local files
from PIL import Image
# from . import helpers
import helpers
import matplotlib.pyplot as plt
# from .file_management import png_save_lib as png_lib
from file_management import png_save_lib as png_lib

# models
# from paddleseg.models import PPLiteSeg

#random testing
import cv2



def segment(net, image, show_original=False, dev='cuda', resize=640):
    if show_original:
        show_image(image)
    """
    Resize the image to (256 x 256)
    CenterCrop it to (224 x 224)
    Convert it to Tensor - all the values in the image becomes between [0, 1] from [0, 255]
    Normalize it with the Imagenet specific values mean = [0.485, 0.456, 0.406], std = [0.229, 0.224, 0.225]
    And lastly, we unsqueeze the image so that it becomes [1 x C x H x W] from [C x H x W]
    """
    transform_mean = [0.485, 0.456, 0.406]
    transform_std = [0.229, 0.224, 0.225]
    transform = torchT.Compose([
        torchT.Resize(resize),  # Resizes the image to size 256 x 256
        #torchT.CenterCrop(224),  # Center Crops the image to have a resulting size of 224 x 224
        torchT.ToTensor(),  # Converts the image to type torch.Tensor and have values between [0, 1]
        torchT.Normalize(mean=transform_mean, std=transform_std)
        # Normalizes the image (in Tensor type) with the given mean and standard deviation
    ]
    )
    """
    T.Compose is a function that takes in a list in which each element is of transforms type and
    it returns a object through which we can pass batches of images 
    and all the required transforms will be applied to the images.
    """
    model_input = transform(image).unsqueeze(0)  # un-squeeze?

    out = net(model_input)['out']
    print(out.shape)  # torch.Size([img_count, class_count, img_height, img_width])

    """ 
    Now we format the output
    """
    unknown = torch.argmax(out.squeeze(), dim=0).detach().cpu().numpy()
    print(unknown.shape)  # image size: (height, width)
    print(np.unique(unknown))  # [, found_class_count]

    rgb = helpers.decode_segmap(unknown)
    show_image(rgb)
    return rgb


def get_model(model_nr, model_name=False):
    if model_name:
        model = model_name  # paddleseg.models.[model_name]

    elif model_nr == 2:
        model = models.segmentation.deeplabv3_resnet101(pretrained=1).eval()  # deeplab

    else:
        model = models.segmentation.fcn_resnet101(pretrained=True).eval()  # fully convolutional network
    return model


def show_image(img, axis='off'):
    plt.imshow(img)
    if axis == 'off':
        plt.axis('off')
    plt.show()


# Path can be a list of paths or a single path
def segment_image(net, path, show_original=False, dev='cuda', resize=640):
    if np.shape(path):
        all_images = []
        for image in path:
            rgb = segment_image(net, image, show_original, dev, resize)
            all_images.append(rgb)
        return all_images
    else:
        image = img = Image.open(path)
        if show_original:
            show_image(image)
        """
        Resize the image to (256 x 256)
        CenterCrop it to (224 x 224)
        Convert it to Tensor - all the values in the image becomes between [0, 1] from [0, 255]
        Normalize it with the Imagenet specific values mean = [0.485, 0.456, 0.406], std = [0.229, 0.224, 0.225]
        And lastly, we unsqueeze the image so that it becomes [1 x C x H x W] from [C x H x W]
        """
        transform_mean = [0.485, 0.456, 0.406]
        transform_std = [0.229, 0.224, 0.225]
        transform = torchT.Compose([
            torchT.Resize(resize),  # Resizes the image to size 256 x 256
            #torchT.CenterCrop(224),  # Center Crops the image to have a resulting size of 224 x 224
            torchT.ToTensor(),  # Converts the image to type torch.Tensor and have values between [0, 1]
            torchT.Normalize(mean=transform_mean, std=transform_std)
            # Normalizes the image (in Tensor type) with the given mean and standard deviation
        ]
        )
        """
        T.Compose is a function that takes in a list in which each element is of transforms type and
        it returns a object through which we can pass batches of images 
        and all the required transforms will be applied to the images.
        """
        model_input = transform(image).unsqueeze(0)  # un-squeeze?

        out = net(model_input)['out']
        print(out.shape)  # torch.Size([img_count, class_count, img_height, img_width])

        """ 
        Now we format the output
        """
        unknown = torch.argmax(out.squeeze(), dim=0).detach().cpu().numpy()
        print(unknown.shape)  # image size: (height, width)
        print(np.unique(unknown))  # [, found_class_count]
        rgb = helpers.decode_segmap(unknown)
        show_image(rgb)
        show_image(unknown)
        return rgb


def segment_image_input(input, use_model=2, show_original=False):
    path = "../data/realsense/"
    png_lib.make_clean_folder(path, check=False)
    model = get_model(use_model)
    result = segment_image(model, input, show_original=show_original)
    png_lib.save_png(result, path, make_path=False)
    return result


# # Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # fcn = models.segmentation.fcn_resnet101(pretrained=True).eval()  # fully convolutional network
    path = './data/images/bird.png'
    # path2 = ['./data/images/bird.png']
    img = Image.open(path)
    color_image = np.asanyarray(img)
    color_image = cv2.resize(color_image, (480, 640))

    print(color_image.shape)
    dlab = models.segmentation.deeplabv3_resnet101(pretrained=1).eval()

    segment(dlab, color_image)

# model = get_model(2)
# img = './data/images/bird.png'
# result = segment_image(model, img, show_original=True)
# print("GOOD")
