# nfl_analysis
A repository for my explorations in NFL play-by-play data via nflscrapR

## How to Use
There are three main folders: charting outputs, jupyter notebooks, and python scripts. Charting outputs are images of charts produced in either a jupyter notebook or script.

The jupyter notebook and python scripts folders will contain the same files with the difference being that jupyter notebooks are .ipynb files and scripts are .py.

If you haven't already, checkout my introduction to using [nflscrapR](https://github.com/maksimhorowitz/nflscrapR) data in Python [here](https://gist.github.com/Deryck97/fa4abc0e66b77922634be9f51f9a1052).

## Topics

### Week by Week EPA Analysis
The first analysis is relatively simple, looking at average EPA on runs vs. passes each week of the 2018 season. What we see is that every single week, passing generates a higher average EPA compared to running the ball. Neutral situations were also examined (first and second downs in the first half) and the same relationship held true. In both cases, passing EPA seemed to take a dip in the last few weeks of the season. However, rushing EPA did not see an uptick during the passing dip. 

### Designed Runs vs Scrambles
Looking at EPA on designed run plays versus scrambles. We see that scrambles typically result in a much greater EPA than designed run plays. Designed runs for QBs are much more successful than non-QB runs, but don't typically provide a high EPA. 

!["all_runs"](https://user-images.githubusercontent.com/38873110/62161389-90f9a900-b305-11e9-919d-af8f02f01bf8.PNG)
