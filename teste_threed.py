import threading
import time


class FractionSetter(threading.Thread):
    def __init__(self, stop_count):
        threading.Thread.__init__(self)
        self.stopthread = threading.Event()
        self.stop_count = stop_count
        self.count = 0

    def run(self):
        """while sentence will continue until the stopthread event is set"""
        while not self.stopthread.isSet():

            time.sleep(1)

            self.count += 1

            print self.count

            if self.count >= self.stop_count:
                break
                # self.stop()

    def stop(self):
        self.stopthread.set()
        # self._Thread__stop()


tr = FractionSetter(10)

tr.start()

time.sleep(5)
if tr.is_alive():
    print 'Chama stop'
    tr.stop()

'''array = []
for i in range(1,10):
    array.append(FractionSetter(i))

#print time.gmtime()

#START THE THREADS
for thread in array:
    thread.start()

#DO STUFF WHILE THE THREAD IS RUNNING
running = True
count = 0
while running:
    if count == 15:
        running = False
    print time.gmtime()
    time.sleep(1)
    count +=1

info = []

#STOP THE THREADS
for thread in array:
    #Stopping the thread
    thread.stop()
    info.append([thread.total, thread.count, thread.getName()])

#print time.gmtime()

for elem in info:
    print elem[0], " ",elem[1], " ",elem[2]
'''
