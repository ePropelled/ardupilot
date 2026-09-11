import time
from serial.tools import list_ports
from pymavlink import mavutil


def run_test():
    print("=" * 60)
    print("TEST ID : COM-USB-001")
    print("TEST    : USB / MAVLink Communication")
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
    port_name = input("Enter FC COM port, for example COM7: ").strip()

    if not port_name:
        print("[FAIL] No COM port selected.")
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

    print("[PASS] MAVLink HEARTBEAT received.")
    print(f"       System ID    : {master.target_system}")
    print(f"       Component ID : {master.target_component}")

    print()
    print("[INFO] Reading SERIAL0_PROTOCOL...")

    master.param_fetch_one("SERIAL0_PROTOCOL")

    start_time = time.time()
    param_value = None

    while time.time() - start_time < 5:
        msg = master.recv_match(type="PARAM_VALUE", blocking=True, timeout=1)

        if msg is None:
            continue

        param_id = msg.param_id
        if isinstance(param_id, bytes):
            param_id = param_id.decode("utf-8").rstrip("\x00")

        if param_id == "SERIAL0_PROTOCOL":
            param_value = msg.param_value
            break

    if param_value is None:
        print("[FAIL] SERIAL0_PROTOCOL could not be read.")
        return False

    print("[PASS] SERIAL0_PROTOCOL readable.")
    print(f"       Actual value : {param_value:g}")

    print()
    print("-" * 60)
    print("OVERALL RESULT : PASS")
    print("-" * 60)

    return True