import httpx
import click
import asyncio

API_URL = "https://api.marketfiyati.org.tr/api/v2/search"
PAGE_SIZE = 50  # Sayfa başına çekilecek ürün sayısı, API destekliyorsa

async def fetch_page(client, product_name, page_number):
    """Belirli bir sayfadaki veriyi çeker."""
    try:
        # Kullanıcı tarafından sağlanan doğru payload yapısı
        payload = {
            "keywords": product_name,
            "pages": page_number, # Doğru parametre adı 'pages'
            "size": PAGE_SIZE
        }
        response = await client.post(API_URL, json=payload)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        if e.response.status_code != 404:
            click.echo(f"HTTP Hatası (Sayfa {page_number}): {e.response.status_code}", err=True)
    except httpx.RequestError as e:
        click.echo(f"İstek Hatası (Sayfa {page_number}): {e}", err=True)
    return None

async def fetch_data(product_name: str):
    """Bir ürün için tüm sayfalardaki verileri asenkron olarak çeker."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        # İlk sayfayı çekerek toplam sonuç sayısını öğren
        initial_data = await fetch_page(client, product_name, 0)
        if not initial_data or 'numberOfFound' not in initial_data or not initial_data.get('content'):
            return {"numberOfFound": 0, "content": []}

        total_found = initial_data.get('numberOfFound', 0)
        all_content = initial_data.get('content', [])

        if total_found > len(all_content):
            tasks = []
            # Kalan sayfaları çekmek için görevler oluştur
            num_pages = (total_found + PAGE_SIZE - 1) // PAGE_SIZE
            for page_num in range(1, num_pages):
                tasks.append(fetch_page(client, product_name, page_num))
            
            if tasks:
                results = await asyncio.gather(*tasks)
                for page_data in results:
                    if page_data and 'content' in page_data:
                        all_content.extend(page_data['content'])
        
        # Tüm veriyi birleştirip döndür
        final_data = {
            "numberOfFound": len(all_content),
            "content": all_content
        }
        return final_data