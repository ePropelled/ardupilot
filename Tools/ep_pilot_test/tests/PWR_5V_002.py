from serial.tools import list_ports
from pymavlink import mavutil


def run_test():
    print("=" * 60)
    print("TEST ID : PWR-5V-001")
    print("TEST    : 5V Rail Monitor")
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

    heartbeat = master.wait_heartbeat(timeout=10)

    if heartbeat is None:
        print("[FAIL] No MAVLink HEARTBEAT received.")
        return False

    print("[PASS] MAVLink HEARTBEAT received.")

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

    board_voltage_mv = power_status.Vcc

    print(f"       Board voltage : {board_voltage_mv} mV")

    expected_mv = 5000
    tolerance_mv = 250

    lower_limit = expected_mv - tolerance_mv
    upper_limit = expected_mv + tolerance_mv

    print()
    print("[INFO] Checking 5V rail...")
    print(f"       Expected      : {expected_mv} mV")
    print(f"       Acceptable    : {lower_limit} to {upper_limit} mV")

    if lower_limit <= board_voltage_mv <= upper_limit:
        print("[PASS] 5V rail is within acceptable range.")
        return True

    print("[FAIL] 5V rail is outside acceptable range.")
    return False