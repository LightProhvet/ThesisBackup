
# http://pytorch.org/vision/main/models.html
from torchvision import models
from torchvision import transforms as torchT

import torch
import numpy as np
"""
static variables are just written into 'segment' function
"""
from PIL import Image
import matplotlib.pyplot as plt


def get_model():
    model = models.segmentation.deeplabv3_resnet101(pretrained=1).eval()  # deeplab
    return model

def decode_segmap(image, nc=21, class_color_map=False):  # nc = class count
    if not class_color_map:
        class_color_map = [(0, 0, 0),  # 0=background
                           # 1=aeroplane, 2=bicycle, 3=bird, 4=boat, 5=bottle
                           (128, 0, 0), (0, 128, 0), (128, 128, 0), (0, 0, 128), (128, 0, 128),
                           # 6=bus, 7=car, 8=cat, 9=chair, 10=cow
                           (0, 128, 128), (128, 128, 128), (64, 0, 0), (192, 0, 0), (64, 128, 0),
                           # 11=dining table, 12=dog, 13=horse, 14=motorbike, 15=person
                           (192, 128, 0), (64, 0, 128), (192, 0, 128), (64, 128, 128), (192, 128, 128),
                           # 16=potted plant, 17=sheep, 18=sofa, 19=train, 20=tv/monitor
                           (0, 64, 0), (128, 64, 0), (0, 192, 0), (128, 192, 0), (0, 64, 128)]

    label_colors = np.array(class_color_map)  # stores the colors for each of the classes, according to the index
    # create empty 2D matrices for all 3 channels
    # So, r, g, and b are arrays which will form the RGB channels for the final image. And each are of shape [H x W]
    # (which is same as the shape of image passed in)
    r = np.zeros_like(image).astype(np.uint8)
    g = np.zeros_like(image).astype(np.uint8)
    b = np.zeros_like(image).astype(np.uint8)

    # Now, we loop over each class color we stored in label_colors.
    # And we get the indexes in the image where that particular class label is present. (idx = image == l)
    # And then for each channel, we put its corresponding color to those pixels where that class label is present.
    for l in range(0, nc):
        idx = image == l
        r[idx] = label_colors[l, 0]
        g[idx] = label_colors[l, 1]
        b[idx] = label_colors[l, 2]
    # And finally we stack the 3 separate channels to form a RGB image.
    rgb = np.stack([r, g, b], axis=2)
    return rgb

def segment(net, image, dev='cuda', resize=640):
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
    """ 
    Now we format the output
    """
    out_formatted = torch.argmax(out.squeeze(), dim=0).detach().cpu().numpy()
    print(out_formatted.shape)
    # rgb = helpers.decode_segmap(unknown)
    return out_formatted, out


class Model(object):
    def __init__(self):
        self.model = get_model()

    # TOD0?: we could also support publishing inbetween datas - raw segmentation for example.
    def _infer(self, images):
        # TOD0?: support batch size > 1
        img = images[0]
        img = self._preprocess(img)
        formatted, raw = segment(self.model, img)

        formatted = self._postprocess(formatted)

        return formatted, raw

    def infer(self, images):
        return [self._infer(images)[0]]  # return formatted

    def _preprocess(self, image):
        image_pil = Image.fromarray((image * 255).astype(np.uint8))
        return image_pil

    def _postprocess(self, image):
        return decode_segmap(image)  # this sort of decoding should be in self.color_map and published separately?

    def get_categories(self):
        return list(self._get_categories().values())

    @staticmethod
    def _get_categories():
        # you can also read the categories.json file here.
        # But since i'm using pretrained network i'm gonna give this hardcoded
        # 6=bus, 7=car, 8=cat, 9=chair, 10=cow
        # 11=dining table, 12=dog, 13=horse, 14=motorbike, 15=person
        # 16=potted plant, 17=sheep, 18=sofa, 19=train, 20=tv/monitor

        return {
            1: 'aeroplane',
            2: 'bicycle',
            3: 'bird',
            4: 'boat',
            5: 'bottle',
            6: 'bus',
            7: 'car',
            8: 'cat',
            9: 'chair',
            10: 'cow',
            11: 'dining table',
            12: 'dog',
            13: 'horse',
            14: 'motorbike',
            15: 'person',
            16: 'potted plant',
            17: 'sheep',
            18: 'sofa',
            19: 'train',
            20: 'tv/monitor',
        }


def show_image(img, axis='off'):
    plt.imshow(img)
    if axis == 'off':
        plt.axis('off')
    plt.show()


def main_example():
    model = Model()
    path = 'images/bird.png'
    img = Image.open(path)
    show_image(img)
    data = np.array(img)
    res = model.infer([data])[0]
    show_image(res)
    print(res)

if __name__ == '__main__':
    main_example()

