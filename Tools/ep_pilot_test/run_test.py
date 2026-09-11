print("=" * 55)
print("       EP-PILOT ENGINEERING TEST UTILITY")
print("=" * 55)
print()
print("[PASS] Python test environment started successfully.")
print()
print("Available tests:")
print()
print("  1 - RC / ExpressLRS")
print("  Q - Exit")
print()

choice = input("Select test: ").strip().upper()

if choice == "1":
    print()
    print("[INFO] RC / ExpressLRS test selected.")
    print("[INFO] Test implementation will run here.")
elif choice == "Q":
    print("Exiting.")
else:
    print("[FAIL] Invalid selection.")