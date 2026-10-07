from starlette.responses import StreamingResponse

from src.domains.agent import service


async def chat(request):
    return StreamingResponse(
        service.generator(),
        media_type='application/x-ndjson',
        headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no',
        }
    )
