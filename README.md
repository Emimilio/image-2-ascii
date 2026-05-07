# image-2-ascii

This is a small image to ASCII art converter. Traditional ASCII art converters don't have any edge detection used to make out the outline of objects in the images. This code adds an extra edge detection layer to add contrast to objects in images. To accomplish this, a canny filter and a sobel filter are combined to extract the edges and identify the right ascii character to represent the edge based on the gradient found with the sobel filter. The edges are represented by the following characters `-`,`/`,`\`,`|` and the pixels intensities are represented with the following characters ` `, `.`, `i`, `c`, `o`, `P`, `O`, `?`, `@`.

This project was made in collaboration with [Edwin Lemelin](https://github.com/Edwin15571)

## Setup:

### Create a virtual envirment
```
python -m venv .venv
```

### Activation the environment:
- Command for Windows:
 ```
.venv\Scripts\activate
```

- Command for Linux/MacOS:
```
source .venv/bin/activate
```

#### 3) Install all the dependencies needed:
```
pip install -r requirements.txt
```


#### Info: 
Command to deactivate the virtual environment for windows/Linux/MacOS:
```
deactivate
```

## How to use:


## References:

- https://www.youtube.com/watch?v=gg40RWiaHRY

- https://www.youtube.com/watch?v=t8aSqlC_Duo

