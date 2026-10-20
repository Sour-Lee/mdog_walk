#!/usr/bin/env python3
import serial
import time


class UART_Servo_Controller:
    """
    功能:
        cmd_servo_move
        cmd_mult_servo_pos_read
        cmd_mult_servo_unload
        cmd_get_battery_voltage
        cmd_servo_temperature_read
    """

    def __init__(self, com_port, baudrate=9600):
        """
        參數:
            com_port: string
                Jetson Nano 通常使用 "/dev/ttyTHS1"，USB 可使用 "/dev/ttyACM0"
            baudrate: int
                HTS-20L 使用 9600
        """
        self.ser = serial.Serial()
        self.ser.baudrate = baudrate
        self.ser.port = com_port
        self.ser.open()
        self.ser.flush()
        time.sleep(1.0)

    def __del__(self):
        """關閉 serial port。"""
        if getattr(self, "ser", None) is not None and self.ser.is_open:
            self.ser.close()

    def cmd_servo_move(self, servo_id, angle_position, time_ms):
        """
        控制單一或多顆馬達轉動。
        servo_id: servo 編號列表，例如 [1, 2, 3, 4]
        angle_position: 位置列表，範圍為 0 到 1000
        time_ms: 移動時間，單位為毫秒
        """
        # 封包格式: header、長度、命令、servo 數量、時間及各 servo 位置。
        data = bytearray(b"\x55\x55")
        data.extend([0xFF & (len(servo_id) * 3 + 5), 0x03, 0xFF & len(servo_id)])
        time_ms = 0xFFFF & time_ms
        # 時間值低位元組在前，高位元組在後。
        data.extend([0xFF & time_ms, 0xFF & (time_ms >> 8)])

        for index, servo in enumerate(servo_id):
            position = 0xFFFF & angle_position[index]
            # 每顆 servo 傳送編號、位置低位元組及位置高位元組。
            data.extend([0xFF & servo, 0xFF & position, 0xFF & (position >> 8)])

        self.ser.write(data)

    def cmd_mult_servo_unload(self, servo_id):
        """讓指定的 servo 放鬆、不再輸出扭力。"""
        data = bytearray(b"\x55\x55")
        data.extend([0xFF & (len(servo_id) + 3), 0x14, 0xFF & len(servo_id)])
        data.extend(0xFF & servo for servo in servo_id)
        self.ser.write(data)

    def cmd_mult_servo_pos_read(self, servo_id):
        """讀取多顆 servo 的位置值 (0-1000)。"""
        # 傳送讀取命令及 servo 編號。
        data = bytearray(b"\x55\x55")
        data.extend([0xFF & (len(servo_id) + 3), 0x15, 0xFF & len(servo_id)])
        data.extend(0xFF & servo for servo in servo_id)

        # 清除舊資料，避免把前一個命令的回覆當成本次結果。
        count = self.ser.in_waiting
        if count:
            self.ser.read(count)
        self.ser.write(data)

        # 每個 servo 回傳 3 bytes，另有 5 bytes 封包標頭及狀態資料。
        response_length = len(servo_id) * 3 + 5
        received = bytearray()
        while len(received) < response_length:
            received.extend(self.ser.read(response_length - len(received)))

        positions = list(servo_id)
        # 確認回覆標頭與命令編號正確後，組合各 servo 的 16-bit 位置值。
        if (
            len(received) == response_length
            and received[0:2] == b"\x55\x55"
            and received[3] == 0x15
        ):
            for index in range(len(servo_id)):
                positions[index] = received[6 + 3 * index] | (received[7 + 3 * index] << 8)
        return positions

    def cmd_get_battery_voltage(self):
        """讀取電池電壓，回傳單位為伏特。"""
        # 命令 0x0F 讀取控制器電池電壓。
        self.ser.reset_input_buffer()
        self.ser.write(bytearray(b"\x55\x55\x02\x0f"))

        received = bytearray()
        while len(received) < 6:
            received.extend(self.ser.read(6 - len(received)))

        # 電壓回覆使用毫伏，除以 1000 轉為伏特。
        if len(received) == 6 and received[0:2] == b"\x55\x55" and received[3] == 0x0F:
            return (received[4] | (received[5] << 8)) / 1000.0
        return None