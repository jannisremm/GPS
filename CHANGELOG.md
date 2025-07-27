## 0.2.0 (2025-07-28)

### Feat

- **plotting**: :sparkles: force individual view to be square
- **plotting**: :sparkles: Change scale on histogram to log
- **plotting**: :sparkles: Added colourbar showing speed information to individual view
- **plotting**: :sparkles: Added speed / height vs distance chart and adjusted sizing
- **core**: :sparkles: added cumulative distance to parse_gpx_to_dataframe
- **plotting**: :sparkles: Added values to single track view annotations
- **plotting**: :sparkles: Add colourbar for speed values to individual view

### Fix

- **plotting**: :art: adjust structure of annotations
- **plotting**: :bug: Added the rest of the code for speed / height vs distance graph
- **plotting**: :bug: changed m/s to km/h in speed vs time graph, in fitting with earlier changes
- **plotting**: :construction: Manually set combined map extents coordinates to Hamburg
- **plotting**: Changed speed from m/s to km/h
- **core**: :bug: improve speed_list generation, make sure values are not None
- **core**: :bug: Added error handling if random track folder contains no gpx files

### Refactor

- **core**: removed now unneeded assignments
- **core**: :art: improved readablity

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
