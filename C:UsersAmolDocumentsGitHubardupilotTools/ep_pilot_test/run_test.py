import os
import sys
from datetime import datetime

from tests.COM_USB_001 import run_test as run_usb_test


class Tee:
    def __init__(self, *streams):
        self.streams = streams

    def write(self, data):
        for stream in self.streams:
            stream.write(data)
            stream.flush()

    def flush(self):
        for stream in self.streams:
            stream.flush()


def start_log(test_id):
    os.makedirs("results", exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = os.path.join(
        "results",
        f"{test_id}_{timestamp}.log"
    )

    log_handle = open(log_file, "w", encoding="utf-8")

    sys.stdout = Tee(sys.__stdout__, log_handle)
    sys.stderr = Tee(sys.__stderr__, log_handle)

    return log_file, log_handle


def main():
    print("=" * 60)
    print("         EP-PILOT ENGINEERING TEST UTILITY")
    print("=" * 60)
    print()
    print("Available tests:")
    print()
    print("  1 - USB / MAVLink Communication")
    print("  Q - Exit")
    print()

    choice = input("Select test: ").strip().upper()

    if choice == "Q":
        print("Exiting.")
        return

    if choice == "1":
        test_id = "COM_USB_001"

        log_file, log_handle = start_log(test_id)

        print()
        print(f"[INFO] Log file : {log_file}")
        print(f"[INFO] Date/Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()

        try:
            result = run_usb_test()

            print()
            print("=" * 60)

            if result:
                print("FINAL RESULT : PASS")
            else:
                print("FINAL RESULT : FAIL")

            print("=" * 60)

        finally:
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__
            log_handle.close()

        print()
        print(f"Test log saved to:")
        print(log_file)

        sys.exit(0 if result else 1)

    print("[FAIL] Invalid selection.")
    sys.exit(1)


if __name__ == "__main__":
    main()