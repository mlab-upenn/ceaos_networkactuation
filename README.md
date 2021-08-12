# What is this?
This is a library that makes writing drivers for network actuation easier. This library is not required, lower level implementations of the same protocol can be used on edge devices without access to python.

# Basic Usage

1. Import this library and your driver library.
    ```python
    from your_driver_lib import mysetpoint, mydo
    from ceaos.networkactuation import NetworkActuation
    ```
2. Register the functions for `setpoint` and `do`, specifying bounds and datatypes to check.
    ```python
    NA = NetworkActuation()
    NA.register_setpoint(mysetpoint, dtype=float, rules=[lambda x: x>1.0, lambda x: x<10.0>])
    NA.register_do(mydo, dtype=bool)
    ```
3. Tell the library to listen
    ```python
    NA.listen(port=26462)  # Pick any port to listen on 
    ```