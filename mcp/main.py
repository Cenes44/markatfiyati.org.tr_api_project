import asyncio
import json
import sys
import os
import logging

# Proje kök dizinini sys.path'e ekleyerek utils modüllerine erişim sağlıyoruz
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp.server.fastmcp import FastMCP
from utils.api_client import fetch_data
from utils.data_processor import process_data

# stdout yerine stderr'e loglama yapacak şekilde logging ayarları
logging.basicConfig(level=logging.INFO, stream=sys.stderr)

# FastMCP sunucusunu başlat
mcp = FastMCP(
    "market_prices",
    "Türkiye'deki marketler için ürün fiyatlarını arayan bir araç."
)

@mcp.tool()
async def search_prices(product_name: str) -> str:
    """Bir ürünün piyasa fiyatlarını arar ve sonuçları JSON formatında döndürür.

    Args:
        product_name: Aranacak ürünün adı (örn: süt, peynir, zeytinyağı).
    """
    logging.info(f"'{product_name}' için fiyatlar aranıyor...")
    
    api_response = await fetch_data(product_name)
    if not api_response or not api_response.get("content"):
        logging.info(f"'{product_name}' için veri bulunamadı.")
        return json.dumps({"error": "Ürün için veri bulunamadı."})

    processed_data = process_data(api_response)
    if not processed_data:
        logging.info(f"'{product_name}' için işlenecek veri bulunamadı.")
        return json.dumps({"error": "İşlenecek veri bulunamadı."})

    logging.info(f"{len(processed_data)} adet sonuç bulundu ve döndürülüyor.")
    # Sonucu JSON string olarak döndür
    return json.dumps(processed_data, indent=2, ensure_ascii=False)

def main():
    """Sunucuyu başlatır."""
    mcp.run(transport="sse", host="0.0.0.0", port=8080)

if __name__ == "__main__":
    main()
