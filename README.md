# HomeScreen +

A one-click, terminal-free **scrcpy** launcher for Fedora Linux that discovers an authorized Android phone over local Wi-Fi. Features a desktop icon, `HomeScreen +` window title, cached-IP fast path, local subnet discovery and an exclusive lock to avoid duplicate launch windows, plus an animated connection splash with pulsing Wi-Fi signal and clear connection/error states.

## Requirements

- Fedora Linux with `scrcpy`, `adb` (`android-tools`), `nmap`, `ip` (`iproute`), and `flock` (`util-linux`), Python 3 with Tkinter (`python3-tkinter`).
- Phone and Fedora PC on a mutually reachable **trusted** local IPv4 network.
- USB debugging previously authorized for the Fedora PC; ADB TCP/IP enabled on the phone, normally port 5555.
- On some Wayland compositors, the taskbar/window icon is determined by compositor app-ID matching; the custom launcher icon is provided but cannot be guaranteed in every window manager.

## Install

```bash
sudo dnf install android-tools nmap scrcpy iproute util-linux python3-tkinter
git clone https://github.com/iliasgws/HomeScreen-Plus.git
cd HomeScreen-Plus
./install.sh
```

Run **HomeScreen +** from your applications list, or `gtk-launch homescreen-plus` if `gtk-launch` is installed.

### Configure your phone

Default matching model is `24129PN74G`. To choose another model, set `HOMESCREEN_MODEL` in your desktop environment, or change the default in the `phone` script. Set `HOMESCREEN_PORT` if ADB uses a different TCP port. The launcher caches its last IP in `${XDG_CACHE_HOME:-~/.cache}/homescreen-plus/phone-ip`; it does **not** hardcode a personal IP.

Test TCP/IP ADB first on a trusted LAN:

```bash
adb devices
adb tcpip 5555
adb connect PHONE_LAN_IP:5555
scrcpy -s PHONE_LAN_IP:5555
```

The splash remains visible for at least **3 seconds** after launch on a successful connection. Adjust the minimum with `HOMESCREEN_SPLASH_MS=5000` (milliseconds) in your launcher environment. This adds a presentation delay, not a network timeout.

## How discovery works

1. Attempts the last successful IP.
2. Checks previously connected ADB TCP/IP devices.
3. Scans directly connected IPv4 subnets for port 5555 (via Nmap), then checks Android's model with `getprop`.
4. Displays an animated phone/Wi-Fi splash during discovery, shows connection status or a short error message, and opens exactly one scrcpy instance with the specified title and no terminal.

The scanning method does not work across the internet, client-isolated public Wi-Fi, or unrelated networks. Only scan networks you own or have permission to scan.

## Security warning

**ADB TCP/IP on port 5555 is sensitive. Do not expose it to the public internet or leave it open on untrusted networks.** Root access and persistent ADB magnify the risk. Avoid router port-forwarding and restrict ADB using Android firewall rules or turn TCP/IP debugging off when not needed. For cross-network use, consider a secure private VPN (e.g., Tailscale) with strict access controls; this launcher only discovers directly connected local IPv4 networks. Persistent Magisk scripts are intentionally **not** installed or enabled by this project.

To disable traditional TCP/IP ADB while USB is connected:

```bash
adb usb
```

If you configured persistent TCP/IP ADB in Magisk, disable that boot script first or it may reactivate the listener.

## License

See [LICENSE](LICENSE).
