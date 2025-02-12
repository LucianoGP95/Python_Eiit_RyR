def golden_check(Golden_Status, SN_Golden_enable, Nest, SerialNumber):
    """
    Checks if the conditions for processing a golden piece are met.
    
    Parameters:
    Golden_Status: object
        Contains the global status flags and serial numbers for golden pieces.
    SN_Golden_enable: bool
        Indicates if the golden check is enabled.
    Nest: int
        The current nest number (1 or 2).
    SerialNumber: str
        The serial number of the piece being processed.
    
    Returns:
    bool
        True if conditions are met, False otherwise.
    """
    # Si la lectura de Golden está deshabilitada
    if not SN_Golden_enable:
        return True
    
    # Determina si para el nido actual ya se han leído las piezas requeridas para ejecución habitual
    if Nest == 1:
        golden_ok_read = Golden_Status.Flag_Golden_OK_Read and Golden_Status.Flag_Golden_NOK_Read
    elif Nest == 2:
        golden_ok_read = Golden_Status.Flag_Golden_OK_Read and Golden_Status.Flag_Golden_NOK_Read
    else:
        return False
    
    # Comprobación del número de serie
    serial_match = SerialNumber in (
        Golden_Status.SN_Golden_OK, Golden_Status.SN_Golden_NOK
    )
    
    return golden_ok_read or serial_match

# Test script
if __name__ == "__main__":
    SN_Golden_enable = True
    Nest = 1
    SerialNumber = "12345"

    class StationGlobals:
        Flag_Golden_OK_Read = False
        Flag_Golden_NOK_Read = False
        SN_Golden_OK = ""
        SN_Golden_NOK = ""
    
    Golden_Status = StationGlobals()

    if golden_check(Golden_Status, SN_Golden_enable, Nest, SerialNumber):
        print("Condiciones Cumplidas")
    else:
        print("Condiciones NO cumplidas")
