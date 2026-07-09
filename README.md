# Logistics App

A command-driven logistics management system for creating routes, assigning packages, managing vehicles, and tracking deliveries across hubs.

## Overview

This application manages the lifecycle of packages and routes across a network of hubs and vehicles. Every action — creating a route, assigning a package, inspecting a hub — is issued as an explicit **command**, executed through a consistent pipeline of validation, service logic, and data persistence.

## Architecture & Design Patterns

The codebase enforces strict separation of concerns through a few key patterns:

- **Command Pattern** — Every user action or business request is encapsulated in its own `Command` class (e.g. `CreateRouteCommand`, `AssignPackageCommand`). New features are added by dropping in a new command, without touching existing logic.
- **Service Layer** — Business logic such as ETA calculations, vehicle distance validation, and package state transitions lives in domain-specific services (`RouteService`, `PackageService`, `VehicleService`, `HubService`), keeping commands thin and focused on orchestration.
- **Dependency Injection** — Services and data stores are injected into commands rather than instantiated internally, enabling full isolation during unit testing.
- **Strict Typing & Validation** — All user input is sanitized and mapped to rigid `Enum` types (`City`, `RouteStatus`, `PackageStatus`) via a centralized validation helper, catching malformed input before it reaches business logic.
- **Centralized Application State** — `core/application_data.py` and `core/data_repository.py` provide a single source of truth for in-memory data, loaded and persisted through `core/file_service.py`.

## Project Structure

```
logistics-app/
├── commands/
│   ├── base/
│   │   └── base_command.py
│   ├── validation_helper.py
│   ├── advance_routes_command.py
│   ├── assign_package_command.py
│   ├── create_package_command.py
│   ├── create_route_command.py
│   ├── hubs_info_command.py
│   ├── inspect_hub_command.py
│   ├── package_info_command.py
│   ├── route_info_command.py
│   ├── routes_in_progress_info_command.py
│   └── unassigned_packages_command.py
├── core/
│   ├── application_data.py
│   ├── command_factory.py
│   ├── data_repository.py
│   ├── engine.py
│   ├── file_service.py
│   └── system_report.py
├── data/
│   └── vehicles.csv
├── docs/
├── enums/
│   ├── city.py
│   ├── package_status.py
│   └── route_status.py
├── models/
│   ├── package/
│   ├── route/
│   ├── hub.py
│   ├── package.py
│   └── vehicle.py
├── services/
│   ├── hub_service.py
│   ├── package_service.py
│   ├── route_service.py
│   └── vehicle_service.py
├── tests/
├── .gitignore
├── input_commands_example.txt
├── main.py
└── README.md
```

## Installation & Setup

1. **Clone the repository**

   ```bash
   git clone git@github.com:Logistics-App-OOP-Group-3/logistics-app.git
   cd logistics-app


2. ## Running the Application

```bash
python main.py
```

Commands can be issued interactively see docs/Use_case_comment.md to see how they fit the usecases

## Testing

The application includes a test suite built on Python's `unittest` framework, using `unittest.mock` for service isolation.

Run all unit tests:

```bash
python -m unittest discover tests
```
don't forget to add the __init__.py file if you are using vscode running the tests

## Adding a New Command

1. Create a new class under `commands/` that extends `base/base_command.py`.
2. Validate input using `commands/validation_helper.py`.
3. Delegate business logic to the relevant service (`RouteService`, `PackageService`, `VehicleService`, `HubService`).
4. Register the command in `core/command_factory.py`.
5. Add corresponding tests under `tests/`.

