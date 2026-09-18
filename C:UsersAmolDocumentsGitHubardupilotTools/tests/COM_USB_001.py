from serial.tools import list_ports
from pymavlink import mavutil


def run_test():
    print("=" * 60)
    print("TEST ID : COM-USB-001")
    print("TEST    : USB / MAVLink / VBUS Detection")
    print("=" * 60)
    print()

    print("[INFO] Scanning Windows serial ports...")
    ports = list(list_ports.comports())

    if not ports:
        print("[FAIL] No serial ports detected.")
        return False

    print()
    print("[INFO] Serial ports found:")

    for i, port in enumerate(ports, start=1):
        print(f"       {i}: {port.device} - {port.description}")

    print()
    selection = input("Select COM port number: ").strip()

    try:
        selected_index = int(selection) - 1
        if selected_index < 0 or selected_index >= len(ports):
            print("[FAIL] Invalid COM port selection.")
            return False

        port_name = ports[selected_index].device

    except ValueError:
        print("[FAIL] Please enter the port number shown in the list.")
        return False

    print()
    print(f"[INFO] Opening {port_name}...")

    try:
        master = mavutil.mavlink_connection(
            port_name,
            baud=115200,
            autoreconnect=True
        )
    except Exception as exc:
        print(f"[FAIL] Could not open {port_name}")
        print(f"       Reason: {exc}")
        return False

    print("[PASS] Serial port opened.")

    print()
    print("[INFO] Waiting for MAVLink HEARTBEAT...")

    try:
        heartbeat = master.wait_heartbeat(timeout=10)
    except Exception as exc:
        print("[FAIL] Error while waiting for HEARTBEAT.")
        print(f"       Reason: {exc}")
        return False

    if heartbeat is None:
        print("[FAIL] No MAVLink HEARTBEAT received within 10 seconds.")
        return False

        print()
    print("[INFO] Requesting POWER_STATUS from flight controller...")

    master.mav.command_long_send(
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_CMD_REQUEST_MESSAGE,
        0,
        mavutil.mavlink.MAVLINK_MSG_ID_POWER_STATUS,
        0,
        0,
        0,
        0,
        0,
        0
    )

    power_status = master.recv_match(
        type="POWER_STATUS",
        blocking=True,
        timeout=5
    )

    if power_status is None:
        print("[FAIL] POWER_STATUS message not received after request.")
        return False

    print("[PASS] POWER_STATUS received.")
    print(f"       Vcc    : {power_status.Vcc} mV")
    print(f"       Vservo : {power_status.Vservo} mV")
    print(f"       Flags  : 0x{power_status.flags:04X}")

    usb_flag = mavutil.mavlink.MAV_POWER_STATUS_USB_CONNECTED

    print()
    print("[INFO] Checking MAV_POWER_STATUS_USB_CONNECTED...")

    if power_status.flags & usb_flag:
        print("[PASS] USB_CONNECTED flag is SET.")
        print(f"       USB bit mask : 0x{usb_flag:04X}")
    else:
        print("[FAIL] USB_CONNECTED flag is NOT set.")
        print(f"       USB bit mask : 0x{usb_flag:04X}")
        return False