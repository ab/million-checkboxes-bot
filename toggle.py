#!/usr/bin/env python3

"""
Toggle checkboxes on One Million Checkboxes
https://onemillioncheckboxes.com
"""

import sys
import time
import optparse

import socketio

URL = 'https://onemillioncheckboxes.com/socket.io/'
VERSION = "0.0.1"

class CheckClient:

    def __init__(self):
        self.sio = self.new_client()

    def new_client(self) -> socketio.SimpleClient:
        sio = socketio.SimpleClient()
        sio.connect(URL, transports=['websocket'])
        return sio

    def toggle_range(start: int, end: int) -> None:
        for i in range(start, end):
            self.toggle(i)
            time.sleep(sleep)
            sys.stdout.write('.')
            sys.stdout.flush()

            if i % 100 == 0:
                print()
                print(i)

    def toggle(self, bit: int) -> None:
        # self.sio.call('toggle_bit', {'index': bit})
        self.sio.emit('toggle_bit', {'index': bit})

    def unflipper(self):
        while True:
            ev = self.sio.receive()

            cmd = ev[0]
            if cmd == "batched_bit_toggles":
                flipA, flipB = ev[1]
                print(f"Received batch with # flips: {len(flipA)}, {len(flipB)}")
                for i in flipA:
                    self.toggle(i)

def callback(*args, **kwargs):
    breakpoint()

def main() -> int:

    p = optparse.OptionParser(usage='%prog [options] START END\n' + __doc__.rstrip(),
                              version='%prog ' + VERSION)
    p.add_option(
        '-i', '--interval', type=float, dest='interval', default=0.05,
        metavar="SLEEP", help='sleep between updates',
    )

    opts, args = p.parse_args()

    sleep = opts.interval

    if len(args) != 2:
        p.print_help()
        return 1

    start, end = args
    start = int(start)
    end = int(end)

    print("Toggling from", start, "to", end)

    cc = CheckClient()

    # ev = sio.receive()

    # cc.toggle_range(start, end)
    cc.unflipper()


    return 0

if __name__ == "__main__":
    sys.exit(main())
