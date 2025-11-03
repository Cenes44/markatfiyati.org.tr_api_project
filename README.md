
# Piyasa Fiyatları Getirici (Market Price Fetcher)

Bu proje, bir ürünün piyasa fiyatlarını çeşitli kaynaklardan toplayan bir CLI (Komut Satırı Arayüzü) ve bir FastAPI uygulaması içerir. Elde edilen veriler CSV, Excel veya Word formatında raporlanabilir.

## Özellikler

- **CLI Uygulaması**: Komut satırından hızlıca ürün fiyatlarını arayın ve dosya olarak kaydedin.
- **FastAPI Uygulaması**: Web üzerinden erişilebilen, verileri dosya olarak indirmenize olanak tanıyan bir REST API.
- **Çoklu Format Desteği**: Verileri `.csv`, `.xlsx` (Excel) ve `.docx` (Word) olarak alın.
- **Temiz Veri**: API'den gelen karmaşık veriler işlenerek anlaşılır bir tablo formatına dönüştürülür.
- **Asenkron İşlemler**: `httpx` ve `asyncio` sayesinde hızlı ve verimli veri çekme.
- **Modern Araçlar**: Paket yönetimi için `uv`, API için `FastAPI` ve CLI için `Click` kullanılmıştır.

## Kurulum

Projeyi yerel makinenizde kurmak için aşağıdaki adımları izleyin.

1.  **Python 3.13 veya üstü** bir sürümün yüklü olduğundan emin olun.

2.  **`uv`'yi yükleyin** (eğer yüklü değilse):
    ```sh
    pip install uv
    ```

3.  **Sanal Ortam Oluşturun**:
    Proje ana dizininde aşağıdaki komutu çalıştırın:
    ```sh
    uv venv
    ```

4.  **Bağımlılıkları Yükleyin**:
    Gerekli tüm kütüphaneleri kurmak için aşağıdaki komutu çalıştırın:
    ```sh
    uv pip sync pyproject.toml
    ```

## Kullanım

### 1. CLI (Komut Satırı Arayüzü)

Komut satırı uygulamasını çalıştırmak için `uv run` komutunu kullanın. Raporlar projenin ana dizinine kaydedilecektir.

**Temel Kullanım:**

```sh
uv run main.py <ürün_adı> --format <format>
```

-   `<ürün_adı>`: Aramak istediğiniz ürün (örn: `domates`, `zeytinyağı`).
-   `--format`: İsteğe bağlı olarak `csv`, `excel`, veya `word` (varsayılan: `csv`).

**Örnekler:**

-   **CSV (varsayılan) formatında** "elma" fiyatlarını almak için:
    ```sh
uv run main.py elma
    ```

-   **Excel formatında** "peynir" fiyatlarını almak için:
    ```sh
uv run main.py peynir --format excel
    ```

-   **Word formatında** "patlıcan" fiyatlarını almak için:
    ```sh
uv run main.py patlıcan --format word
    ```

### 2. FastAPI Uygulaması

API sunucusunu başlatmak için proje ana dizininde aşağıdaki komutu çalıştırın:

```sh
uv run uvicorn fastapi.main:app --reload
```

Sunucu başlatıldıktan sonra (`http://127.0.0.1:8000`), aşağıdaki yolları kullanarak API'yi test edebilirsiniz.

-   **İnteraktif API Belgeleri (Swagger UI)**:
    Tarayıcınızda `http://127.0.0.1:8000/docs` adresini açarak API'yi kolayca test edebilir ve tüm endpoint'leri görebilirsiniz.

-   **Doğrudan Endpoint Kullanımı**:
    Tarayıcınıza aşağıdaki URL'leri yazarak doğrudan dosya indirebilirsiniz:

    -   **CSV için:** `http://127.0.0.1:8000/search/?product_name=süt&format=csv`
    -   **Excel için:** `http://127.0.0.1:8000/search/?product_name=süt&format=excel`
    -   **Word için:** `http://127.0.0.1:8000/search/?product_name=süt&format=word`

### 3. MCP Sunucusu (Yapay Zeka Ajanları için)

Bu proje ayrıca, [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) standardına uygun bir sunucu içerir. Bu sunucu, Claude gibi yapay zeka asistanlarının yerel olarak ürün fiyatlarını sorgulamasına olanak tanır.

**Sunucuyu Çalıştırma:**

Sunucu, AI asistanı tarafından gerektiğinde otomatik olarak başlatılır. Manuel olarak test etmek veya çalıştırmak için proje ana dizininde aşağıdaki komutu kullanabilirsiniz:

```sh
uv run mcp/main.py
```

**AI Asistanına Entegre Etme:**

Claude for Desktop gibi bir MCP istemcisine bu aracı eklemek için, istemcinin yapılandırma dosyasını düzenlemeniz gerekir. Dokümantasyonda belirtildiği gibi, `mcpServers` anahtarı altına aşağıdaki gibi bir yapı eklenmelidir (dosya yolunu kendi sisteminize göre güncellemeyi unutmayın):

```json
{
  "mcpServers": {
    "market_prices": {
      "command": "uv",
      "args": [
        "--directory",
        "C:/Users/wın10/Desktop/Projelerim/Proje 1",
        "run",
        "mcp/main.py"
      ]
    }
  }
}
```
