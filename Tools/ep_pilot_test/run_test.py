import sys

from tests.COM_USB_001 import run_test as run_usb_test


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

    print()

    if choice == "1":
        result = run_usb_test()
        sys.exit(0 if result else 1)

    if choice == "Q":
        print("Exiting.")
        sys.exit(0)

    print("[FAIL] Invalid selection.")
    sys.exit(1)


if __name__ == "__main__":
    main()