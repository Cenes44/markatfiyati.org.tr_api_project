import asyncio

import click

from utils.api_client import fetch_data
from utils.data_processor import process_data
from utils.file_saver import save_as_csv, save_as_excel, save_as_word


@click.command()
@click.argument("product_name")
@click.option(
    "--format",
    type=click.Choice(["csv", "excel", "word"], case_sensitive=False),
    default="csv",
    help="Çıktı formatı.",
)
def main(product_name, format):
    """
    Belirtilen ürün adını kullanarak piyasa fiyat verilerini çeker ve
    belirtilen formatta, temizlenmiş olarak kaydeder.
    """
    click.echo(f"'{product_name}' için veri çekiliyor ve işleniyor...")

    api_response = asyncio.run(fetch_data(product_name))

    if not api_response:
        click.echo("API'den veri alınamadı.", err=True)
        return

    processed_data = process_data(api_response)

    if not processed_data:
        click.echo("İşlenecek veri bulunamadı.")
        return

    if format == "csv":
        save_as_csv(processed_data, product_name)
    elif format == "excel":
        save_as_excel(processed_data, product_name)
    elif format == "word":
        save_as_word(processed_data, product_name)


if __name__ == "__main__":
    main()
