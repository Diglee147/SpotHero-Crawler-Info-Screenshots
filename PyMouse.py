import pyautogui
import time
print('Set the Mouse Position')
time.sleep(2)
x, y = pyautogui.position()
print ("Mouse Position:")
print ("x = "+str(x)+" y = "+str(y))
