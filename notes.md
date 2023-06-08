

# Lecture 7 june: Noise
Two types of outlier detection
- Distribution based
- Distance based

## Chauvenet's criterion
limit above which the deviation of any value from the mean is considered to be improbable


## Mixture Model
?


## Distance-based outlier detection
distant points are considered to be outliers


## Local Outlier Factor
LOF takes into account the local density of a data point's neighborhood to classify whether it's an outlier




# Lecture 8 june: Feature Engineering

## Support
What fraction of all time points does the pattern occur?


## Temporal Pattern Identification Algorithm
Uses support

## Mixed Data
Make categories from the numerical values


## Frequencies
### Fourier transformation:
Add sinewaves together as a regression method
k (nr of sin waves) runs between 0 to window size (because we cannot go smaller than the window size)
lambda+1 is enough wavelength to decompose any signal
for every sine wave assign amplitude