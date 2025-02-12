def golden_check(Golden_Status, SN_Golden_enable, SerialNumber, parts_per_nest=1):
    """
    Checks if the conditions for processing a golden piece are met, allowing for a second part per nest.
    
    Parameters:
    Golden_Status: tuple
        Contains the global status flags and serial numbers for golden pieces.
    SN_Golden_enable: bool
        Indicates if the golden check is enabled.
    SerialNumber: str
        The serial number of the piece being processed.
    parts_per_nest: int, optional
        Number of parts per nest (default is 1, can be 2).
    
    Returns:
    bool
        True if conditions are met, False otherwise.
    """
    # Data preparation and security checks
    (Flag_Golden_OK_Read, Flag_Golden_NOK_Read, Flag_Golden_OK_Read_A, Flag_Golden_NOK_Read_A,
    SN_Golden_OK, SN_Golden_NOK, SN_Golden_OK_A, SN_Golden_NOK_A) = Golden_Status
    if parts_per_nest in (1, 2):
        pass
    else:
        AllowTest = False
        Debug = "Unsupported number of parts per nest!"
        print(Debug)
        return (AllowTest, Debug)
    
    # Pass condition 1: Disabled system
    if not SN_Golden_enable:
        check_disabled = True
    else:
        check_disabled = False
    
    # Pass condition 2: Gold OK and NOK parts already read
    golden_ok_read = Flag_Golden_OK_Read and Flag_Golden_NOK_Read
    
    if parts_per_nest == 2:
        golden_ok_read &= Flag_Golden_OK_Read_A and Flag_Golden_NOK_Read_A
    
    # Pass condition 3: Detected Gold OK or NOK parts serial number
    serial_match = SerialNumber in (SN_Golden_OK, SN_Golden_NOK)
    
    if parts_per_nest == 2:
        serial_match |= SerialNumber in (SN_Golden_OK_A, SN_Golden_NOK_A)
    
    # Checks if any condition is fulfilled to allow a test
    AllowTest = golden_ok_read or serial_match or check_disabled
    Debug = f"Check desactivado: {str(check_disabled)} - SN coincide con gold: {str(serial_match)} - Se han pasado las gold: {str(golden_ok_read)}"
    return (AllowTest, Debug)

# Test script
if __name__ == "__main__":
    SN_Golden_enable = True
    SerialNumber = "12345"
    parts_per_nest = 1  # Cambia a 1 si solo hay una pieza por nido

    Golden_Status = (False, False, False, False, "", "", "", "")

    AllowTest, Debug = golden_check(Golden_Status, SN_Golden_enable, SerialNumber, parts_per_nest)
    
    if AllowTest:
        print("Condiciones Cumplidas")
        print(Debug)
    else:
        print("Condiciones NO cumplidas")
        print(Debug)
