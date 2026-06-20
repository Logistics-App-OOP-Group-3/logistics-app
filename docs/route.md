# 🚚 Route Module Documentation

## 📌 Overview

The **Route** module is responsible for representing and managing delivery routes in the logistics system. A route defines an ordered sequence of locations (stops) between a start and end destination, and can have assigned trucks and packages.

The module is designed using OOP principles with clear separation of concerns:

- **`Route`** — model that stores data and encapsulates route-specific logic
- **`RouteService`** — handles business logic and coordination with other system components
- **`RouteStop`** — represents individual stops within a route

---

## 🧱 Route Structure

A route consists of:

- A unique route ID
- An ordered list of stops (locations with timestamps)
- An optional assigned truck
- A list of assigned package IDs

---

## 📍 RouteStop

### Purpose

Represents a single stop in a route.

### Attributes

| Attribute | Description |
|---|---|
| `location` | Location code (e.g. `SYD`, `MEL`) |
| `expected_time` | Expected arrival or departure time |

### Responsibility

- Stores stop-related data only
- Does not contain business logic

---

## 🚚 Route

### Purpose

Represents a full delivery route between multiple locations.

### Attributes

| Attribute | Type | Description |
|---|---|---|
| `route_id` | `int` | Unique identifier of the route |
| `stops` | `list[RouteStop]` | Ordered list of stops |
| `truck_id` | `int \| None` | Assigned truck |
| `package_ids` | `list[int]` | Assigned packages |

### Key Properties

#### `start_location`
Returns the first location in the route.

#### `end_location`
Returns the last location in the route.

#### `locations`
Returns all locations in order as a list.

### Core Methods

#### `can_deliver_between(start_location, end_location)`

Checks whether a route supports delivery between two locations in the correct order.

**Returns:**
- `True` if start comes before end in route order
- `False` otherwise

#### `add_package(package_id)`

Adds a package to the route if it is not already assigned.

#### `assign_truck(truck_id)`

Assigns a truck to the route.

### Responsibility

The `Route` class:

- Encapsulates route structure and route-level logic
- Validates delivery feasibility within a single route
- Tracks assigned packages and trucks
- **Does NOT** handle searching or system-wide logic

---

## ⚙️ RouteService

### Purpose

The `RouteService` handles all business operations related to routes. It acts as a bridge between the data layer (`AppData`) and the domain model (`Route`).

### Responsibilities

- Create new routes
- Retrieve routes by ID
- Find suitable routes for a given package
- Assign packages to routes
- Assign trucks to routes

### Key Methods

#### `create_route(route_id, stops)`

Creates a new route and stores it in `AppData`.

#### `get_route(route_id)`

Retrieves a route from storage.

> ⚠️ Raises an error if the route does not exist.

#### `find_routes_for_package(package)`

Returns all routes that can deliver a package based on:

- Start location
- End location
- Correct order of stops

#### `assign_package_to_route(package, route_id)`

Assigns a package to a route if:

- The package is not already assigned
- The route supports the delivery path

Updates both:

- **`Route`** (`package_ids`)
- **`Package`** (`route_id`)

#### `assign_truck_to_route(route_id, truck)`

Assigns a truck to a route if both are available.

### Responsibility

`RouteService`:

- Implements business rules
- Coordinates multiple domain objects
- Uses `AppData` as storage only
- Contains no UI or input handling logic

---

## 🧠 Design Summary

The Route module follows a layered architecture:

```
Commands → RouteService → Route + AppData
```

### Responsibilities Split

| Layer | Responsibility |
|---|---|
| **Route** | Route structure + internal logic |
| **RouteService** | Business rules + coordination |
| **AppData** | Data storage |
| **Commands** | User interaction |

### ✔ Design Principles Used

- Encapsulation (`Route` owns its logic)
- Separation of Concerns (Service vs Model vs Commands)
- Single Responsibility Principle
- Clean architecture layering
- Efficient lookup using dictionary-based storage

---

## 🚀 Summary

The Route module provides a clean and scalable way to manage delivery routes. It separates data, logic, and user interaction into distinct layers, ensuring maintainability and ease of extension for future features.
