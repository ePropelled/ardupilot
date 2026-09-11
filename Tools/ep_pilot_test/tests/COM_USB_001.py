print()
print("[INFO] Waiting for POWER_STATUS...")

power_status = master.recv_match(
    type="POWER_STATUS",
    blocking=True,
    timeout=5
)

if power_status is None:
    print("[FAIL] POWER_STATUS message not received.")
    return False

print("[PASS] POWER_STATUS received.")
print(f"       Vcc   : {power_status.Vcc} mV")
print(f"       Vservo: {power_status.Vservo} mV")
print(f"       Flags : 0x{power_status.flags:04X}")

usb_flag = mavutil.mavlink.MAV_POWER_STATUS_USB_CONNECTED

if power_status.flags & usb_flag:
    print("[PASS] USB_CONNECTED flag is set.")
else:
    print("[FAIL] USB_CONNECTED flag is NOT set.")
    return False