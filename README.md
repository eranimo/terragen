# Terragen
Computer Graphics Project
Kaelan Cooter

# Features
## Random terrain
Using the diamond-square algorithm to achieve realistic terrain features. Terrain wraps horizontally and vertically such that a representation of a globe can be approximated. Due to the chosen algorithm, images are always square. A sea level is chosen so that around 50-70% of the surface of the planet is covered in water.

## Geographical Features
The following features are detected using a flood fill algorithm:
- Continents: large body of land
- Oceans: large body of water
- Islands: small bodies of land under 10% of land pixels
- Inland Sea: surfaces below sea level surrounded by land

The following features are generated:
- Volcanoes: cone shaped mountains randomly placed on the land and water
- Craters: impact basins

Other features (planned):
- Mountain Range: Areas inside land features with rough terrain
- Plains: large areas of lower elevation
- River Valley: Depression created by large rivers

## Rivers and Lakes
Rivers start on mountains and flow towards sea level. As they flow, they increase in speed

A few important points:
- A source of a river is called a Spring
- Flowing water has momentum. Fast moving rivers pick up sediments and deposit them downstream.
- River segments are pixels on the map that make up a river.
- Speed is a property of a river segment from this segment to the next one. Speed is defined as the change in elevation.
- Rivers have depth.
- A river of depth 1 and speed 0 means the terrain is flat. These form lakes.
- When speed increases, more sediment is picked up and the river gets deeper.
- When speed decreases, sediment is deposited and the river gets more shallow.
- Above depth 1, rivers carve out river valleys. A river segment of depth 2 will decrease the elevation of the pixel to the left and right of the segment by 1. A river segment of depth 3 will decrease the elevation to the right and left two pixels out. The end result is a cross section of a river segment form a V shape.
- Sediment is the change in speed between segments + 1.
- River deltas form when rivers have leftover sediments when they reach sea level.
- When a river encounters multiple potential next segments with equal elevation, the river splits.
- When a river segment encounters a segment of another river, it joins that river.

**Example**:

Note: Most rivers would be longer than this.

Sea level = 206
| River Segments | Elevation | # Neighbors | Speed | Sediment | Δ Sediment | Depth | Notes
|:---------------|:---------:|-------------|:-----:|----------|------------|-------|--------------
| Segment 0      | 214       | 1           | 0     | 1        | +1         | 1     | River source
| Segment 1      | 212       | 1           | 2     | 3        | +2         | 3     | Water fall
| Segment 2      | 211       | 1           | 1     | 2        | -1         | 2     |
| Segment 2      | 210       | 1           | 1     | 2        |  0         | 2     |
| Segment 3      | 209       | 1           | 1     | 2        |  0         | 2     | Flat land
| Segment 4      | 209       | 1           | 0     | 1        | -1         | 1     |
| Segment 5      | 208       | 1           | 1     | 2        | +1         | 2     |
| Segment 6      | 207       | 1           | 1     | 2        |  0         | 2     |
| Segment 7      | 206       | 1           | 1     | 2        |  0         | 2     | River end

Effective elevation at sea_level = 204
Leftover sediment at sea_level = 2
River mouth is the pixel in front of Segment 7 in the opposite direction of the river
Leftover sediment will be deposited at the river mouth, raising its elevation


Sea level = 206
| River Segments   | Elevation | # Neighbors | Speed | Sediment | Δ Sediment | Depth | Notes
|:-----------------|:---------:|-------------|:-----:|----------|------------|-------|--------------
| Segment 0        | 216       | 1           | 0     | 1        | +1         |       | River source
| Segment 1        | 215       | 1           | 1     | 3        | +2         |       |
| Segment 2        | 214       | 1           | 1     | 3        |  0         |       |
| Lake segment (3) | 213       | 0           | 0     | 2        | -1         |       | Lake
| Segment 4        | 212       | 1           | 1     | 3        |            |       |
| Segment 5        | 211       | 1           | 1     | 3        |            |       |
| Segment 6        | 210       | 1           | 1     | 3        |            |       |
| Segment 7        | 209       | 1           | 1     | 3        |            |       |
| Segment 8        | 208       | 1           | 1     | 3        |            |       | River end


### Pseudo-code of structures
```
class Map
    int size
    int sea_level
    Function make_rivers(int number)

class Coordinate
    int x
    int y
    int elevation

class Pixel
    Coordinate coords

class River
    RiverSegment source
    Function __init__(RiverSegment source)
class RiverPart
class Lake extends RiverPart
    Coordinate[] pixels
    RiverSegment[] next_segments
    Function fill()

class RiverSegment extends RiverPart
    Coordinate   location
    Boolean      is_lake
    RiverPart[]  prev_segments
    RiverPart[]  next_segments
    Function     find_segment()
    Function     flow()
```

### Psuedo-code of algorithms
**Map.make_rivers(int number_rivers)**
```
river_sources = number_rivers number of random mountain pixels
make new River instance at source
for each river, make initial RiverSegment and run RiverSegment.find_segment()
```
**RiverSegment.find_segment()**
```
next_segments = lowest neighboring pixel below this elevation
if next_segments:
    next_segments = next_segments
if no next_segments:
    # we're in a depression
    next_segments = new Lake()
    call Lake.fill() to find all lake pixels
    # Lake becomes next river segment
if lowest two or more neighbors with the same elevation:
    next_segments = lowest neighbors with same elevation
if any river segment in next_segments is a river already:
    add this segment as a source in that river segment
    add this that segment to next_segments
```
**RiverSegment.flow()**
```
while RiverSegment has next_segments:
    # compute river speed
    segment.speed = change in elevation
    # erode sediments based on speed
    segment.sediments = change in speed + last segment's sediments
    # compute depth
    segment.depth = 1 + change in sediments

    if at segment.elevation is at sea_level and sediments leftover:
        function make_delta:
            compute the river mouth pixel
            deposit leftover sediments recursively until there are no more sediments
            if river mouth elevation > sea_level:
                add new river segment with 0 sediment
                run make_delta again until no more new segments
        run make_delta()
```

erosion = 1
██░██
█████

erosion = 2
█   █
██░██
█████

erosion = 3
█     █
██   ██
███░███
███████
```
# River generation algorithm:
determine randomly placed river sources
for each river source:
    active_segment = river source
    while river can still be extended:
        find lowest neighboring pixels
        if lowest neighbor is >= active_segment:
            perform flood fill algorithm here to fill lake
            active_segment = lowest neighbor of lake
        else if lowest neighbor is < active_segment:
            active_segment = lowest_neighbor
        mark active_segment as a river/lake
# Erosion
loop over each river:
    loop over each river segment:
        last_elevation = last river segment's elevation
        last_speed = last river segment's speed
        this_elevation = this river segment's elevation
        last_erosion = last river segment's erosion
        if river source:
            this_speed = 0
            this_erosion = 1
        else:
            this_speed = last_elevation - this_elevation
            this_erosion = last_erosion + (last_speed - this_speed)
        decrease elevation by this_erosion
        decrease side pixels such that a pixel x pixel away is decreased by (this_erosion - x)
        this will make a V pattern
    if last river_segment is at sea_level:
        deposit eroded sediments at mouth of river to form delta

```


### New river algorithm
Modeling fluid dynamics


At every land pixel, drop a certain amount of water
step:
    for each land pixel:
        move that water to the lowest neighboring pixel
        each unit of water moved = 1 water flow
        if there is no lowest neighboring pixel, keep raising the level to check for a neighboring land pixel until
run 'step' a set number of times (world parameter?)
land pixels with a certain amount of water flow are rivers

analysis:
will make short rivers that flow into larger rivers
erosion can be modeled by the water flow

## Moisture
- Rivers produce a lot of moisture
- coastlines some produce moisture

## Temperature
- based on latitude
