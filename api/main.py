from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route, WebSocketRoute
from starlette.websockets import WebSocket, WebSocketDisconnect
from pipeline.normalizer import normalize_code_mixed_text
from pipeline.dual_path import DualPathEngine
from pipeline.streaming_asr import StreamingASRProcessor
from pipeline.threat_cache import LocalThreatCache

dual_engine = DualPathEngine()
threat_cache = LocalThreatCache()
asr_processor = StreamingASRProcessor()

async def verify_threat(request):
    body = await request.json()
    text = body.get('text', '')
    normalized_text = normalize_code_mixed_text(text)
    result = dual_engine.fast_classify(normalized_text)
    xai_rationale = dual_engine.generate_xai_rationale(result['threat_type'], normalized_text)
    return JSONResponse({**result, 'normalized_input': normalized_text, 'xai_rationale': xai_rationale})

async def verify_upi(request):
    body = await request.json()
    vpa = body.get('vpa', '')
    amount = float(body.get('amount', 0.0))
    mcc = body.get('mcc', '5411')
    return JSONResponse(threat_cache.verify_vpa(vpa, amount, mcc))

async def websocket_audio_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_bytes()
            async for response in asr_processor.process_audio_stream(data):
                await websocket.send_json(response)
    except WebSocketDisconnect:
        pass

async def health_check(request):
    return JSONResponse({'status': 'healthy', 'architecture': 'Pure Starlette ASGI Core + Dual-Path XAI Active'})

routes = [
    Route('/api/v1/verify-threat', verify_threat, methods=['POST']),
    Route('/api/v1/verify-upi', verify_upi, methods=['POST']),
    WebSocketRoute('/ws/audio-stream', websocket_audio_endpoint),
    Route('/health', health_check, methods=['GET'])
]

app = Starlette(debug=True, routes=routes)
