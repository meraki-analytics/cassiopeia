import threading

class SingleRateLimiter(object):
    # @param calls_per_epoch # int # Number of calls allowed in each epoch
    # @param seconds_per_epoch # int # Number of seconds per epoch
    def __init__(self, calls_per_epoch, seconds_per_epoch):
        self.seconds_per_epoch = seconds_per_epoch
        self.semaphore = threading.Semaphore(calls_per_epoch)
        self.lock = threading.Lock()
        self.current = 0
        self.limit = calls_per_epoch
        self.resetter = None

    # @param method # function # The function which will be called within the rate limit
    # @param *args # * # The arguments to be passed to the function when it is called
    # @return # * # The result of the function
    def call(self, method=None, *args):
        # Block until a call opens up
        self.semaphore.acquire()

        # Current tracks how many calls are currently inside the method body
        self.lock.acquire()
        self.current += 1
        self.lock.release()

        try:
            if(method):
                return method(*args)
            else:
                return None
        finally:
            # If we don't have an epoch timer running, start one. Also count that we've completed a call.
            self.lock.acquire()
            if(not self.resetter):
                self.resetter = threading.Timer(self.seconds_per_epoch, self._reset)
                self.resetter.daemon = True
                self.resetter.start()

            self.current -= 1
            self.lock.release()

    # Drains the current 
    def _drain(self):
        while self.semaphore.acquire(False):
            pass

    # Resets the rate limit after an epoch has completed
    def _reset(self):
        self.lock.acquire()

        self._drain()
        for _ in range(self.limit - self.current):
            self.semaphore.release()
        self.resetter = None

        self.lock.release()

    # Waits until a call is available
    def wait(self):
        self.semaphore.acquire()
        self.semaphore.release()

    # @param seconds # int # Number of seconds to reset after
    def reset_in(self, seconds):
        if(self.resetter):
            self.resetter.cancel()

        self._drain()
        self.resetter = threading.Timer(seconds, self.reset)
        self.resetter.daemon = True
        self.resetter.start()

class MultiRateLimiter(object):
    # @param limits # list<tuple> # A list of rate limit pairs. A rate limit is (calls_per_epoch, seconds_per_epoch)
    def __init__(self, limits):
        self.limits = []

        for limit in limits:
            self.limits.append(SingleRateLimiter(limit[0], limit[1]))

    # @param method # function # The function which will be called within the rate limit
    # @param *args # * # The arguments to be passed to the function when it is called
    # @return # * # The result of the function
    def call(self, method=None, *args):
        self.wait()

        try:
            if(method):
                return method(*args)
            else:
                return None
        finally:
            for limit in self.limits:
                limit.call()

    # Waits until a call is available
    def wait(self):
        for limit in self.limits:
            limit.wait()

    # @param seconds # int # Number of seconds to reset after
    def reset_in(self, seconds):
        for limit in self.limits:
            limit.reset_in(seconds)