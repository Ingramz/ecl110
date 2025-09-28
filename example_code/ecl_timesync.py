#!/usr/bin/env python3
"""
Danfoss ECL Time Syncing Script
Sets the current date and time on the Danfoss ECL controller via Modbus
Tested on ECL110.

Vibe-coded using Claude Sonnet 4 2025-09-28

"""

from pymodbus.client import ModbusSerialClient
from pymodbus.exceptions import ModbusException
from pymodbus.pdu import ExceptionResponse
from datetime import datetime
import time
import sys


SERIAL_PORT = '/dev/ttyUSB0' # USB to RS485 adapter port
MB_ID = 5  # 5 is a danfoss standard id

# Standard comm parameters
BAUD_RATE = 19200
DATA_BITS = 8
PARITY = 'E'  # Even
STOP_BITS = 1

# Danfoss ECL Date/Time register addresses
TIME_REGISTERS = {
    'hour': 64045,      # Hour (0-23)
    'minute': 64046,    # Minute (0-59) 
    'day': 64047,       # Day (1-31)
    'month': 64048,     # Month (1-12)
    'year': 64049,      # Year (e.g., 2025)
}

def write_register(client, address, value, mb_id):
    """Write a single register to the Danfoss ECL"""
    try:
        # Use 0-based addressing (subtract 1 from PNU address)
        modbus_address = address - 1
        response = client.write_register(address=modbus_address, value=value, slave=mb_id)
        
        if isinstance(response, ExceptionResponse):
            return False, f"Unable to write - {response}"
        else:
            return True, "Success"
            
    except Exception as e:
        return False, f"Error: {e}"

def set_ecl_time(client, mb_id, target_datetime=None):
    """Set the Danfoss ECL date and time"""
    if target_datetime is None:
        target_datetime = datetime.now()
    
    print(f"Setting Danfoss ECL time to: {target_datetime.strftime('%Y-%m-%d %H:%M')}")
    print()
    
    # Warning and confirmation
    print("⚠️  You are about to write to Modbus registers on the Danfoss ECL")
    print("This will modify the following registers with the values:")
    
    # Prepare the values to write
    # Note: Danfoss ECL year register only stores 2-digit year (e.g., 25 for 2025)
    time_values = {
        'hour': target_datetime.hour,
        'minute': target_datetime.minute,
        'day': target_datetime.day,
        'month': target_datetime.month,
        'year': target_datetime.year % 100,  # Convert to 2-digit year
    }
    
    # Show what will be written
    for register_name, value in time_values.items():
        address = TIME_REGISTERS[register_name]
        if register_name == 'year':
            print(f"  • Register {address} ({register_name.capitalize()}): {value} (20{value:02d})")
        else:
            print(f"  • Register {address} ({register_name.capitalize()}): {value}")
    
    print()
    
    # Ask for confirmation
    confirm = input("Do you want to proceed with writing to these registers? (yes/no): ").lower().strip()
    if confirm not in ['yes', 'y']:
        print("Operation cancelled by user.")
        return False
    
    print()
    print("Proceeding with register writes...")
    print()
    
    # Write each register
    all_success = True
    for register_name, value in time_values.items():
        address = TIME_REGISTERS[register_name]
        success, message = write_register(client, address, value, mb_id)
        
        if success:
            if register_name == 'year':
                print(f"✓ {register_name.capitalize()}: {value} (20{value:02d}) -> Register {address}")
            else:
                print(f"✓ {register_name.capitalize()}: {value} -> Register {address}")
        else:
            print(f"✗ {register_name.capitalize()}: Failed to write {value} -> Register {address} ({message})")
            all_success = False
        
        # Small delay between writes
        time.sleep(0.1)
    
    return all_success

def read_ecl_time(client, mb_id):
    """Read back the current Danfoss ECL time to verify the setting"""
    try:
        time_values = {}
        
        for register_name, address in TIME_REGISTERS.items():
            modbus_address = address - 1
            response = client.read_holding_registers(address=modbus_address, count=1, slave=mb_id)
            
            if isinstance(response, ExceptionResponse):
                return None
            else:
                time_values[register_name] = response.registers[0]
        
        # Convert 2-digit year to 4-digit year (assuming 20xx)
        full_year = 2000 + time_values['year'] if time_values['year'] < 100 else time_values['year']
        
        # Format as datetime string
        return f"{full_year:04d}-{time_values['month']:02d}-{time_values['day']:02d} {time_values['hour']:02d}:{time_values['minute']:02d}"
        
    except Exception as e:
        return None

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] in ['-h', '--help']:
            print("Usage:")
            print("  python3 set_time.py              # Set to current system time")
            print("  python3 set_time.py --help       # Show this help")
            print()
            print("This script sets the Danfoss ECL controller's internal clock to the current system time.")
            print("⚠️  WARNING: This will write to Modbus registers on the controller!")
            return
    
    print("=== Danfoss ECL Time Setting Tool ===")
    print(f"Current system time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    client = ModbusSerialClient(
        port=SERIAL_PORT,
        baudrate=BAUD_RATE,
        bytesize=DATA_BITS,
        parity=PARITY,
        stopbits=STOP_BITS,
        timeout=2
    )
    
    try:
        print(f"Connecting to Danfoss ECL on {SERIAL_PORT}")
        print(f"Settings: Baudrate={BAUD_RATE}, Parity={PARITY}, ModBus ID={MB_ID}")
        print()
        
        if client.connect():
            print("✓ Connection successful")
            print()
            
            # Small delay after connection
            time.sleep(0.5)
            
            # Read current ECL time
            print("Reading current Danfoss ECL time...")
            current_ecl_time = read_ecl_time(client, MB_ID)
            if current_ecl_time:
                print(f"Current Danfoss ECL time: {current_ecl_time}")
            else:
                print("Unable to read current Danfoss ECL time. Stopping.")
                exit()
            print()
            
            # Set the time
            success = set_ecl_time(client, MB_ID)
            print()
            
            if success:
                print("✓ Time setting completed successfully")
                
                # Read back to verify
                time.sleep(0.5)
                print("Verifying time setting...")
                new_ecl_time = read_ecl_time(client, MB_ID)
                if new_ecl_time:
                    print(f"✓ Danfoss ECL time is now: {new_ecl_time}")
                else:
                    print("⚠ Unable to verify time setting")
            else:
                print("✗ Time setting failed - some registers could not be written")
            
        else:
            print("✗ Modbus connection failed")
            print("Check serial port, wiring, and Danfoss ECL power")
            
    except ModbusException as exc:
        print(f"✗ Modbus Error: {exc}")
        print("Check connections, port settings, and MB ID")
    except Exception as exc:
        print(f"✗ Unexpected error: {exc}")
    finally:
        if client.connected:
            client.close()
            print()
            print("Serial port closed")

if __name__ == "__main__":
    main()
