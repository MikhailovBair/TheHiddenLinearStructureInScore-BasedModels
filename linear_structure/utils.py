import torch
from torchvision.datasets import CIFAR10
import torchvision.transforms as transforms

from tensordict import TensorDict

def load_dataset(name):
    transform = transforms.Compose([transforms.ToTensor(),
        transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])])

    if name == "CIFAR10":
        dataset = CIFAR10(root='./data', train=True, download=True, transform=transform)
    else:
        raise ValueError(f"No {name}")

    return dataset

def isotropic_score(dataset):
    ims = []
    for im, label in dataset:
        ims.append(im.flatten())
    X = torch.stack(ims)
    mu = torch.mean(X, dim=0)
    return {"mu": mu}

def gaussian_score(dataset):
    ims = []
    for im, label in dataset:
        ims.append(im.flatten())
    X = torch.stack(ims)
    mu = torch.mean(X, dim=0)
    Sigma = torch.cov(X.T)

    U, lambdas, _ = torch.svd(Sigma)
    return {"mu": mu, "U": U, "lambdas": lambdas}

def save_parameters(parameters, filename):
    for name, parameter in parameters.items(): 
        torch.save(parameter, name + ".pt")

