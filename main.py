from src.RTSPSource import RTSPSource
from src.HashPool import HashPool
from app import init_app
from dotenv import load_dotenv
import threading
import time
import os

load_dotenv()  # ridondante con docker

# POOL UPDATER (ogni 30 secondi ricalcola gli hash dalle source della pool)
def pool_updater(pool, interval=30):
    while True:
        pool.recompute()
        time.sleep(interval)

sources = [
    RTSPSource("tapo_leo", os.environ["RTSP_URL_LEO"], interval_seconds=300),
    RTSPSource("tapo_salotto", os.environ["RTSP_URL_SALOTTO"], interval_seconds=300)
]

pool = HashPool(sources)

# avvia i thread delle telecamere
for src in sources:
    threading.Thread(target=src.run_forever, daemon=True).start()

threading.Thread(target=pool_updater, args=(pool,), daemon=True).start()

# init Flask app
app = init_app(pool)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
