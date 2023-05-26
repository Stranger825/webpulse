# WebPulse

WebPulse is a Python script that allows you to check the validity and status of web targets. It helps you determine if a target URL or IP address is valid, alive, dead, or invalid.

## Features

- Single target check: Check the validity and status of a single web target.
- Multiple targets check: Check the validity and status of multiple web targets stored in a file.
- Supports both HTTP and HTTPS protocols.
- Handles targets with and without specified ports.
- Provides clear output of valid, invalid, alive, and dead targets.

## Prerequisites

- Python 3.x installed on your system.

## Installation

1. Clone the repository:
```shell
git clone <repository-url>
```

2. Navigate to the project directory:
```shell
cd webpulse
```

3. Install the required dependencies:
```shell
pip install -r requirements.txt
```

## Usage

1. Single target check:
```shell
python webpulse.py
```

2. Multiple targets check:
```shell
python webpulse.py
```
## Examples

1. Single target check:
```shell
Choose an option below:
1: For a single target
2: For multiple targets
Enter Your Option: 1
Target address: example.com

==============================ALIVE TARGETS==============================
The below target(s) are alive:
example.com
============================================================================

===============================DEAD TARGETS==============================
There are no dead target(s)
============================================================================

==============================INVALID TARGETS=============================
There are no invalid target(s)
============================================================================

===============================VALID TARGETS==============================
The below target(s) are valid:
example.com
============================================================================

```
2. Multiple targets check:
```shell
Choose an option below:
1: For a single target
2: For multiple targets
Enter Your Option: 2
Provide the exact file name: targets.txt

=================================ALIVE TARGETS=================================
The below target(s) are alive:
example1.com
example2.com
example3.com
================================================================================

=================================DEAD TARGETS==================================
There are no dead target(s)
================================================================================

================================INVALID TARGETS================================
There are no invalid target(s)
================================================================================

=================================VALID TARGETS==================================
The below target(s) are valid:
example1.com
example2.com
example3.com
================================================================================

```
## Contributing

Contributions are welcome! If you have any suggestions, improvements, or bug fixes, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/Stranger825/webpulse/blob/main/LICENSE) file for more details.

## Acknowledgments

This script was inspired by the need to quickly check the validity and status of web targets for various purposes.
