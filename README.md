# PyMetrologie

Flask app for keeping records of measuring instruments. k

- ER diagram: https://github.com/mixall/PyMetrologie/blob/master/PyMetrologie_ER_diagram.jpg

## Functionality

### 1. Meter (gauge)
Each meter (e.g. thermometer 1, thermometer 2) is assigned to a specific device (e.g. thermobox, cooling chamber, refrigerated truck). One device can contain multiple meters. Sometimes it is necessary to lend the meter to another device. In this case, DefDev (home device), which is different from DefDev, is populated.

- App enables:
1) Create records of meters
2) Edit records
3) Deactivate meters 

### 2. Device and location
Every device is located at certain place (location - warehouse 1, warehouse 2, car 1, car 2, ...) and belongs to a specific user.

- App enables:
1) Create records of devices / locations
2) Edit records
4) Deactivate devices / location 

### 3. User
User is a person responsible for the device. User e-mail address is used for e-mail notifications.

- App enables:
1) Create user
2) Edit user
3) Deactivate user


### 4. Calibration
Each meter can have multiple calibrations over time. 
The functionality has not yet been implemented.
