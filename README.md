# sqlalchemy-challenge
## Background
### Per BootcampSpot assignment:
> Congratulations! You've decided to treat yourself to a long holiday vacation in Honolulu, Hawaii. To help with your trip planning, you decide to do a climate analysis about the area. The following sections outline the steps that you need to take to accomplish this task.

## Assignment Breakdown
### Part 1
In Part 1 of the assignment, I used Python's SQLAlchemy library to `create_engine()` funciton to connect to the hawaii.sqlite database. I then used `automap_base()` to reflect the two tables (station and measurement) into classes, which I stored in variables. The analysis and visualization followed this outline:

1. Find the most recent date in dataset.
2. Using that date, query date and prcp values for the last 12 months of the dataset.
3. Load results into a DataFrame. Sort the values by date.
4. Plot the results using pandas plot method.
5. Use pandas to print summary statistics for prcp data.
6. Create query to find total number of stations in dataset.
7. Design query to find most active stations (based on number of rows). List stations and observation counts in descending order.
8. Determine which is the most active station.
9. Create a query that calculates the lowest, highest and average temperatures for the most active stations.
10. Design a query that collects the last 12 months of temperature observations (TOBS), filter by most active station.
11. Store results into DataFrame, plot a histogram with `bins=12`.
12. Close the session.

### Part 2
In Part 2, I create simple APIs using the Flask library, based on the queries in Part 1.

1. Once Flask has been setup, define homepage route `@app.route("/")`. List all available routes.
2. Next, define `/api/v1.0/precipitation` route. Convert precipitation analysis to a dictionary, using date as key, prcp as value. Filter last 12 months of data. JSONify results.
3. Define `/api/v1.0/stations` route. Return JSON list of all stations.
4. Define `/api/v1.0/tobs` route. Return JSON list of all tobs values for the previous year.
5. Define `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>` dynamic routes:
    - Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
    - For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
    - For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
    - The function I created checks all dates in the dataset to ensure that the user specified date is there.
    - I adopted a different approach from the instructions in the homework. The instructions state to provide a jsonified list of the `tmin`, `tmax` and `tavg` for the specified dates.
    - Instead, I created a dictionary where the key is the `date` and the value is a dictionary containing `tmin`, `tmax` and `tavg` values.
    - Results look like this:
~~~
[
  {
    "2013-02-03": {
      "tobs_avg": 66.71,
      "tobs_max": 73.0,
      "tobs_min": 58.0
    }
  },
~~~

## Repository Breakdown
Included in this repository are the following items:
  - README.md
  - .gitignore
  - SurfsUp directory
    - climate_starter.ipynb (Part 1)
    - app.py (Part 2)
    - Resources directory containing 6 CSV files with the data to populate tables