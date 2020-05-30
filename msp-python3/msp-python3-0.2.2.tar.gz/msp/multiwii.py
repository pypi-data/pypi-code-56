import serial
import struct
import time
import queue
import logging

from threading import Thread, Lock
from threading import current_thread

from msp.message_ids import MessageIDs
from msp.data_structures.channels import Channel
from msp.data_structures.identification import Identification
from msp.data_structures.status import Status
from msp.data_structures.motors import Motor
from msp.data_structures.gps import GPS
from msp.data_structures.comp_gps import CompGPS
from msp.data_structures.imus import IMU
from msp.data_structures.attitude import Attitude
from msp.data_structures.altitude import Altitude
from msp.data_structures.servos import Servo
from msp.data_structures.pid_coefficients import PIDCoefficients





class MultiWii(Thread):
    """Class initialization"""

    __FAILSAFE_VALUE = 2050
    __ANGLE_VALUE = 2050

    def __init__(self, ser_port, print_debug=False):
        super(MultiWii, self).__init__(
            name="Comms_Tx"
        )

        self.__print_debug = print_debug

        # Private Attributes
        self.__lock = Lock()
        self.__running = True
        self.__is_armed = False
        self.__q = queue.Queue()
        self.__timeout = 1.0/60

        self.__rx_thread = Thread(
            target=self.__receive,
            args=[],
            name="Comms_Rx",
            daemon=True
        )

        self.__ser = None
        self.__init_comms(ser_port)
        self.__rc_actual = Channel()
        self.__attitude = Attitude()
        self.__altitude = Altitude()
        self.__imu = IMU()
        self.__gps = GPS()
        self.__comp_gps = CompGPS()

        # Public Attributes
        self.identification = Identification()
        self.status = Status()
        self.servo = Servo()
        self.motor = Motor()
        self.pid_coef = PIDCoefficients()


        self.vtx_config = {
            'device': 0,
            'band': 0,
            'channel': 0,
            'power': 0,
            'pit': 0,
            'unknown': 0
        }

        self.__code_action_map = self.__create_action_map()

    # Private Methods
    def __create_action_map(self):
        code_action_map = {MessageIDs.IDENT: self.identification.parse,
                           MessageIDs.STATUS: self.status.parse,
                           MessageIDs.RAW_IMU: self.__imu.parse,
                           MessageIDs.SERVO: None,
                           MessageIDs.MOTOR: None,
                           MessageIDs.RC: self.__rc_actual.parse,
                           MessageIDs.RAW_GPS: self.__gps.parse,
                           MessageIDs.COMP_GPS: self.__comp_gps.parse,
                           MessageIDs.ATTITUDE: self.__attitude.parse,
                           MessageIDs.ALTITUDE: self.__altitude.parse,
                           MessageIDs.ANALOG: None,
                           MessageIDs.RC_TUNING: None,
                           MessageIDs.PID: None,
                           MessageIDs.BOX: None,
                           MessageIDs.MISC: None,
                           MessageIDs.MOTOR_PINS: None,
                           MessageIDs.BOXNAMES: None,
                           MessageIDs.PIDNAMES: None,
                           MessageIDs.WP: None,
                           MessageIDs.BOXIDS: None,
                           MessageIDs.SERVO_CONF: None}

        return code_action_map

    def __init_comms(self, ser_port):
        """
        Initializes the serial communications port and establishes connection with the Flight Controller.

        :param ser_port: Example: /dev/ttyS0
        :return: None
        """
        self.__ser = serial.Serial()
        self.__ser.port = ser_port
        self.__ser.baudrate = 115200
        self.__ser.bytesize = serial.EIGHTBITS
        self.__ser.parity = serial.PARITY_NONE
        self.__ser.stopbits = serial.STOPBITS_ONE
        self.__ser.timeout = None
        self.__ser.xonxoff = False
        self.__ser.rtscts = False
        self.__ser.dsrdtr = False
        # self.__ser.writeTimeout = 2

        # Time to wait until the board becomes operational
        wakeup = 2
        try:
            self.__ser.open()
            self.__print("Waking up board on " + self.__ser.port + "...")
            for i in range(1, wakeup):
                self.__print(wakeup - i)
                time.sleep(1)
        except Exception as error:
            print("\n\nError opening " + self.__ser.port + " port.\n" + str(error) + "\n\n")

        self.__print("Serial Communication Initialized")

    def __on_thread(self, function, *args, **kwargs):
        self.__q.put((function, args, kwargs))

    def __print(self, data):
        if self.__print_debug:
            print(data)

    def __shutdown(self):
        print(current_thread().name + " - Shutting Down")
        self.__running = False

    def __idle(self):
        # Request Data
        self.__send(MessageIDs.RAW_IMU)
        self.__send(MessageIDs.ALTITUDE)
        self.__send(MessageIDs.ATTITUDE)
        self.__send(MessageIDs.RC)
        self.__send(MessageIDs.RAW_GPS)
        self.__send(MessageIDs.COMP_GPS)
        self.__send(MessageIDs.PID)

        # Set RC values
        data = self.rc_target.to_array()
        self.__send(
            MessageIDs.SET_RAW_RC,
            len(data)*2,
            data
        )

    def __arm(self):
        self.__print("Arming...")
        self.__rc_actual.armed(True)

        data = self.__rc_actual.to_array()
        self.__send(
            MessageIDs.SET_RAW_RC,
            len(data)*2,
            data
        )

        self.__is_armed = True
        self.__print("Armed")

    def __disarm(self):
        self.__print("Disarming...")
        # Roll, Pitch, Throttle, Yaw
        self.__rc_actual.armed(False)

        data = self.__rc_actual.to_array()
        self.__send(
            MessageIDs.SET_RAW_RC,
            len(data)*2,
            data
        )

        self.__is_armed = False
        self.__print("Disarmed")

    def __send(self, code: MessageIDs, data_length=0, data=None):
        """
        Crafts and sends the command packet to be sent over the serial interface to the Flight Controller.

        :param data_length: The number of 'shorts' required to transmit the data.
        :param code: The MessageID of the command to be sent
        :param data: The data (if required) to be transmitted. Can be left blank if the data_length = 0.
        :return: None
        """
        if data is None:
            data = []

        total_data = ['$'.encode('utf-8'), 'M'.encode('utf-8'), '<'.encode('utf-8'), data_length, code] + data
        structure = struct.pack('<2B%dH' % len(data), *total_data[3:len(total_data)])

        checksum = 0
        for i in structure:
            checksum = checksum ^ i
        total_data.append(checksum)

        try:
            b = self.__ser.write(struct.pack('<3c2B%dHB' % len(data), *total_data))
            # self.__ser.flushOutput()
        except Exception as error:
            import traceback
            print("\n\nError in send.")
            print("(" + str(error) + ")")
            traceback.print_exc()

    def __receive(self):
        self.__print("Starting " + current_thread().name)
        while self.__running:
            try:
                while True:
                    header = self.__ser.read().decode('utf-8')
                    if header == '$':
                        header = header + self.__ser.read(2).decode('utf-8')
                        break

                data_length = struct.unpack('<B', self.__ser.read())[0]
                code = struct.unpack('<B', self.__ser.read())[0]
                data = self.__ser.read(data_length)
                # TODO Add logging
                self.__print("Receiving - " + str(code))
                checksum = struct.unpack('<B', self.__ser.read())[0]
                # TODO check Checksum
                # total_data = ['$'.encode('utf-8'), 'M'.encode('utf-8'), '<'.encode('utf-8'), data_length, code] + data
                # structure = struct.pack('<2B%dH' % len(data), *total_data[3:len(total_data)])
                #
                # checksum = 0
                # for i in structure:
                #     checksum = checksum ^ i
                # total_data.append(checksum)


                # print("code: " + str(code))
                # print("data_length: " + str(data_length))
                # print("data: " + str(data))
                # print("checksum: " + str(checksum))

                self.__ser.flushInput()

            except Exception as error:
                import traceback
                print("\n\nError in receive.")
                print("(" + str(error) + ")")
                traceback.print_exc()
                return

            if not data_length > 0:
                return

            temp = struct.unpack('<' + 'h' * int(data_length / 2), data)
            try:
                self.__code_action_map[code](temp)
            except KeyError as err:
                print(err)

    # Public Methods
    def shutdown(self):
        self.__on_thread(self.__shutdown)

    def run(self):

        try:
            self.__rx_thread.start()
            while self.__running:
                try:
                    function, args, kwargs = self.__q.get(timeout=self.__timeout)
                    function(*args, **kwargs)
                except queue.Empty:
                    logging.getLogger("MSP_TX").info("Idling...")
                    self.__idle()

        finally:
            self.__print("Closing Serial Port")
            self.__ser.close()

    def is_armed(self):
        return self.__is_armed

    def arm(self):
        self.__on_thread(self.__arm)

    def disarm(self):
        self.__on_thread(self.__disarm)

    def calibrate_acc(self):
        self.__on_thread(self.__send, [MessageIDs.ACC_CALIBRATION, []])

    # Setters
    def set_target_channels(self, channel):
        self.rc_target = Channel.limit(channel)

    # Getters
    def get_imu(self):
        return self.__imu.get()

    def get_attitude(self):
        return self.__attitude.get()

    def get_altitude(self):
        return self.__altitude.get()

    def get_rc_channels(self):
        return self.__rc_actual.get()

    def get_gps(self):
        return self.__gps.get()

    def get_comp_gps(self):
        return self.__comp_gps.get()

    def get_pid(self):
        return self.pid_coef.get()













