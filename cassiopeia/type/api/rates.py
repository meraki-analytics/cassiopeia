import threading


class SingleRateLimiter(object):
    """
    Handles a single rate limit, ensuring that calls don't exceed it
    """

    def __init__(self, calls_per_epoch, seconds_per_epoch):
        """
        Handles a single rate limit, ensuring that calls don't exceed it
        """
        self.seconds_per_epoch = seconds_per_epoch
        self.semaphore = threading.Semaphore(calls_per_epoch)
        self.lock = threading.Lock()
        self.current = 0
        self.limit = calls_per_epoch
        self.resetter = None
        self._total_calls = 0
        self._successful_calls = 0

    def call(self, method=None, *args):
        """
        Args:
            calls_per_epoch (int): the number of calls allowed in each epoch
            seconds_per_epoch (int): the number of seconds per epoch
        """
        # Block until a call opens up
        self.semaphore.acquire()

        # Current tracks how many calls are currently inside the method body
        with self.lock:
            self.current += 1

        successful_call = True
        try:
            return method(*args) if method else None
        except:
            successful_call = False
            raise
        finally:
            # If we don't have an epoch timer running, start one. Also count that we've completed a call.
            with self.lock:
                if not self.resetter:
                    self.resetter = threading.Timer(self.seconds_per_epoch, self._reset)
                    self.resetter.daemon = True
                    self.resetter.start()

                self.current -= 1
                self._total_calls += 1
                if successful_call:
                    self._successful_calls += 1

    def _drain(self):
        """
        Calls a function when the rate limit allows (first come first serve)

        Args:
            method (function): the function which will be called when the rate limit allows
            *args (any...): the arguments to be passed to the functions when it is called

        Returns:
            any: the result of the function once it has been called
        """
        while self.semaphore.acquire(False):
            pass

    def _reset(self):
        """
        Calls a function when the rate limit allows (first come first serve)

        Args:
            method (function): the function which will be called when the rate limit allows
            *args (any...): the arguments to be passed to the functions when it is called

        Returns:
            any: the result of the function once it has been called
        """
        self.lock.acquire()

        self._drain()
        for _ in range(self.limit - self.current):
            self.semaphore.release()
        self.resetter = None

        self.lock.release()

    def wait(self):
        """
        Calls a function when the rate limit allows (first come first serve)

        Args:
            method (function): the function which will be called when the rate limit allows
            *args (any...): the arguments to be passed to the functions when it is called

        Returns:
            any: the result of the function once it has been called
        """
        self.semaphore.acquire()
        self.semaphore.release()

    def reset_in(self, seconds):
        """
        Calls a function when the rate limit allows (first come first serve)

        Args:
            method (function): the function which will be called when the rate limit allows
            *args (any...): the arguments to be passed to the functions when it is called

        Returns:
            any: the result of the function once it has been called
        """
        with self.lock:

            if self.resetter:
                self.resetter.cancel()

            self._drain()
            self.resetter = threading.Timer(seconds, self._reset)
            self.resetter.daemon = True
            self.resetter.start()

    def _decrease_successful_calls(self):
        with self.lock:
            self._successful_calls -= 1

    @property
    def calls(self):
        """
        Drains all remaining calls
        """
        with self.lock:
            return (self._successful_calls, self._total_calls)


class MultiRateLimiter(object):
    """
    Resets the rate limit
    """

    def __init__(self, *limits):
        """
        Resets the rate limit
        """
        self.limits = []

        for limit in limits:
            self.limits.append(SingleRateLimiter(limit[0], limit[1]))

    def call(self, method=None, *args):  # TODO
        """
        Waits until a call becomes available
        """
        self.wait()

        successful_call = True
        try:
            return method(*args) if method else None
        except:
            successful_call = False
            raise
        finally:
            for limit in self.limits:
                # call with method=None always updates the successful calls
                limit.call()
                if not successful_call:
                    limit._decrease_successful_calls()

    def wait(self):
        """
        Resets the rate limiter after waiting

        Args:
            seconds (int): the number of seconds to wait before resetting
        """
        for limit in self.limits:
            limit.wait()

    def reset_in(self, seconds):
        """
        Resets the rate limiter after waiting

        Args:
            seconds (int): the number of seconds to wait before resetting
        """
        for limit in self.limits:
            limit.reset_in(seconds)

    @property
    def calls(self):
        """
        Returns the number of successful calls (no exceptions in the call) and total calls served by this limiter

        Returns:
            return: tuple   A (successful calls, total calls) tuple
        """
        try:
            return self.limits[0].calls
        except IndexError:
            # Disable the counting if no limits are enforced
            return 0
