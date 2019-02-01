# calceph_earth-sun_distance
Small tool to compute earth sun distance based on CALCEPH package


This project contains two scripts python:
* solarDistanceComputation.py : A script which uses the CALCEPH library to compute the earth/sun distance. It takes as an input :
    * The ephemeris file(s) to use. (Examples can be find on https://www.imcce.fr/inpop/)
    * The year of the date for which the solar distance has to be computed
    * The month of the date for which the solar distance has to be computed
    * The day of the date for which the solar distance has to be computed
    * The hour of the date for which the solar distance has to be computed
    * The minute of the date for which the solar distance has to be computed
    * The second of the date for which the solar distance has to be computed
    
* cmpToDayMonthMethod.py : A script which plots (for a whole year) the solar distance given by the CALCEPH library and a elliptical model method. It also gives some statistics on the difference between those two measures. It takes as an input :
    * The ephemeris file(s) to use. (Examples can be find on https://www.imcce.fr/inpop/)
    * The year for which the comparison will be done

### Installation

To use these scripts the **calcephpy** package must be previously installed.

``pip install calcephpy``