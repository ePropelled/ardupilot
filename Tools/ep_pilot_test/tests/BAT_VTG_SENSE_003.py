from serial.tools import list_ports
from pymavlink import mavutil


def run_test():
    print("=" * 60)
    print("TEST ID : PWR-BAT-001")
    print("TEST    : Battery Voltage Sense")
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
    print("[INFO] Requesting SYS_STATUS from flight controller...")

    master.mav.command_long_send(
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_CMD_REQUEST_MESSAGE,
        0,
        mavutil.mavlink.MAVLINK_MSG_ID_SYS_STATUS,
        0,
        0,
        0,
        0,
        0,
        0
    )

    sys_status = master.recv_match(
        type="SYS_STATUS",
        blocking=True,
        timeout=5
    )

    if sys_status is None:
        print("[FAIL] SYS_STATUS message not received after request.")
        return False

    print("[PASS] SYS_STATUS received.")

    battery_mv = sys_status.voltage_battery

    print(f"       Battery voltage : {battery_mv} mV")

    print()
    user_voltage = input("Enter applied battery voltage [V]: ").strip()

    try:
        expected_v = float(user_voltage)
    except ValueError:
        print("[FAIL] Invalid voltage entered.")
        return False

    expected_mv = int(expected_v * 1000)
    tolerance_mv = 200

    lower_limit = expected_mv - tolerance_mv
    upper_limit = expected_mv + tolerance_mv

    print()
    user_voltage = input("Enter applied battery voltage [V]: ").strip()

    try:
        expected_v = float(user_voltage)
    except ValueError:
        print("[FAIL] Invalid voltage entered.")
        return False

    expected_mv = int(expected_v * 1000)

    tolerance_mv = 200

    lower_limit = expected_mv - tolerance_mv
    upper_limit = expected_mv + tolerance_mv

    print()
    print("[INFO] Checking battery voltage sense...")
    print(f"       Expected      : {expected_mv} mV")
    print(f"       Measured      : {battery_mv} mV")
    print(f"       Acceptable    : {lower_limit} to {upper_limit} mV")

    if lower_limit <= battery_mv <= upper_limit:
        print("[PASS] Battery voltage sense is within acceptable range.")
        return True

    print("[FAIL] Battery voltage sense is outside acceptable range.")
    return False

    if lower_limit <= battery_mv <= upper_limit:
        print("[PASS] Battery voltage sense is within acceptable range.")
        return True

    print("[FAIL] Battery voltage sense is outside acceptable range.")
    return False