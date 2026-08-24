"""
Kitap Takip Uygulaması
----------------------
Amaç: Okunan/okunacak kitapları ekleyen, listeleyen, durumunu
(okundu/okunmadı) güncelleyen ve silen basit bir konsol uygulaması.
Kitaplar 'kitaplar.json' dosyasında saklanır; program kapanıp açılınca
kayıtlar korunur.

Nasıl çalıştırılır:
- python3 kitap.py

İşlevler:
1. Kitapları Listele
2. Yeni Kitap Ekle (boş başlık/yazar kabul etmez)
3. Okundu/Okunmadı İşaretle
4. Kitap Sil
5. Çıkış (kayıtları dosyaya yazar)
"""

import json
import os

# Dosya adı sabiti
DOSYA_ADI = "kitaplar.json"


def kitaplari_yukle():
    """
    Kitapları JSON dosyasından yükler.
    Dosya yoksa veya bozuksa boş liste döndürür.
    """
    try:
        with open(DOSYA_ADI, "r", encoding="utf-8") as dosya:
            kitaplar = json.load(dosya)
            # Kitapların doğru formatta olduğundan emin ol
            if not isinstance(kitaplar, list):
                return []
            return kitaplar
    except FileNotFoundError:
        print("Kayıt dosyası bulunamadı. Yeni bir liste oluşturuldu.")
        return []
    except json.JSONDecodeError:
        print("Dosya bozuk. Yeni bir liste oluşturuldu.")
        return []
    except Exception as e:
        print(f"Beklenmeyen bir hata oluştu: {e}")
        return []


def kitaplari_kaydet(kitaplar):
    """
    Kitapları JSON dosyasına kaydeder.
    """
    try:
        with open(DOSYA_ADI, "w", encoding="utf-8") as dosya:
            json.dump(kitaplar, dosya, ensure_ascii=False, indent=2)
        print("Kitaplar başarıyla kaydedildi.")
        return True
    except Exception as e:
        print(f"Kaydetme hatası: {e}")
        return False


def kitaplari_listele(kitaplar):
    """
    Kitapları numaralandırarak listeler.
    """
    if not kitaplar:
        print("\nHenüz kayıtlı kitap yok.")
        return

    print("\n--- KİTAP LİSTESİ ---")
    for i, kitap in enumerate(kitaplar, 1):
        durum = "okundu" if kitap.get("okundu", False) else "okunmadı"
        print(f"{i}. {kitap['baslik']} — {kitap['yazar']} [{durum}]")
    print("---------------------")


def kitap_ekle(kitaplar):
    """
    Kullanıcıdan başlık ve yazar alarak yeni kitap ekler.
    """
    print("\n--- YENİ KİTAP EKLE ---")

    baslik = input("Kitap başlığı: ").strip()
    if not baslik:
        print("Başlık boş olamaz!")
        return

    yazar = input("Yazar: ").strip()
    if not yazar:
        print("Yazar boş olamaz!")
        return

    # Yeni kitap sözlüğü oluştur
    yeni_kitap = {
        "baslik": baslik,
        "yazar": yazar,
        "okundu": False  # Varsayılan olarak okunmadı
    }

    kitaplar.append(yeni_kitap)
    print(f"'{baslik}' eklendi.")

    # Değişiklikleri kaydet
    kitaplari_kaydet(kitaplar)


def durum_degistir(kitaplar):
    """
    Kitap numarasına göre durumu (okundu/okunmadı) değiştirir.
    """
    if not kitaplar:
        print("\nHenüz kayıtlı kitap yok.")
        return

    # Önce kitapları listele
    kitaplari_listele(kitaplar)

    try:
        secim = input("\nDurumunu değiştirmek istediğiniz kitabın numarası: ").strip()
        if not secim:
            print("Lütfen bir numara girin!")
            return

        numara = int(secim)

        if 1 <= numara <= len(kitaplar):
            kitap = kitaplar[numara - 1]
            # Durumu tersine çevir
            kitap["okundu"] = not kitap.get("okundu", False)
            durum = "okundu" if kitap["okundu"] else "okunmadı"
            print(f"'{kitap['baslik']}' artık [{durum}] olarak işaretlendi.")
            kitaplari_kaydet(kitaplar)
        else:
            print("Geçersiz kitap numarası!")

    except ValueError:
        print("Lütfen bir sayı girin!")


def kitap_sil(kitaplar):
    """
    Kitap numarasına göre kitap siler.
    """
    if not kitaplar:
        print("\nHenüz kayıtlı kitap yok.")
        return

    # Önce kitapları listele
    kitaplari_listele(kitaplar)

    try:
        secim = input("\nSilmek istediğiniz kitabın numarası: ").strip()
        if not secim:
            print("Lütfen bir numara girin!")
            return

        numara = int(secim)

        if 1 <= numara <= len(kitaplar):
            silinen_kitap = kitaplar.pop(numara - 1)
            print(f"'{silinen_kitap['baslik']}' silindi.")
            kitaplari_kaydet(kitaplar)
        else:
            print("Geçersiz kitap numarası!")

    except ValueError:
        print("Lütfen bir sayı girin!")


def menu_goster():
    """
    Ana menüyü gösterir.
    """
    print("\n--- KİTAP TAKİP UYGULAMASI ---")
    print("1. Kitapları Listele")
    print("2. Yeni Kitap Ekle")
    print("3. Okundu/Okunmadı İşaretle")
    print("4. Kitap Sil")
    print("5. Çıkış")
    print("-----------------------------")


def ana_program():
    """
    Programın ana akışını yönetir.
    """
    print("Kitap Takip Uygulamasına Hoş Geldiniz!")

    # Kitapları yükle
    kitaplar = kitaplari_yukle()
    if kitaplar:
        print(f"{len(kitaplar)} kitap yüklendi.")

    while True:
        menu_goster()

        try:
            secim = input("Seçiminiz (1-5): ").strip()

            if secim == "1":
                kitaplari_listele(kitaplar)

            elif secim == "2":
                kitap_ekle(kitaplar)

            elif secim == "3":
                durum_degistir(kitaplar)

            elif secim == "4":
                kitap_sil(kitaplar)

            elif secim == "5":
                print("Programdan çıkılıyor...")
                break

            else:
                print("Geçersiz seçim! Lütfen 1-5 arası bir değer girin.")

        except KeyboardInterrupt:
            print("\nProgram kullanıcı tarafından sonlandırıldı.")
            break
        except Exception as e:
            print(f"Beklenmeyen bir hata oluştu: {e}")


# Program başlangıç noktası
if __name__ == "__main__":
    ana_program()