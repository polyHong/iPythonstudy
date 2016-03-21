from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

# Load the images.
orig_img = Image.open("data/lena512.png")
corr_img = Image.open("data/lena512_corrupted.png")

# Convert to arrays.
Uorig = np.array(orig_img)
Ucorr = np.array(corr_img)
rows,cols = Uorig.shape

# Known is 1 if the pixel is known.
# 0 if the pixel was corrupted
Known = np.zeros((rows,cols))
for i in xrange(rows):
	for j in xrange(cols):
		if Uorig[i,j] == Ucorr[i,j]:
			Known[i,j] = 1

# matplotlib inline
fig, ax = plt.subplots(1,2,figsize=(10,5))
ax[0].imshow(orig_img)
ax[0].set_title("Original Image")
ax[0].axis('off');
ax[1].imshow(corr_img)
ax[1].set_title("Corrupted Image")
ax[1].axis('off');
#plt.show()


# Recover the original image using total variation in-painting
from cvxpy import *
U = Variable(rows,cols)
obj = Minimize(tv(U))
constraints = [mul_elemwise(Known,U) == mul_elemwise(Known,Ucorr)]
prob = Problem(obj,constraints)
# Use SCS to solve the problem
prob.solve(verbose=True, solver=SCS)

fig, ax = plt.subplots(1,2,figsize=(10,5))
#Display the in-painted image.
img_rec = Image.fromarray(U.value)
ax[0].imshow(img_rec);
ax[0].set_title("In-Painted Image")
ax[0].axis('off')

img_diff = Image.fromarray(10*np.abs(Uorig-U.primal_value))
ax[1].imshow(img_diff)
ax[1].set_title("Difference Image")
ax[1].axis('off')
plt.show()











