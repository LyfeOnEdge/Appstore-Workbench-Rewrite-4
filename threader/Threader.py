import signal, threading, multiprocessing
from collections import deque

import ctypes

class KillException(BaseException):
	pass


class Thread(threading.Thread):
	'''A thread class that supports raising exception in the thread from
	   another thread.
	'''
	def get_id(self):
		if not self.isAlive(): return #If thread is dead
		if hasattr(self, "tid"): return self.tid #earlier grab
		# check threading module _active dict
		for tid, obj in threading._active.items():
			if obj is self:
				self.tid = tid
				return tid
		raise AssertionError("No thread ID")
		
	def stop(self):
		tid = self.get_id()
		if tid:
			res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid),
															 ctypes.py_object(KillException))
			if res == 0:
				raise ValueError("invalid thread id")
			elif res != 1:
				# "if it returns a number greater than one, you're in trouble,
				# and you should call it again with exc=NULL to revert the effect"
				ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid), None)
				raise SystemError("PyThreadState_SetAsyncExc failed")

class Threader:
	def __init__(self, max_worker_threads: int = 3):
		self.queue = deque()
		self.threads = deque()

		self.max_worker_threads = max_worker_threads
		self.watchdogrunning = True
		self.stopwatchdog = False #Flag to stop the loop thread

		signal.signal(signal.SIGINT, self.exit)
		signal.signal(signal.SIGTERM, self.exit)

		#Call mainloop
		self._update_running_threads()

	def new_session(self):
		self.queue = deque()

	def add(self, callback, arglist: list = []):
		t = Thread(target = callback, args = arglist)
		self.queue.append(t)

	def do(self, callback, arglist: list = []):
		t = Thread(target = callback, args = arglist)
		t.start()
		self.threads.append(t)
	#Not to be called by user
	def _update_running_threads(self):
		if self.stopwatchdog:
			self.watchdogrunning = False
			return
		
		self._clear_dead_threads()

		while (self.queue and len(self.threads) < self.max_worker_threads):
			t = self.queue.popleft()
			t.start()
			self.threads.append(t)

		if not self.stopwatchdog:
			self.watchdog = threading.Timer(0.1, self._update_running_threads) # Runs every 100 milliseconds
			self.watchdog.start()

	#Not to be called by user
	def _clear_dead_threads(self):
		if self.threads:
			for t in list(self.threads):
				if not t.is_alive():
					self.threads.remove(t)

	def kill_threads(self):
		print("Killing all worker threads.")
		for t in self.threads:
			print(f"Stopping {t.name}")
			t.stop()

	def exit(self, _ = None, __ = None):
		self.stopwatchdog = True
	
	def join(self):
		for t in self.threads:
			t.join()