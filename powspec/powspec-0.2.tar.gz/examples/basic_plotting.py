"""
======================
Basic Usage of powspec
======================

"""
import matplotlib.pyplot as plt
# sphinx_gallery_thumbnail_path = '_static/demo.png'
import astropy.units as u
from astropy.visualization import quantity_support

import numpy as np
from powspec.powspec import power_spectral_density
from powspec.utils.generator import gen_pkfield

quantity_support()

# %%
# Create fake images
# ------------------
#
# Create a list of fake images with different P(k)
#


res = 1 * u.arcmin
alphas = [-1, -2, -3]
images = []
for alpha in alphas:
    images.append(
        gen_pkfield(npix=1024, alpha=alpha, fknee=0.1 / u.arcmin, res=res) * u.MJy
    )

# %%
# Compute P(k)
# ------------
#
# Compute power spectra of each images
#

powspecs = []
for image in images:
    powspec, k = power_spectral_density(image, res=res)
    powspecs.append(powspec)


k_mid = np.mean(u.Quantity([k[1:], k[:-1]]), axis=0)

# %%
# Plots
# -----

fig = plt.figure()
gs = fig.add_gridspec(ncols=2, nrows=len(alphas))
ax_pk = fig.add_subplot(gs[:, 0])

for i, (image, powspec, alpha) in enumerate(zip(images, powspecs, alphas)):

    ax_pk.loglog(k_mid.to(u.arcmin ** -1), powspec.to(u.MJy ** 2 / u.arcmin ** 2), label=alpha)
    ax = fig.add_subplot(gs[i, 1])
    ax.imshow(image.value, origin="lower")

plt.show()
