# Imports
import numpy as np
import os
from PIL import Image

# PyTorch Imports
import torch
from torch.utils.data import Dataset


# Data Directories
data_dir = "/ctm-hdd-pool01/tgoncalv/datasets/CBIS_proprocessed"
train_dir = os.path.join(data_dir, "train")
val_dir = os.path.join(data_dir, "val")
test_dir = os.path.join(data_dir, "test")



# Function: Get images and labels from directory files
def map_images_and_labels(dir):
    # Images
    dir_files = os.listdir(dir)
    dir_imgs = [i for i in dir_files if i.split('.')[1]=='png']
    dir_imgs.sort()

    # Labels
    dir_labels_txt = [i.split('.')[0]+'case.txt' for i in dir_imgs]
    

    # Create a Numpy array to append file names and labels
    imgs_labels = np.zeros(shape=(len(dir_imgs), 2), dtype=object)

    # Go through images and labels
    idx = 0
    for image, label in zip(dir_imgs, dir_labels_txt):
        # Debug print
        # print(f"Image file: {image} | Label file: {label}")

        # Append image (Column 0)
        imgs_labels[idx, 0] = image
        
        # Append label (Column 1)
        # Read temp _label
        _label = np.genfromtxt(
            fname=os.path.join(dir, label),
            dtype=str
        )

        # Debug print
        # print(f"_label: {_label}")
        
        # Append to the Numpy Array
        imgs_labels[idx, 1] = _label

        # Debug print
        # print(f"Image file: {imgs_labels[idx, 0]} | Label: {imgs_labels[idx, 1]}")


        # Update index
        idx += 1
    

    # Create labels dictionary to map strings into numbers
    _labels_unique,  nr_classes = np.unique(imgs_labels[:, 1], return_counts=True)

    # Create labels dictionary
    labels_dict = dict()
    
    for idx, _label in enumerate(_labels_unique):
        labels_dict[_label] = idx


    return imgs_labels, labels_dict, nr_classes



# Create a Dataset Class
class TorchDatasetFromNumpyArray(Dataset):
    def __init__(self, base_data_path, transform=None):
        """
        Args:
            base_data_path (string): Data directory.
            pickle_path (string): Path for pickle with annotations.
            transform (callable, optional): Optional transform to be applied
                on a sample.
        """
        
        # Init variables
        imgs_labels, self.labels_dict, self.nr_classes = map_images_and_labels(dir=base_data_path)
        self.images_paths, self.images_labels = imgs_labels[:, 0], imgs_labels[:, 1]
        self.transform = transform


        return 


    # Method: __len__
    def __len__(self):
        return len(self.images_paths)



    # Method: __getitem__
    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()
        

        # Get images
        img_name = self.images_paths[idx]
        image = Image.open(img_name)

        # Get labels
        label = self.labels_dict[self.images_labels[idx]]

        # Apply transformation
        if self.transform:
            image = self.transform(image)


        return image, label



# Test
a, b, c = map_images_and_labels(dir=train_dir)
print(f"{a}")
print(f"{b}")
print(f"{c}")