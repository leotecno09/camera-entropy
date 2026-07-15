import threading
import hashlib
import time

class HashPool:
    def __init__(self, sources):
        self.sources = sources
        self._lock = threading.Lock()
        self.global_seed = None
        self.last_update = None

    def recompute(self):
        hashes = []
        for src in self.sources:
            h = src.get_hash()

            if h:
                hashes.append(h)

        if not hashes:
            return # nn ci sono fonti

        combined = "".join(sorted(hashes))
        digest = hashlib.sha512(combined.encode()).hexdigest()

        with self._lock:
            self.global_seed = digest
            self.last_update = time.time()

    def get_seed(self):
        with self._lock:
            return self.global_seed, self.last_update