from bluepy.btle import Scanner, DefaultDelegate, Peripheral, BTLEException

# UUID
ServiceUUID =        "4499d2d0-26e8-4678-8b25-8fd84816eb7e"
CharacteristicUUID = "53dc74ee-accb-4f00-a86e-fdf15c8d2fe4"

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
            # print "Discovered device", device.addr

            # Ignore device if not connectable
            if not device.connectable:
                return

            # Create peripheral object for device
            perif = Peripheral()

            print "Connecting to device: %s" % device.addr
            try:
                perif.connect(device.addr)
            except Exception:
                print "Error: Exception while connecting"
                return

            # Discover services
            print "Finding service for device: %s" % device.addr
            services = None
            try:
                services = perif.getServicesByUUID(ServiceUUID)
            except BTLEException:
                perif.disconnect()
                print "Error: Could not find service matching UUID"
                return

            print "Connected to Tardigrade service on device: %s" % device.addr

            # Discover characteristics on services
            characteristics = services.getCharacteristic(forUUID=CharacteristicUUID)

            if len(characteristics) != 1:
                print "Error: %s characteristics returned for UUID" % len(characteristics)

            print "Found DB download characteristic on device: %s" % device.addr
            characteristic = characteristics[0]

            # Subscribe to characteristic
            if not characteristic.supportsRead():
                print "Error: download characteristic doesn't support reading"

            # Wait for start BOM: SOM
            while characteristic.read() != "SOM":
                continue

            # Read data
            data = ""
            while True:
                newData = characteristic.read()

                if newData == "EOM":
                    break

                data = data + newData

            # TODO: Do something with data object
            print data

            # Close connection
            perif.disconnect()
            return

        elif isNewData:
            # print "Received new data from", device.addr
            pass


def scan():
    """
    Starts a loop that scans for new devices and calls the ScanDelegate handler
    on discovery.
    """
    # Scan process
    scanner = Scanner().withDelegate(ScanDelegate())

    scanner.clear()  # Clears the current set of discovered devices
    scanner.start()  # Starts listening for broadcasts

    # Loop and process connections
    while True:
        # Waits for broadcasts and calls delegate object when received. Timeout in seconds.
        print "Scanning for Tardigrade nodes..."
        scanner.process(10)
        scanner.clear()


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
