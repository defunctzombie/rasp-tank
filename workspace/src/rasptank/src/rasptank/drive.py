import RPi.GPIO as GPIO

Motor_A_EN    = 4
Motor_B_EN    = 17

Motor_A_Pin1  = 14
Motor_A_Pin2  = 15
Motor_B_Pin1  = 27
Motor_B_Pin2  = 18

class Drive:
    def __init__(self):
        self.pwm_A = None
        self.pwm_B = None
        pass

    def init(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(Motor_A_EN, GPIO.OUT)
        GPIO.setup(Motor_B_EN, GPIO.OUT)
        GPIO.setup(Motor_A_Pin1, GPIO.OUT)
        GPIO.setup(Motor_A_Pin2, GPIO.OUT)
        GPIO.setup(Motor_B_Pin1, GPIO.OUT)
        GPIO.setup(Motor_B_Pin2, GPIO.OUT)

        self.stop()

        self.pwm_A = GPIO.PWM(Motor_A_EN, 1000)
        self.pwm_B = GPIO.PWM(Motor_B_EN, 1000)
        self.pwm_A.start(0)
        self.pwm_B.start(0)

    def cleanup(self):
        GPIO.cleanup()

    def stop(self):
        GPIO.output(Motor_A_Pin1, GPIO.LOW)
        GPIO.output(Motor_A_Pin2, GPIO.LOW)
        GPIO.output(Motor_B_Pin1, GPIO.LOW)
        GPIO.output(Motor_B_Pin2, GPIO.LOW)
        GPIO.output(Motor_A_EN, GPIO.LOW)
        GPIO.output(Motor_B_EN, GPIO.LOW)
        if (self.pwm_A):
            self.pwm_A.ChangeDutyCycle(0)
        if (self.pwm_B):
            self.pwm_B.ChangeDutyCycle(0)

    def motor_left(self, power):
        if power > 0:
            GPIO.output(Motor_B_Pin1, GPIO.HIGH)
            GPIO.output(Motor_B_Pin2, GPIO.LOW)
            self.pwm_B.ChangeDutyCycle(abs(power))
        elif power < 0:
            GPIO.output(Motor_B_Pin1, GPIO.LOW)
            GPIO.output(Motor_B_Pin2, GPIO.HIGH)
            self.pwm_B.ChangeDutyCycle(abs(power))
        pass

    def motor_right(self, power):
        if power > 0:
            GPIO.output(Motor_A_Pin1, GPIO.HIGH)
            GPIO.output(Motor_A_Pin2, GPIO.LOW)
            self.pwm_A.ChangeDutyCycle(abs(power))
        elif power < 0:
            GPIO.output(Motor_A_Pin1, GPIO.LOW)
            GPIO.output(Motor_A_Pin2, GPIO.HIGH)
            self.pwm_A.ChangeDutyCycle(abs(power))