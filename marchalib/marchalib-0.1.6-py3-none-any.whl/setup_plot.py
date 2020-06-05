import os
import numpy as np
import colorcet as cc
import matplotlib
import matplotlib.pyplot as plt

cm_coolwarm = cc.cm["coolwarm"]
cm_coolwarm.set_bad(color='gray')
# cm_coolwarm.set_under(color='gray')
imkw_coolwarm = dict(origin='lower', interpolation='none', cmap=cm_coolwarm)

cm_inferno = plt.get_cmap('inferno')
cm_inferno.set_bad(color='black')
cm_inferno.set_under(color='black')
imkw_inferno = dict(origin='lower', interpolation='none', cmap=cm_inferno)

cm_afmhot = plt.get_cmap('afmhot')
cm_afmhot.set_bad(color='white')
imkw_afmhot = dict(origin='lower', interpolation='none', cmap=cm_afmhot)

cm_viridis = plt.get_cmap('viridis')
cm_viridis.set_bad(color='black')
imkw_viridis = dict(origin='lower', interpolation='none', cmap=cm_viridis)

cm_bone = plt.get_cmap('bone')
cm_bone.set_bad(color='black')
cm_coolwarm.set_under(color='black')
imkw_bone = dict(origin='lower', interpolation='none', cmap=cm_bone)

cm_cubehelix = plt.get_cmap('cubehelix')
cm_cubehelix.set_bad(color='white')
imkw_cubehelix = dict(origin='lower', interpolation='none', cmap=cm_cubehelix)

# cm_planck = matplotlib.colors.ListedColormap(np.loadtxt("Planck_Parchment_RGB.txt")/255.)
# cm_planck.set_bad("white")
# cm_planck.set_under("white")
# imkw_planck = dict(origin='lower', interpolation='none', cmap=cm_planck)


