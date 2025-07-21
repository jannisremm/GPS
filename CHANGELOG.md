## 0.1.0 (2025-07-21)

### Feat

- :bug: Check if tracks folder exists, print error message if not
- :children_crossing: Creates combined tracks CSV automatically, and uses it if available
- :sparkles: Added png output and changed naming
- :sparkles: Added a histogram
- :sparkles: Adds annotations to the detail view graph
- :sparkles: Added labels for max height and speed
- :sparkles: added opacity based upon gps error
- :sparkles: added function to chose a random track
- :sparkles: changed main to show all tracks merged together

### Fix

- :bug: made sure all speeds are above zero
- :bug: fixed combined track not being shown

### Refactor

- :art: migrate to Poetry and src layout
- :building_construction: changed graphs to display three at once
- :heavy_plus_sign: updated logic to use pandas
- :recycle: turned plot_track into own function

### Perf

- :heavy_plus_sign: changed gpx logic to use gpxpy
