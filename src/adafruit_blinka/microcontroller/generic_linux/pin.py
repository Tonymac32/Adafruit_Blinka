import gpiod

# Pins dont exist in CPython so...lets make our own!
class Pin:
    IN = 0
    OUT = 1
    LOW = 0
    HIGH = 1
    PULL_NONE = 0
    PULL_UP = 1
    PULL_DOWN = 2
    _CONSUMER = 'adafruit_blinka'

    id = None
    _value = LOW
    _mode = IN

    def __init__(self, pin_number):
        self.id = pin_number
        # FIXME: Presumably this might vary by system:
        self._chip = gpiod.Chip("gpiochip0")
        self._line = self._chip.get_line(int(pin_number))

    def __repr__(self):
        return str(self.id)

    def __eq__(self, other):
        return self.id == other

    def init(self, mode=IN, pull=None):
        if mode != None:
            if mode == self.IN:
                flags = ()
                if pull != None:
                    if pull == self.PULL_UP:
                        flags = (gpiod.LINE_REQ_FLAG_ACTIVE_LOW)
                    elif pull == self.PULL_DOWN:
                        flags = (gpiod.LINE_REQ_FLAG_ACTIVE_HIGH)
                    else:
                        raise RuntimeError("Invalid pull for pin: %s" % self.id)

                self._mode = self.IN
                self._line.request(
                    consumer=self._CONSUMER,
                    type=gpiod.LINE_REQ_DIR_IN,
                    flags=flags
                )

            elif mode == self.OUT:
                if pull != None:
                    raise RuntimeError("Cannot set pull resistor on output")
                self._mode = self.OUT
                self._line.request(consumer=self._CONSUMER, type=gpiod.LINE_REQ_DIR_OUT)

            else:
                raise RuntimeError("Invalid mode for pin: %s" % self.id)

    def value(self, val=None):
        if val != None:
            if val in (self.LOW, self.HIGH):
                self._value = val
                self._line.set_value(val)
            else:
                raise RuntimeError("Invalid value for pin")
        else:
            return self._line.get_value()
