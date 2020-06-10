import asyncio
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
import os
from soco_mrc.mrc_model import MRCModel
from soco_mrc.config import EnvVars


path = os.path.dirname(__file__)

app = Starlette()
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_headers=['X-Requested-With', 'Content-Type'])
model = MRCModel(EnvVars.region, EnvVars.use_gpu, EnvVars.max_ans_len)

loop = asyncio.get_event_loop()
loop.close()

@app.route('/v1/ping', methods=['GET'])
async def ping(request):
    return JSONResponse({'result': 'pong'})


@app.route('/v1/query', methods=['POST'])
async def analyze(request):
    body = await request.json()
    data = body['data']
    model_id = body['model_id']
    n_best = body.get('n_best', 1)
    results = model.batch_predict(model_id, data, n_best)
    print(results[0:5])
    return JSONResponse({'result': results})

