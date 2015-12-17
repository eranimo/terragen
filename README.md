# Terragen
Computer Graphics Project
Kaelan Cooter

# Features

## Random terrain
Using the diamond-square algorithm to achieve realistic terrain features. Terrain wraps horizontally and vertically such that a representation of a globe can be approximated. Due to the chosen algorithm, images are always square. A sea level is chosen so that around 50-70% of the surface of the planet is covered in water.

## Geographical Features
- Volcanoes and craters

## Rivers and Lakes
- rivers start on the coastlines and head inwards to the continent
- ~5 river algorithms were tried, but only one worked and looked good
- chose an algorithm that looked better instead of one that was more realistic
- rivers produce Moisture
- rivers sometimes form lakes

## Moisture
- Rivers produce a lot of moisture
- random areas of the map produce moisture (called ground water)

## Temperature
- based on latitude and altitude

## Biomes
- based on lookup table of moisture and temperature

## Satellite map
- more realistic biome colors
- blended colors randomly
- altitude slightly changes color to give perception of height
