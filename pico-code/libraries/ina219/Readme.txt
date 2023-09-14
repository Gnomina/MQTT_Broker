This library is written for the INA219 module.
The library uses standard micropython features.
The library implements several functions:
Obtaining the current battery voltage in V,
Current in mA, Power in mW, Battery Charge in percentage

Each function has a duplicate with formatted data output.
I need this for use both as a printed string and for working with data.
In order not to clutter the working code with
additional output formatting, I added these functions.

Automatic selection of the type of power source is also configured to display the percentage of charge.
Lipo-1s, Lipo-2s, Lipo-3s.