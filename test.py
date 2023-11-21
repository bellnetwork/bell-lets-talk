import subprocess

def unlock_android_phone():
    """
    Function to unlock Android phones via USB.

    This function uses the 'adb' (Android Debug Bridge) command-line tool to unlock the Android phone.
    It executes the 'adb shell input keyevent 82' command, which simulates pressing the unlock button on the phone.

    Returns:
    - bool:
        True if the phone is successfully unlocked, False otherwise.

    Raises:
    - FileNotFoundError:
        If the 'adb' command is not found, it means that the Android SDK platform tools are not installed or not in the system's PATH.
    - subprocess.CalledProcessError:
        If there is an error while executing the 'adb' command.
    """

    try:
        # Execute the 'adb shell input keyevent 82' command to unlock the Android phone
        subprocess.run(['adb', 'shell', 'input', 'keyevent', '82'], check=True)
        return True
    except FileNotFoundError:
        raise FileNotFoundError("The 'adb' command is not found. Make sure Android SDK platform tools are installed.")
    except subprocess.CalledProcessError as e:
        raise subprocess.CalledProcessError(f"Error while executing 'adb' command: {e}")

# Example usage of the unlock_android_phone() function:

try:
    unlocked = unlock_android_phone()
    if unlocked:
        print("Android phone unlocked successfully.")
    else:
        print("Failed to unlock Android phone.")
except FileNotFoundError as e:
    print(f"Error: {e}")
except subprocess.CalledProcessError as e:
    print(f"Error: {e}")
