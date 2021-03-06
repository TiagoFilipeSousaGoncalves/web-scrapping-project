# Imports
import numpy as np
import os
import _pickle as cPickle
from PIL import Image

# PyTorch Imports
import torch
from torch.utils.data import Dataset


# Function: Get labels and paths from pickle
def imgs_and_labels_from_pickle(base_data_path, pickle_path):
    # Open pickle file
    with open(pickle_path, "rb") as fp:
        pickle_data = cPickle.load(fp)

    # Split Images and Labels
    images_path = list()
    labels = list()

    # Go through pickle file
    for path, clf in zip(pickle_data[:, 0], pickle_data[:, 1]):
        images_path.append(os.path.join(base_data_path, path+".jpg"))
        labels.append(int(clf))
    

    # Assign variables to class variables
    images_paths = images_path
    images_labels = labels


    return images_paths, images_labels



# Create a Dataset Class
class TorchDatasetFromPickle(Dataset):
    def __init__(self, base_data_path, pickle_path, transform=None):
        """
        Args:
            base_data_path (string): Data directory.
            pickle_path (string): Path for pickle with annotations.
            transform (callable, optional): Optional transform to be applied
                on a sample.
        """
        
        # Init variables
        self.images_paths, self.images_labels = imgs_and_labels_from_pickle(base_data_path, pickle_path)
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
        label = self.images_labels[idx]

        # Apply transformation
        if self.transform:
            image = self.transform(image)


        return image, label