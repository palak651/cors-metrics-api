# CORS-Aware Metrics API

FastAPI service for the metrics assignment.

## Endpoint

`GET /stats?values=1,2,3`

Example response:

```json
{
  "email": "24f2005619@ds.study.iitm.ac.in",
  "count": 3,
  "sum": 6,
  "min": 1,
  "max": 3,
  "mean": 2.0
}
```

## CORS

Only this origin is allowed:

`https://dash-sh27fw.example.com`

A preflight from other origins will not receive `Access-Control-Allow-Origin`.

Every HTTP response, including preflight responses, includes `X-Request-ID` and `X-Process-Time`.

## Deploy on Render

1. Create a public GitHub repository and upload these files to its root.
2. In Render, choose **New + → Web Service** and connect the repository.
3. Use the settings in `render.yaml`, or enter:
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Wait for deployment to finish.
5. Test `https://YOUR-SERVICE.onrender.com/stats?values=1,2,3`.
6. Submit only the base URL, e.g. `https://YOUR-SERVICE.onrender.com`.

Do not submit the example URL; use your actual deployed Render URL.
