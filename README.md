# Calceph Earth-Sun distance

This is a small tool to compute earth sun distance based on CALCEPH package.

This project contains two Python scripts:

* [solarDistanceComputation.py](solarDistanceComputation.py): A script which
  uses the CALCEPH library to compute the earth/sun distance. It takes as an
  input:
    * the ephemeris file(s) to use (examples can be find on https://www.imcce.fr/inpop/)
    * the year of the date for which the solar distance has to be computed
    * the month of the date for which the solar distance has to be computed
    * the day of the date for which the solar distance has to be computed
    * the hour of the date for which the solar distance has to be computed
    * the minute of the date for which the solar distance has to be computed
    * the second of the date for which the solar distance has to be computed

* [cmpToDayMonthMethod.py](cmpToDayMonthMethod.py): A script which plots (for
  a whole year) the solar distance given by the CALCEPH library and
  a elliptical model method. It also gives some statistics on the difference
  between those two measures. It takes as an input:
    * the ephemeris file(s) to use (examples can be find on https://www.imcce.fr/inpop/)
    * the year for which the comparison will be done

## Requirements

To use these scripts, the **calcephpy** package must be previously installed.

``pip install calcephpy``

## Copyright & License

> Copyright (C) 2019 CS Systèmes d'Information (CS SI)
>
> Licensed under the Apache License, Version 2.0 (the "License");
> you may not use this file except in compliance with the License.
> You may obtain a copy of the License at
>
> http://www.apache.org/licenses/LICENSE-2.0
>
> Unless required by applicable law or agreed to in writing, software
> distributed under the License is distributed on an "AS IS" BASIS,
> WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
> See the License for the specific language governing permissions and
> limitations under the License.
