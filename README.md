# From a polygon to unique rectangles

In order to decompose a polygon into a set of non-overlapping rectangles

1. A polygon is a set of point array in either clockwise or counter-clockwise order
2. The first point in the point array will not be repeated in the last point in the point array


## How to build and run poly2rec (C++ version)

```bash
# c++ version
g++ -std=c++14 poly2rec.cpp -o poly2rec
./poly2rec
```

## How to build and run poly2rec (Python version)

### How to install dependencies

```bash
conda create --name env_ai python=3.8
conda activate env_ai
pip install -r requirements.txt
```

### To remove env_ai

```bash
conda deactivate
conda env remove --name env_ai
conda info --envs # check envs
```

### To run poly2rec (Python version)

```bash
conda activate env_ai
python poly2rec.py
```

## Output

#### INPUT: A POLYGON
![image](/results/polygon.png)

#### OUTPUT: A POLYGON WITH RECTANGLES
![image](/results/polygon_with_rectangles.png)
