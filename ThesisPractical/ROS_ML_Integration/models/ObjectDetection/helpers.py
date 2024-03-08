import numpy as np
# from torch import transforms as torchT
import matplotlib.pyplot as plt
import torchvision.transforms.functional as F


def transform(transform_mean=[0.485, 0.456, 0.406], transform_std=[0.229, 0.224, 0.225], resize=640, center_crop=False):
    if center_crop:
        transform = torchT.Compose([
            torchT.Resize(resize),  # Resizes the image to size 256 x 256
            torchT.CenterCrop(center_crop),  # Center Crops the image to have a resulting size of 224 x 224
            torchT.ToTensor(),  # Converts the image to type torch.Tensor and have values between [0, 1]
            torchT.Normalize(mean=transform_mean, std=transform_std)
            # Normalizes the image (in Tensor type) with the given mean and standard deviation
        ]
        )
    else:
        transform = torchT.Compose([
            torchT.Resize(resize),
            torchT.ToTensor(),
            torchT.Normalize(mean=transform_mean, std=transform_std)
            ]
        )
    return transform


# We will use the following function to convert this 2D image to an RGB image
# where each label is mapped to its corresponding color.
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


def show(imgs):
    if not isinstance(imgs, list):
        imgs = [imgs]
    fig, axs = plt.subplots(ncols=len(imgs), squeeze=False)
    for i, img in enumerate(imgs):
        img = img.detach()
        img = F.to_pil_image(img)
        axs[0, i].imshow(np.asarray(img))
        axs[0, i].set(xticklabels=[], yticklabels=[], xticks=[], yticks=[])
