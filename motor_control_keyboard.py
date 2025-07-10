
import RPi.GPIO as GPIO
import time
import curses

# GPIOピン番号の定義 (BCMモード)
# 左モーター
L_MOTOR_AIN1 = 4
L_MOTOR_AIN2 = 27
# 右モーター
R_MOTOR_BIN1 = 22
R_MOTOR_BIN2 = 23

# GPIOのセットアップ
GPIO.setmode(GPIO.BCM)
GPIO.setup(L_MOTOR_AIN1, GPIO.OUT)
GPIO.setup(L_MOTOR_AIN2, GPIO.OUT)
GPIO.setup(R_MOTOR_BIN1, GPIO.OUT)
GPIO.setup(R_MOTOR_BIN2, GPIO.OUT)

# --- モーター制御関数 ---

def forward():
    """
    両方のモーターを正回転させ、前進する。
    """
    GPIO.output(L_MOTOR_AIN1, GPIO.HIGH)
    GPIO.output(L_MOTOR_AIN2, GPIO.LOW)
    GPIO.output(R_MOTOR_BIN1, GPIO.HIGH)
    GPIO.output(R_MOTOR_BIN2, GPIO.LOW)

def backward():
    """
    両方のモーターを逆回転させ、後退する。
    """
    GPIO.output(L_MOTOR_AIN1, GPIO.LOW)
    GPIO.output(L_MOTOR_AIN2, GPIO.HIGH)
    GPIO.output(R_MOTOR_BIN1, GPIO.LOW)
    GPIO.output(R_MOTOR_BIN2, GPIO.HIGH)

def turn_right():
    """
    左モーターを正回転、右モーターを逆回転させて右旋回する。
    """
    GPIO.output(L_MOTOR_AIN1, GPIO.HIGH)
    GPIO.output(L_MOTOR_AIN2, GPIO.LOW)
    GPIO.output(R_MOTOR_BIN1, GPIO.LOW)
    GPIO.output(R_MOTOR_BIN2, GPIO.HIGH)

def turn_left():
    """
    左モーターを逆回転、右モーターを正回転させて左旋回する。
    """
    GPIO.output(L_MOTOR_AIN1, GPIO.LOW)
    GPIO.output(L_MOTOR_AIN2, GPIO.HIGH)
    GPIO.output(R_MOTOR_BIN1, GPIO.HIGH)
    GPIO.output(R_MOTOR_BIN2, GPIO.LOW)

def brake():
    """
    両方のモーターをブレーキさせ、素早く停止する。
    """
    GPIO.output(L_MOTOR_AIN1, GPIO.HIGH)
    GPIO.output(L_MOTOR_AIN2, GPIO.HIGH)
    GPIO.output(R_MOTOR_BIN1, GPIO.HIGH)
    GPIO.output(R_MOTOR_BIN2, GPIO.HIGH)

def coast():
    """
    モーターを空転させ、自然に停止（惰性停止）させる。
    """
    GPIO.output(L_MOTOR_AIN1, GPIO.LOW)
    GPIO.output(L_MOTOR_AIN2, GPIO.LOW)
    GPIO.output(R_MOTOR_BIN1, GPIO.LOW)
    GPIO.output(R_MOTOR_BIN2, GPIO.LOW)

def main(stdscr):
    # cursesの初期設定
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    stdscr.nodelay(True) # キー入力待ちを非ブロッキングに

    # 操作説明の表示
    stdscr.addstr(0, 0, "キーボードでモーターを操作します。")
    stdscr.addstr(1, 0, "w: 前進, s: 後退, a: 左旋回, d: 右旋回")
    stdscr.addstr(2, 0, "スペース: ブレーキ, q: 終了")
    stdscr.addstr(4, 0, "現在の状態: ")
    
    status = "停止中"
    last_key = -1

    while True:
        # キー入力を取得
        key = stdscr.getch()

        # qが押されたらループを抜ける
        if key == ord('q'):
            break
        
        # キーが押された場合のみ状態を更新
        if key != -1:
            last_key = key

        # キー入力に応じた処理
        if last_key == ord('w'):
            forward()
            status = "前進  "
        elif last_key == ord('s'):
            backward()
            status = "後退  "
        elif last_key == ord('a'):
            turn_left()
            status = "左旋回"
        elif last_key == ord('d'):
            turn_right()
            status = "右旋回"
        elif last_key == ord(' '):
            brake()
            status = "ブレーキ"
        else:
            # キーが押されていないときは惰性停止
            coast()
            status = "停止中"
        
        # 最後のキー入力をリセットして、キーを離したら停止するようにする
        if key == -1:
            last_key = -1

        # 現在の状態を表示
        stdscr.addstr(4, 12, status)
        stdscr.refresh()

        # CPU負荷を少し下げる
        time.sleep(0.05)

# --- メイン処理 ---
if __name__ == '__main__':
    try:
        # cursesをラップして実行
        curses.wrapper(main)
    except KeyboardInterrupt:
        print("プログラムが中断されました。")
    finally:
        # プログラム終了時に必ずGPIO設定をクリーンアップ
        GPIO.cleanup()
        print("GPIOクリーンアップ完了")