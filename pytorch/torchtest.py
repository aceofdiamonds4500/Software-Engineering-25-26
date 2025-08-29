import torch
x = torch.rand(5,3)
print(x)

print(torch.cuda.is_available()) #"is CUDA available for Nvidia drivers?"

'''if this runs, your environment is running correctly :]'''