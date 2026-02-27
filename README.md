# Hepsiburada UI & API Automation

Bu proje, Hepsiburada icin UI ve API otomasyon testlerini `pytest` ile calistirmak icin hazirlanmistir.

## Kullanilan Teknolojiler
- Python
- Pytest
- Selenium WebDriver (Chrome)
- Standart kutuphane tabanli HTTP client (`urllib`)

## Proje Yapisi
- `tests/`: Test senaryolari
- `tests/api/`: API testleri
- `src/pages/`: UI Page Object siniflari
- `src/utils/`: Locator ve wait yardimcilari
- `src/api/`: API istemcisi

## Test Case - Dosya Eslesmesi

| Case / Senaryo | Aciklama | Dosya |
|---|---|---|
| Scenario 1 (UI) | Ana sayfada `ps5` aramasi yapar, rastgele urune gider, yorumlar alanina inip siralama/etkilesim adimlarini dogrular. | `tests/test_senaryo_1.py` |
| Scenario 2 (UI) | Ana sayfada `iphone` aramasi yapar, urun detayina gider, karsilastirma alani/fiyatlari kontrol eder, uygun urunu sepete ekler. | `tests/test_senaryo_2.py` |
| Swagger Generator API (API) | `/gen/clients` ile dil listesi alir, secili dil icin client uretir, donen `code` ile indirmenin 200 dondugunu dogrular. | `tests/api/test_api_automation.py` |

## Pytest Marker'lari
`pytest.ini` icinde tanimli marker'lar:
- `ui`: UI test suite
- `api`: API test suite

## Notlar
- API testlerinde SSL dogrulamasi varsayilan olarak kapalidir (`--api-verify-ssl` verilirse aktif olur).
- Varsayilan API base URL: `https://generator.swagger.io/api`
