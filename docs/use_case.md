# INFO

- List elements (filled bullets) under each Use case heading represent required commands
  to execute with parameters (split by a single space).
- `Locations` are accepted by abbreviation or full name, case-insensitively.
- String format for `date_time` parameters is `Sep-12th-06:00h`.

Months: *Jan, Feb, Mar, Apr, May, June, Jul, Aug, Sep, Oct, Nov, Dec*

Locations: *Syd: Sydney, Mel: Melbourne, Adl: Adelaide, Asp: AliceSprings,
Bri: Brisbane, Dar: Darwin, Per: Perth*

# Use case #1

- `createpackage` `start_location` `end_location` `weight`(decimal) `contact_info`(text)`

Creates the **package** and displays a list of **available routes** between the specified locations, if any exist.

- `assignpackage` `package_id` `route_id`

Assigns the package to the specified route. If route_id is 0, the current route assignment remains **unchanged**.

# Use case #2

- `hubsinfo`

Lists all **hubs** with total package **weight** and package **count**, **sorted** by
weight and then count.

- `inspecthub` `city_location`

Lists **packages in the hub grouped by end location** and **sorted** by total
weight and package count, providing suggested calculated data for **route
creation**.

- `createroute` `start_time`(date_time) `stop_location1` `stop_location2` ...`

The route must contain **at least two** stop locations, and all stops must
be **unique**.

**Automatically assigns packages** from each hub at stop locations in visit
order, using FIFO order within each hub.

If a queued package does not fit, **continues** checking the remaining
packages until all are evaluated.

# Use case #3

- `routesinprogress`

Display routes **in progress** with all required information.

# Use case #4

- `unassignedpackages`

Displays all **packages awaiting route assignment**. Each package is listed on a single line in the format: **[id] start_location -> end_location weight**.

# Use case #5

- `packageinfo` `package_id`

Displays the **package information**, including its **status**, **current location**, and **ETA** if it is still in transit.

# Additional
- `advanceroutes`

Completes all routes next stop

- `routeinfo` `route_id`

Information for single route.