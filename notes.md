

# Lecture 7 june: Noise
Two types of outlier detection
- Distribution based
- Distance based

**## Chauvenet's criterion
**limit above which the deviation of any value from the mean is considered to be improbable


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


# Lecture 9 June: Clustering
## Distance metrics
- Euclidian distance
- Manhattan distance
- Minkowski distance


## Gowers similarity
useful for non-numeric data
- dichotomous
- categorical
- numerical

## Dataset distance
compare datasets instead of individual instances
- expllicit ordering
- temporal ordering

Options:
- summerize values per attribute into single value, e.g. mean
- estimate parameters of distribution per attributes and compare, e.g. normal distribution
- compare the distributions of values for an attirbute , e.g. kolmogorov smirnov test