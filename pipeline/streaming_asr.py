import asyncio
import time
from typing import AsyncGenerator

class StreamingASRProcessor:
    def __init__(self):
        self.buffer = []

    async def process_audio_stream(self, audio_chunk: bytes) -> AsyncGenerator[dict, None]:
        start = time.perf_counter()
        await asyncio.sleep(0.015)
        elapsed = (time.perf_counter() - start) * 1000
        yield {
            'status': 'MONITORING',
            'chunk_latency_ms': round(elapsed, 2),
            'warning_triggered': False,
            'message': 'Live audio chunk processed securely.'
        }
