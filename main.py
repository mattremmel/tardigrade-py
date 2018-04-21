from blupy.btle import Scanner, DefaultDelegate

#
# Central BLE Device
#

class ScanDelegate(DefaultDelegate):
    """
    Delegate called by the 'scan' function when a new device is discovered.
    """
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, device, isNewDevice, isNewData):
        """
        - device is the new device id
        - isNewDevice is a flag that is false if the device has already been discovered.
        - isNewData (i think) is a flag that indicates if the broadcast data for the device is new
        """
        if isNewDevice:
            print "Discovered device", device.addr

        elif isNewData:
            print "Received new data from", device.addr


def scan():
    """
    Starts a loop that scans for new devices and calls the ScanDelegate handler
    on discovery.
    """
    # Scan process
    scanner = Scanner().withDelegate(ScanDelegate())

    scanner.clear() # Clears the current set of discovered devices
    scanner.start() # Starts listening for broadcasts

    # Loop and process connections
    while (True):
        # Waits for broadcasts and calls delegate object when received. Timeout in seconds.
        scanner.process(10)
        scanner.clear()


#
# Peripheral BLE Device
#


def main():
    """
    Process 1. Start process that scans for BTLE devices (filter by project UUID)
        and makes a connect, listens for the data-start-BOM, and starts downloading the data.

        - Scanner object (must be run as root), scans for BLE connections.
            - Takes a ScanDelegate (DefaultDelegate child) class to handle callbacks for
                - def handleDiscovery(self, device, isNewDevice, isNewData)

    Process 2. Start process that advertises the device with the project UUID, and when a connection is made, broadcasts
        all the data available on the device.
    """

    scan()


if __name__ == '__main__':
    main()
