### dsMods
Contains versatile python code modules that help speeding up the completion of data science tasks:

PANDAS
- compute_2D: summarises the relationship between two categorical variables (optionally based on a third variable/dimension). For example when we have a departure (d1) vs destination (d2) column, we can form an interaction matrix that shows the number of trips to and from each location. For some other use cases see example.ipynb
- compute_2D_multiple_d2: similar to compute_2D. The difference is that d2 should be one-hot encoded or consists of columns with 0 and 1 values

VISUALISE
- plot_2D: quickly plots the resulting matrix from the pandas 2D functions
- default_y2: default y2 axis configuration for plotly.go
- map_object_colour: batch colouring function - mapping specific colours to some objects from all objects. The rest is mapped to default colour


