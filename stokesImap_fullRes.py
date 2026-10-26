import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

from astropy.io import fits
from astropy.wcs import WCS
from matplotlib.colors import LogNorm


# =========================
# Input
# =========================
fits_file = "StokesIfile.fits"

sigma = 3.4e-06  # rms noise

# Log-scale display range
vmin = 5e-07
vmax = 0.007

contour_levels = np.array([3, 10, 18, 100]) * sigma


# =========================
# Read FITS
# =========================
with fits.open(fits_file) as hdul:
    data = np.squeeze(hdul[0].data)
    header = hdul[0].header

wcs = WCS(header).celestial


# =========================
# Mask non-positive pixels for LogNorm
# =========================
data_log = np.ma.masked_less_equal(data, 0)


# =========================
# Plot
# =========================
fig = plt.figure(figsize=(8, 7))
ax = plt.subplot(projection=wcs)

norm = LogNorm(vmin=vmin, vmax=vmax)

cmap = mpl.colormaps.get_cmap("bone").copy()
cmap.set_bad(color="black")

im = ax.imshow(
    data_log,
    origin="lower",
    cmap=cmap,
    norm=norm,
    interpolation="nearest"
)


# =========================
# Contours
# =========================
ax.contour(
    data,
    levels=contour_levels,
    colors="black",
    linewidths=1.2,
    transform=ax.get_transform(wcs)
)


# =========================
# Colorbar
# =========================
cbar = plt.colorbar(im, ax=ax, pad=0.02)

ticks_display = np.array([
    0.001,
    0.003,
    0.01,
    0.03,
    0.1,
    0.3,
    1.0,
    3.0,
    7.0
])

ticks = ticks_display * 1e-3

cbar.set_ticks(ticks)
cbar.set_ticklabels([f"{t:g}" for t in ticks_display])
cbar.ax.yaxis.get_offset_text().set_visible(False)

cbar.set_label(r"$10^{-3}\ \rm Jy\ Beam^{-1}$", fontsize=14)
cbar.ax.tick_params(labelsize=14)


# =========================
# Axes
# =========================
ax.set_xlabel("Right Ascension (J2000)", fontsize=20)
ax.set_ylabel("Declination (J2000)", fontsize=20)
ax.tick_params(axis="both", labelsize=20)

plt.tight_layout()
plt.show()
