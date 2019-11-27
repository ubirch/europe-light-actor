## Prerequisites
* A Pycom Development Board
* A Pycom Expansion Board or Shield
* Wifi Access to the Internet
* An account at [Ubirch Web UI](https://console.demo.ubirch.com)

## Prepare Local Environment
1. Download and install Atom Editor ([download](https://atom.io/))
    * Mac: download and click on atom-mac.zip
    * Windows: download and run setup exe
    * Linux: download .deb file and run
      ```bash
      sudo dpkg -i atom-amd64.deb
      sudo apt install -f
      ```
      > for more information visit https://flight-manual.atom.io/getting-started/sections/installing-atom/
1. Start Atom Editor
1. Click on *Install a Package* in the menu on the right
     * Enter `pymakr` in the search field
     * Install pymakr package
1. Connect Pycom Device via USB
    * watch pymakr console window in Atom to see if it worked (should show up automatically on the bottom of the Atom window)
1. CLOSE Atom Editor or DISCONNECT the Pycom Device

## Flash Pycom Devices
1. Download Pycom Upgrader ([download](https://pycom.io/downloads/))
1. Download UBIRCH Pycom Firmware ([download](https://github.com/ubirch/example-micropython/releases/tag/pybytes-ed25519))
    * select the correct firmware for your Pycom device (WiPy, Lopy4, GPy, ...)
1. Run Pycom Upgrader and Flash Firmware
    * On the third screen named `COMMUNICATION`select the right serial port / COM port and check the `flash from local file` checkbox
    * select file downloaded in step 2 and continue the process
    * wait until flash process finished successfully

## Configure Pycom Device
1. Re-start Atom Editor or re-connect device
1. Download example firmware code
    * Click menu `View >> Toggle Command Palette`
    * Enter `git clone` and press return
    * Paste `https://github.com/ubirch/example-micropython` to the *Clone from* field and clone it
    * A new project with the project tree at the right of Atom should open automatically

1. Press the `UPLOAD` button just above the pymakr console window in Atom
1. Wait for all files to upload. The code will start running on your device and you will see a `** UUID : XXXX` output
1. copy the **UUID**

## Register Device in Ubirch Web UI
1. Go to https://console.demo.ubirch.com and register your device:
    * Once logged in, go to **Things** (in the menu on the left) and click on **ADD NEW DEVICE**
    * paste the the **UUID** copied in the last step of the previous chapter to the **hwDeviceId** field
    * click **create**
1. Next, click on your device and copy the apiConfig
1. Create a file `config.json` in the `src` directory of the project tree and paste the apiConfig into it.
1. Add configuration for WIFI connection and the expansion board you are using.

   It should then look like this:
    ```json
    {
      "connection": "<'wifi' or 'nbiot'>",
      "networks": {
        "<WIFI SSID>": "<WIFI PASSWORD>"
      },
      "apn": "<APN for NB IoT connection",
      "type": "<BOARD TYPE>",
      "password": "<password for ubirch auth and data service>",
      "keyService": "<URL of key registration service>",
      "niomon": "<URL of authentication service>",
      "data": "<URL of data service>"
    }
    ```
    * Replace `<WIFI SSID>` with the name of your wifi network
    * Replace `<WIFI PASSWORD>` with the password to your wifi network
    * Replace `<BOARD TYPE>` with the expansion board type you are using (`pysense` or `pytrack`)
1. Press the `UPLOAD` button again and you're good to go. 

On initial start, the Pycom will generate an ed25519 key pair for the device and register the public key at the Ubirch
key service. After that, it will frequently measure the following data...
* pysense:
    ```json
            {
                "AccPitch": "<accelerator Pitch in [deg]>",
                "AccRoll": "<accelerator Roll in [deg]>",
                "AccX": "<acceleration on x-axis in [G]>",
                "AccY": "<acceleration on y-axis in [G]>",
                "AccZ": "<acceleration on z-axis in [G]>",
                "H": "<relative humidity in [%RH]>",
                "L_blue": "<ambient light levels (violet-blue wavelength) in [lux]>",
                "L_red": "<ambient light levels (red wavelength) in [lux]>",
                "P": "<atmospheric pressure in [Pa]>",
                "T": "<external temperature in [°C]>",
                "V": "<supply voltage in [V]>",
            }
    ```
* pytrack:
    ```json
            {
                "AccPitch": "<accelerator Pitch in [deg]>",
                "AccRoll": "<accelerator Roll in [deg]>",
                "AccX": "<acceleration on x-axis in [G]>",
                "AccY": "<acceleration on y-axis in [G]>",
                "AccZ": "<acceleration on z-axis in [G]>",
                "GPS_lat": "<longitude in [deg]>",
                "GPS_long": "<latitude in [deg]>",
                "V": "<supply voltage in [V]>",
            }
    ```
...and send it to the Ubirch data service. Further, it packs the sha512 hash of the data into a chained UPP (Ubirch Protocol Package)
which is the certificate of the data's authenticity, and sends it to the Ubirch public blockchain based authentication and timestamping service.

## Visualize the data
1. Go to https://grafana.dev.ubirch.com/?orgId=1
1. Login with your Ubirch Web UI account
1. Create a new dashboard and go to `Add Query`
1. Select `Elasticsearch` in the drop-down menu 
1. Configure your query and make sure your device is still running
1. Enjoy the data coming in from your device

## (Optional - for experts) Check Blockchain Anchoring [DRAFT]
1. While the Pycom is connected and running, and Atom is open, check the pymakr console in Atom and wait for a hash of 
a measurement certificate to appear, e.g.:
    ```
    ** sending measurement certificate ...
    hash: nU3Q1JbJ/q/U0nxbremiIbHtKwaHSD9N9qPHeSr0sXTh3ZaVLyTioZZ3wfiQL0gFONIpGQGKgcr0RyLj4gGO1w==
    ```
    Copy the hash.

1. Send a POST request to the UBIRCH verification service, e.g. by using **curl** (or any other tool to send POST requests):
    ```
    curl -s -X POST -H "accept: application/json" -H "Content-Type: text/plain" -d "$HASH" "$URL"
    ```
    * Replace `$HASH` with the hash copied in step 1
    * Replace `$URL` with
        * https://verify.dev.ubirch.com/api/verify or
        * https://verify.demo.ubirch.com/api/verify or
        * https://verify.prod.ubirch.com/api/verify
    
      depending on the environment you are using

1. The response will list all blockchain anchors containing this measurement certificate. The `txid` (Blockchain 
Transaction ID) of each anchors entry can be used to lookup the entry in the according blockchain explorer (consider 
the `blockchain` and `network_type` attribute to find the right explorer)
