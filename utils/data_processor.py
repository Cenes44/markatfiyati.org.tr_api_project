def process_data(api_data):
    """API'den gelen veriyi temizler ve düz bir listeye dönüştürür."""
    clean_data = []
    if not api_data or "content" not in api_data:
        return clean_data

    for product in api_data["content"]:
        if "productDepotInfoList" in product and product["productDepotInfoList"]:
            for depot in product["productDepotInfoList"]:
                clean_data.append(
                    {
                        "Ürün Adı": product.get("title", "N/A"),
                        "Marka": product.get("brand", "N/A"),
                        "Miktar": product.get("refinedVolumeOrWeight", "N/A"),
                        "Market": depot.get("marketAdi", "N/A"),
                        "Market Şubesi": depot.get("depotName", "N/A"),
                        "Fiyat": depot.get("price", "N/A"),
                        "Birim Fiyat": depot.get("unitPrice", "N/A"),
                        "Güncellenme": depot.get("indexTime", "N/A"),
                    }
                )
    return clean_data
