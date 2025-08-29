'''
This is various info blurbs I read the PyTorch docs and grabbed
Best practice is to comment out any print statements you arent using
'''

import torch
import numpy as np 

data = [[1,2],[3,4]] #initialize tensor from data
x_data = torch.tensor(data)

np_array = np.array(data) #tensors with numpy
x_np = torch.from_numpy(np_array) #converting to torch tensor

x_ones = torch.ones_like(x_data) #gives same attributes as original data
#print(f"Ones Tensor: \n {x_ones} \n")

x_rand = torch.rand_like(x_data, dtype=torch.float) #you can change the data type with dtype and some other stuff
#print(f"Random Tensor: \n {x_rand} \n")

shape = (2,3,) #a tuple of tensor dimensions
rand_tensor = torch.rand(shape)
ones_tensor = torch.ones(shape)
zeros_tensor = torch.zeros(shape)

#print(f"Random Tensor: \n {rand_tensor} \n")
#print(f"Ones Tensor: \n {ones_tensor} \n")
#print(f"Zeros Tensor: \n {zeros_tensor}")

tensor = torch.rand(3,4) #these are the attributes of a tensor

#print(f"Shape of tensor: {tensor.shape}")
#print(f"Datatype of tensor: {tensor.dtype}")
#print(f"Device tensor is stored on: {tensor.device}")

if torch.accelerator.is_available():
    print("you have an accelerator to divert resources to")
    tensor = tensor.to(torch.accelerator.current_accelerator())

print(tensor)
print(f"Device tensor is stored on: {tensor.device}")

