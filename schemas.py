"""
Finance Dashboard Schemas

Each Pydantic model represents a MongoDB collection. The collection name is the lowercase
of the class name (e.g., Asset -> "asset").
"""
from typing import Optional, List, Literal
from pydantic import BaseModel, Field, HttpUrl
from datetime import date


class Asset(BaseModel):
    """
    General assets you own. Can be physical or digital.
    Collection: "asset"
    """
    name: str = Field(..., description="Asset name")
    category: Literal["physical", "digital"] = Field(..., description="Type of asset")
    value: float = Field(..., ge=0, description="Estimated current value in USD")
    notes: Optional[str] = Field(None, description="Additional details")


class Investment(BaseModel):
    """
    Traditional investments like stocks, bonds, funds, real estate.
    Collection: "investment"
    """
    name: str = Field(..., description="Investment name or ticker")
    kind: Literal["stock", "bond", "fund", "real_estate", "other"] = Field(..., description="Investment category")
    institution: Optional[str] = Field(None, description="Brokerage or institution")
    value: float = Field(..., ge=0, description="Current market value in USD")


class Crypto(BaseModel):
    """
    Cryptocurrency holdings.
    Collection: "crypto"
    """
    symbol: str = Field(..., description="Crypto symbol, e.g., BTC")
    amount: float = Field(..., ge=0, description="Units held")
    exchange: Optional[str] = Field(None, description="Exchange or wallet provider")
    value_usd: Optional[float] = Field(None, ge=0, description="Current value in USD (optional)")


class Will(BaseModel):
    """
    Will and estate planning documents.
    Collection: "will"
    """
    title: str = Field(..., description="Document title")
    executor_name: Optional[str] = Field(None, description="Executor full name")
    beneficiaries: List[str] = Field(default_factory=list, description="Beneficiaries list")
    file_url: Optional[HttpUrl] = Field(None, description="Link to stored document")


class TaxFiling(BaseModel):
    """
    Income tax filings and records.
    Collection: "taxfiling"
    """
    year: int = Field(..., ge=1990, le=2100, description="Tax year")
    status: Literal["planned", "in_progress", "filed", "refunded", "due"] = Field(..., description="Filing status")
    filed_on: Optional[date] = Field(None, description="Date filed")
    file_url: Optional[HttpUrl] = Field(None, description="Link to return or receipts")
