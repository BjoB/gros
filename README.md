<p align="center">
  <img src="doc/gros_logo.png">
</p>

-----------------

# Status

<!--[![BjoB](https://circleci.com/gh/BjoB/gros.svg?style=shield)](https://circleci.com/gh/BjoB/gros)-->
<!--[![PyPI Latest Release](https://img.shields.io/pypi/v/gros.svg)](https://pypi.org/project/gros/)-->
[![BjoB](https://img.shields.io/circleci/build/github/BjoB/gros/master.svg?style=flat-square&logo=circleci)](https://circleci.com/gh/BjoB/gros)
[![Generic badge](https://img.shields.io/badge/powered%20by-astropy-blue.svg)](https://img.shields.io/badge/powered--by-astropy-blue)
[![Generic badge](https://img.shields.io/badge/powered%20by-plotly-blue.svg)](https://img.shields.io/badge/powered--by-plotly-blue)

# Overview

**gros** is a python package to numerically calculate and simulate particle trajectories based on the field equations of general relativity. A user needs to define a certain metric by providing the mass of a central gravitational attractor and the start coordinates and velocity of the test particle.

# Installation

Clone the repository from <https://github.com/BjoB/gros>. After this you can install the package via pip in your choosen environment:

```sh
pip install .
```

# Theoretical background

To simulate particle trajectories around a spherically symmetric body, we use the *Schwarzschild* solution of Einstein's field equations, describing the exterior spacetime for our use case. Starting from the field equations 

<img src="https://render.githubusercontent.com/render/math?math=\large R_{\mu\nu}-\frac{1}{2}g_{\mu\nu}R=\frac{8\pi%20G}{c^4}T_{\mu\nu}">

with a vanishing energy momentum tensor 

<img src="https://render.githubusercontent.com/render/math?math=\large T_{\mu\nu}=0">

the *Schwarzschild* metric can be derived as

<img src="https://render.githubusercontent.com/render/math?math=\large ds^2=g_{\mu\nu}dx^\mu dx^\nu=c^2 (1-\frac{r_s}{r})dt^2-\frac{1}{1-r_s/r}dr^2-r^2d\theta^2-r^2sin^2\theta d\phi^2">

with the *Schwarzschild radius* <img src="https://render.githubusercontent.com/render/math?math=r_s=2GM/c^2"> and the space time coordinates based on spherical coordinates <img src="https://render.githubusercontent.com/render/math?math=(x^0,x^1,x^2,x^3) \mapsto (ct, r,\theta, \phi)">.

The intrinsic space time curvature can be derived from the metric by evaluating the *Christoffel symbols* given with

<img src="https://render.githubusercontent.com/render/math?math=\large \Gamma_{\alpha\nu}^{\beta}=\frac{1}{2}g^{\mu\beta}(\partial_{\alpha}g_{\mu\nu}%2B\partial_{\nu}g_{\mu\alpha}-\partial_\mu g_{\alpha\nu})">

After calculating these coefficients and using the proper time as parameter, the motion of of a particle in the gravitational field can be retrieved by solving the system of differential equations given with the geodesic equations

<img src="https://render.githubusercontent.com/render/math?math=\large \frac{dx^\mu}{d\tau}+\Gamma_{\alpha\beta}^{\mu}\frac{dx^\alpha}{d\tau}\frac{dx^\beta}{d\tau}=0">

# Examples

Some simple simulations can be found in the [examples](https://github.com/BjoB/gros/tree/master/src/gros/examples) directory.

## Particle on Mercury's orbit

This example simulates a particle orbiting the sun with some initial orbital parameters taken from <https://nssdc.gsfc.nasa.gov/planetary/factsheet/>. After calculating the trajectory, an animation will be generated, which can be used to track the particle with a previously choosen step size.

<p align="center">
  <img src="doc/mercury_plot.png">
</p>

## Earth as a black hole

What if earth was a black hole? The according example shows how a particle would act in short distance of 30m. Especially the perihelion precession is visualized as a direct effect of general relativity. Additionally the gravitational time dilation can be tracked along the animation frames with τ as the proper time of the particle. t is the calculated coordinate time, which can be seen as the measured proper time of a hypothetical observer positioned infinitely far away from the gravitational center.

<p align="center">
  <img src="doc/earth_black_hole_animation_zoomed.png">
</p>
