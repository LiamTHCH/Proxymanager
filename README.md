# 3proxy Configuration Management Script

This Python script manages configurations for the 3proxy software, allowing users to manipulate proxy settings, add new proxies, list existing proxies, and generate configuration files.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Functionality](#functionality)
- [Contributing](#contributing)
- [License](#license)

## Introduction

This script facilitates the management of 3proxy configurations. It enables users to parse existing configurations, add new proxy entries, list proxies based on interface or user, remove proxies, and generate configuration files compatible with 3proxy.

## Features

- Parse existing 3proxy configurations from a formatted string.
- Add new proxy entries with type, port, endpoint, and optional interface and users.
- List all proxies on a specified interface.
- List all proxies associated with a specific user.
- Remove a proxy entry by its port number.
- Generate configuration files formatted for 3proxy from parsed data.
- Write configurations to a file for persistence.

## Requirements

- Python 3.x
- 3proxy software installed (if generating 3proxy configurations)


## Functionality

### Parsing Configurations

The `parse_config` function parses a formatted string or file of 3proxy configurations, extracting proxy type, port, endpoint, interface (if specified), and associated users.

### Adding a Proxy

Use the `create_proxy` function to add a new proxy entry. Provide parameters for type, port, endpoint, interface (optional), and users (optional).

### Editing a Proxy

The `edit_proxy` function allows modifying an existing proxy entry identified by its port number. It accepts parameters to update connection type, endpoint, interface, and users associated with the proxy.

### Listing Proxies

- **List Proxies on Interface:** `list_proxies_on_interface(parsed_data, interface)` lists all proxy entries associated with a specific network interface.

- **List Proxies for User:** `list_proxies_for_user(parsed_data, user)` lists all proxy entries associated with a specific user.

### Removing Proxies

- **Remove Proxy Entry:** `remove_proxy_entry(parsed_data, port)` removes a proxy entry identified by its port number.

- **Remove User from Proxy:** `remove_user_from_proxy(parsed_data, user, port)` removes a specific user from a proxy entry identified by its port number.

### Generating Configurations

The `generate_all_configurations` function generates configuration strings for all parsed proxy entries formatted for 3proxy.

### Writing Configurations to File

Use `write_config_to_file(filename, configurations)` to write all generated 3proxy configurations to a file.

### Reading Configurations from File

The `readfile(filename)` function reads content from a specified file, facilitating the input of existing configurations for parsing and manipulation.
