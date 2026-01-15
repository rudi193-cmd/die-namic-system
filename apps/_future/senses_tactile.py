#!/usr/bin/env python3
"""
Senses Tactile — The Nervous System (Hardware)

PHASE 3 ARTIFACT: Servo/sensor driver for Riggs.
STATUS: PARKED — No Arduino connected yet.

AUTHOR: Consus (generated)
DEPENDENCIES: pip install pyfirmata

GOVERNANCE: Human must physically connect hardware.
AI cannot initiate hardware control without human presence.
"""

from typing import Optional

try:
    from pyfirmata import Arduino, util
    PYFIRMATA_AVAILABLE = True
except ImportError:
    PYFIRMATA_AVAILABLE = False
    print("[WARN] pyfirmata not installed. Running in simulation mode.")


class NervousSystem:
    """
    Hardware interface for servo/sensor control.

    SAFE: Operations are logged. Hardware errors fail gracefully.
    Simulation mode when no Arduino connected.
    """

    def __init__(self, port: str = 'COM3'):
        self.port = port
        self.board = None
        self.simulation_mode = True

        if not PYFIRMATA_AVAILABLE:
            print(f"[SIM] NervousSystem initialized in simulation mode (pyfirmata not installed)")
            return

        print(f"[*] Connecting to Nerve Center (Arduino) on {port}...")
        try:
            self.board = Arduino(port)
            # Start the iterator to read data without blocking
            self.it = util.Iterator(self.board)
            self.it.start()
            self.simulation_mode = False
            print("[SUCCESS] Nerve Center Active.")
        except Exception as e:
            print(f"[!] Could not find Arduino on {port}. Running in simulation mode.")
            print(f"    Error: {e}")
            self.board = None

    def move_finger(self, pin: int, angle: int) -> bool:
        """
        Move a servo attached to a specific pin.

        Args:
            pin: Digital pin number (e.g., 9)
            angle: Target angle (0-180)

        Returns:
            True if command sent, False if simulated
        """
        # Clamp angle to safe range
        angle = max(0, min(180, angle))

        if self.board and not self.simulation_mode:
            try:
                # Setup pin as Servo (Mode 4 in Firmata)
                self.board.digital[pin].mode = 4
                self.board.digital[pin].write(angle)
                print(f"    -> Servo {pin} moved to {angle}°")
                return True
            except Exception as e:
                print(f"    [!] Servo Failure: {e}")
                return False
        else:
            print(f"    [SIM] Servo {pin} would move to {angle}° (hardware disconnected)")
            return False

    def read_sensor(self, pin: int) -> Optional[float]:
        """
        Read an analog sensor value.

        Args:
            pin: Analog pin number (e.g., 0 for A0)

        Returns:
            Value between 0.0 and 1.0, or None on error
        """
        if self.board and not self.simulation_mode:
            try:
                val = self.board.analog[pin].read()
                return val
            except Exception as e:
                print(f"    [!] Sensor Read Failure: {e}")
                return None
        else:
            print(f"    [SIM] Sensor A{pin} would be read (hardware disconnected)")
            return 0.5  # Simulated middle value

    def disconnect(self):
        """Safely disconnect from Arduino."""
        if self.board:
            try:
                self.board.exit()
                print("[*] Nerve Center disconnected.")
            except:
                pass
        self.board = None
        self.simulation_mode = True


# === TEST BLOCK ===
if __name__ == "__main__":
    print("Nervous System Test")
    print("=" * 40)

    # Try to connect (will fail gracefully if no Arduino)
    nerves = NervousSystem(port='COM3')

    print(f"\nSimulation mode: {nerves.simulation_mode}")

    # Test servo
    print("\nTesting servo on pin 9:")
    nerves.move_finger(9, 90)

    # Test sensor
    print("\nTesting sensor on A0:")
    value = nerves.read_sensor(0)
    print(f"    Value: {value}")

    # Cleanup
    nerves.disconnect()
    print("\nTest complete.")
