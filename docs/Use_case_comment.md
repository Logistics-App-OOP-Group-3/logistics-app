
# Use case #1
*cities are accepted case insensitively in full name or abbreviation (mELBOURNE, meL)*
- createpackage  start_city  end_city  weight(float)  contact_info

*shows list of available routes for package if any*
- choose route_id to assign it to, or leave it at the hub, automatically left at hub if no available routes

*todo: when accepting userinput loop until valid ,refactor into 2 commands(maybe)*

# Use case #2
- hubsinfo -> list all hubs total packages weight and count (sorted by weight)
- inspecthub -> list all packages in the hub grouped by end_location and sorted by weigth
    *this is setup for createroute*
- createroute city1 city2 city3
    *atleast 2 stops to have a valid route*

*cities are accepted case insensitively in full name or abbreviation*


# Use case #3
- todo

# Use case #4
- unassignedpackages

*short one line per package [id] start_location -> end_location*

# Use case #5
- packageinfo package_id

*displays package info, status, current_location, eta*
