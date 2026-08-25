import numpy as np
import cv2
from time import sleep
import queue


class MHI:
    def __init__(self, cap, tau, delta, xi, t):
        self.tau = tau
        self.delta = delta
        self.xi = xi
        self.t = t
        self.cap = cap
        self.data = queue.Queue()
        ret, frame = cap.read()
        if ret:
            for i in range(t):
                self.data.put(frame)
        self.H = np.zeros(frame.shape)

    def getimag(self):
        ret, frame = cap.read()
        if not ret:
            return ret, frame
        self.data.put(frame)
        old_frame = self.data.get()
        a = cv2.addWeighted(old_frame.astype(float), 1, frame.astype(float), -1, 0)
        D = np.fabs(a)
        Psi = D >= self.xi
        c = self.H - self.delta
        H = np.maximum(0, c)
        H[Psi] = self.tau
        self.H = H
        return ret, H.astype("uint8")


cap = cv2.VideoCapture(0)  #
a = MHI(cap, tau=200, xi=20, delta=10, t=1)
while cap.isOpened():
    _, frame = a.getimag()
    cv2.imshow("out_win", frame)
    sleep(0.04)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()