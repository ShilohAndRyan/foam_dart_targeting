"""
dreamcheekystorm.py implements an interface to the Dream Cheeky O.I.C Storm
USB missile launcher.  It should also work with the Dream Cheeky Thunder, but
since I don't have a Thunder, apply the standard translation from programmer-ese
to plain English: 'It should work' == 'I haven't tested that.'

By default, the device will only be accessable by root.
To make the missile launcher world-writeable, create a file named
'dreamcheeky.rules' in /etc/udev/rules.d containing the following line:
ATTRS{idVendor}=="2123",ATTRS{idProduct}=="1010",MODE="0666"
"""

# Thank you and credit to Nathan Milford who reverse engineered the
# control codes for the Dream Cheeky Thunder/O.I.C. Storm devices for
# his StormLauncher project: https://github.com/nmilford/stormLauncher

# To Do:
# ____ add time-out parameter to all turret moves
# ____ sort out the time delay and interaction on the 'fire' command.

import usb.core as u
import time

class DreamCheekyStorm(object):
    """Implements an interface to the Dream Cheeky O.I.C Storm USB
    missile launcher."""
    _bmRequestType = 0x21 # FIXME: replace with symbolic constant
    _bRequest = 0x09 # FIXME: replace with symbolic constant
    _reqData = {'up':[0x02,0x02,0x00,0x00,0x00,0x00,0x00,0x00],
                'down':[0x02,0x01,0x00,0x00,0x00,0x00,0x00,0x00],
                'left':[0x02,0x04,0x00,0x00,0x00,0x00,0x00,0x00],
                'right':[0x02,0x08,0x00,0x00,0x00,0x00,0x00,0x00],
                'stop':[0x02,0x20,0x00,0x00,0x00,0x00,0x00,0x00],
                'fire':[0x02,0x10,0x00,0x00,0x00,0x00,0x00,0x00]}
    _homeuptime = 1.0
    _homerighttime = 6.0
    def __init__(self):
        self.dev = u.find(idVendor=0x2123, idProduct=0x1010)
        if self.dev is None:
            raise IOError('Dream Cheeky missile launcher not found.')
        if self.dev.is_kernel_driver_active(0):
            self.dev.detach_kernel_driver(0)
        self.dev.set_configuration()
        print 'missile launcher initialized'
    def _writeLauncher(self, data):
        "Write funnel."
        self.dev.ctrl_transfer(self._bmRequestType, self._bRequest, 0, 0, data)
    def home(self):
        "Move turrent to home: limit up, right"
        self.up()
        time.sleep(self._homeuptime)
        self.stop()
        self.right()
        time.sleep(self._homerighttime)
        self.stop()
    def up(self):
        "Turret up."
        self._writeLauncher(self._reqData['up'])
    def down(self):
        "Turret down."
        self._writeLauncher(self._reqData['down'])
    def left(self):
        "Turret left."
        self._writeLauncher(self._reqData['left'])
    def right(self):
        "Turret right."
        self._writeLauncher(self._reqData['right'])
    def stop(self):
        "Stop turret motion."
        self._writeLauncher(self._reqData['stop'])
    def fire(self):
        "Fire missile."
        self._writeLauncher(self._reqData['fire'])

if __name__ == '__main__':
    #import time
    # Test 1: Open the device or throw IOError exception if not present.
    m = DreamCheekyStorm()
    
    # Test 2: Waggle.
    m.right()
    time.sleep(1.0)
    m.stop()
    time.sleep(0.5)
    m.left()
    time.sleep(1.0)
    m.stop()

    # Test 3: Home.
    m.home()

