import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from bson import ObjectId

from database import db, create_document, get_documents
from schemas import Asset, Investment, Crypto, Will, TaxFiling

app = FastAPI(title="Finance Dashboard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Finance Dashboard API is running"}


@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️ Connected but Error: {str(e)[:80]}"
        else:
            response["database"] = "⚠️ Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:80]}"

    return response


# Helpers
class IdModel(BaseModel):
    id: str


def _ensure_object_id(id_str: str) -> ObjectId:
    try:
        return ObjectId(id_str)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")


# Generic list endpoints
@app.get("/assets", response_model=List[Asset])
def list_assets() -> List[Asset]:
    docs = get_documents("asset")
    # Convert to Pydantic models (remove _id for response)
    return [Asset(**{k: v for k, v in d.items() if k != "_id"}) for d in docs]


@app.post("/assets")
def add_asset(asset: Asset):
    inserted_id = create_document("asset", asset)
    return {"id": inserted_id, "message": "Asset added"}


@app.get("/investments", response_model=List[Investment])
def list_investments() -> List[Investment]:
    docs = get_documents("investment")
    return [Investment(**{k: v for k, v in d.items() if k != "_id"}) for d in docs]


@app.post("/investments")
def add_investment(investment: Investment):
    inserted_id = create_document("investment", investment)
    return {"id": inserted_id, "message": "Investment added"}


@app.get("/crypto", response_model=List[Crypto])
def list_crypto() -> List[Crypto]:
    docs = get_documents("crypto")
    return [Crypto(**{k: v for k, v in d.items() if k != "_id"}) for d in docs]


@app.post("/crypto")
def add_crypto(crypto: Crypto):
    inserted_id = create_document("crypto", crypto)
    return {"id": inserted_id, "message": "Crypto added"}


@app.get("/wills", response_model=List[Will])
def list_wills() -> List[Will]:
    docs = get_documents("will")
    return [Will(**{k: v for k, v in d.items() if k != "_id"}) for d in docs]


@app.post("/wills")
def add_will(will: Will):
    inserted_id = create_document("will", will)
    return {"id": inserted_id, "message": "Will added"}


@app.get("/tax", response_model=List[TaxFiling])
def list_tax() -> List[TaxFiling]:
    docs = get_documents("taxfiling")
    return [TaxFiling(**{k: v for k, v in d.items() if k != "_id"}) for d in docs]


@app.post("/tax")
def add_tax(filing: TaxFiling):
    inserted_id = create_document("taxfiling", filing)
    return {"id": inserted_id, "message": "Tax filing recorded"}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
