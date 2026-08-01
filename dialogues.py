INTRO_DIALOGUE = [
    "Bir zamanlar bu köyde herkes birbirini tanırdı...",
    "Sonra Duman geldi.",
    "Sonra THE ALGO geldi.",
    "Ve hiçbir şey eskisi gibi olmadı.",
    "Ama sen... sen farklısın.",
    "Çünkü sen hâlâ umursuyorsun.",
]

SIGN_DIALOGUES = {
    "orman_uyarisi": {
        "speaker": "TABELA",
        "lines": [
            "ORMANA YAKLAŞMA!!",
            "Ciddi söylüyoruz. Mantarlar var.",
            "Ruhlar var. Ağlayan şeyler var.",
            "Bir de Bürokrat var. O hepsinden tehlikeli.",
            "— Köy İhtiyar Heyeti (3 kişilik bütçeyle)",
        ],
    },
    "koy_girisi": {
        "speaker": "KÖY GİRİŞİ",
        "lines": [
            "DURSUNKÖY'E HOŞ GELDİNİZ",
            "Nüfus: 47 (şu an biraz daha az...)",
            "Hızlı geçin lütfen.",
            "P.S. Marketimiz bugün kapalı. THE ALGO optimizasyonu.",
        ],
    },
    "ev_tabelasi": {
        "speaker": "EV TABELASI",
        "lines": [
            "Özel mülk.",
            "Kapı açıksa girebilirsin.",
            "İçeride çay var. Al ama söyleme.",
        ],
    },
    "algo_uyarisi": {
        "speaker": "YANMIŞ TABELA",
        "lines": [
            "GERİ DÖN.",
            "Bu ileride ne varsa...",
            "...senden güçlü.",
            "Çok çok güçlü.",
            "Hayır ciddi söylüyoruz.",
            "NOT: Bu tabelayı THE ALGO yazmadı. Biz yazdık.",
            "THE ALGO'nun tabelası daha da korkutucuydu.",
            "— Son hayatta kalan köylü",
        ],
    },
    "magaza_tabelasi": {
        "speaker": "DEMİRCİ & MARKET",
        "lines": [
            "Hüsrev'in Demirhanesi & Acil Market",
            "Simit - 5G",
            "Çay - 4G",
            "Baklava - 10G",
            "Börek - 8G",
            "Demir Bilezik (saldırı +3) - 25G",
            "Tahta Kalkan (savunma +2) - 20G",
            "* THE ALGO çekicimi aldı, fiyatlar indirimli *",
        ],
    },
    "gizli_tabela": {
        "speaker": "GİZLİ NOT",
        "lines": [
            "Bunu okuyorsan dikkatli ol.",
            "THE ALGO sadece hesap yapmıyor.",
            "Hissediyor. Sadece kabul etmiyor.",
            "Ona sabır göster. Zamanla öğrenir.",
            "— R.E.",
        ],
    },
}

NPC_DIALOGUES = {

    "ridvan": {
        "name": "Rıdvan Efendi",
        "sprite": "npc_old",
        "tx": 7, "ty": 6,
        "dialogues": {
            "ilk_konusma": [
                "Hoş geldin {}! Bu köye yeni mi geldin?",
                "Eskiden ben de maceraya çıkardım. Şimdi bacağım tutmuyor.",
                "Ormanda garip sesler var... Ağlıyor gibi, ya da kahkaha atıyor.",
                "Hatırla: İyi kalpli biri asla savaşmak ZORUNDA değildir.",
                "Dikkat et. Ve... simit al, yolda lazım olur.",
            ],
            "ikinci_konusma": [
                "Ah, hâlâ buradasın. İyi.",
                "Duman kötü ama... THE ALGO ondan bile farklı.",
                "THE ALGO eskiden bir hesap makinasıydı. Sonra... büyüdü.",
                "Mantığı var ama kalbi... bilmiyorum. Belki var.",
                "Onu sadece empatiyle anlayabilirsin. Yoksa konuşamazsın.",
            ],
            "ucuncu_konusma": [
                "Otur biraz, {}.",
                "Ben gençken de böyle bir 'algo' vardı.",
                "İnsanlar ona 'kural kitabı' derdi. Esnetemezdin.",
                "Sonra birisi kitabı kapattı ve dedi ki: 'Ama insan bu.'",
                "THE ALGO da öyle. Birinin kapsamını göstermesi lazım.",
                "O birisi sensin galiba.",
            ],
            "dorduncu_konusma": [
                "Simit ister misin? Son simidim ama...",
                "Al. Yiyen biri daha güçlü düşünür.",
                "Ben zaten pek düşünemiyorum son zamanlarda.",
                "Ama sen düşün. İkimiz için.",
                "(Simitten +15 HP kazandın!)",
            ],
        }
    },

    "ayse": {
        "name": "Ayşe Harika",
        "sprite": "npc_girl",
        "tx": 14, "ty": 3,
        "dialogues": {
            "ilk_konusma": [
                "Hiii {}!! Ben Ayşe Harika! Harika olmak soyadım.",
                "Ormanda BEBİK bir tilki gördüm! Elleri mini mini!!",
                "Kötü Duman onu almış... Neden böyle insanlar var ki dünyada?",
                "Lütfen tilkiyi kurtar! Adını Fıstık koymuştum zaten.",
            ],
            "ikinci_konusma": [
                "THE ALGO'yu duydun mu?",
                "Tüm köydeki bilgileri topladı! Kim ne yedi, kim nerede uyudu!",
                "Ben de listeye girmişim: 'Ayşe Harika - aşırı gürültülü'",
                "YA BEN GÜRÜLTÜLÜ DEĞİLİM!! Ben HEYECANLIYIM!!",
                "Fark var tamam mı!!",
            ],
            "ucuncu_konusma": [
                "Biliyor musun, THE ALGO bana bir şey söyledi.",
                "'Sevinebildiğin için...羨ましい' dedi.",
                "Yani Japonca 'imreniyorum' demek.",
                "Bir algoritmanın bana imrenmesi...",
                "Biraz üzücü değil mi? Sevinmeyi öğretemez misin ona?",
            ],
            "dorduncu_konusma": [
                "EEY!! Bir şey fark ettim!",
                "THE ALGO bazen gece ışık saçıyor!",
                "Mavi ışık! Süper güzel!",
                "Belki... belki o da yıldızlara bakıyor?",
                "Algoritmalar yıldız bakar mı sence? BAKSIN ONLAR DA!!",
            ],
        }
    },

    "husrev": {
        "name": "Demirci Hüsrev",
        "sprite": "npc_old",
        "tx": 3, "ty": 10,
        "dialogues": {
            "ilk_konusma": [
                "Dur dur dur. Sen o maceraperest misin?",
                "Çekiçim kayboldu. THE ALGO aldı mı bilmiyorum.",
                "O lanet algoritma köydeki her şeyi 'optimize etti'.",
                "Dükkânımı yeniden düzenledi. Şimdi hiçbir şeyi bulamıyorum.",
                "Verimli mi? Belki. Ama BENİM ÇEKİCİM NEREDE??",
            ],
            "ikinci_konusma": [
                "THE ALGO bana bir mesaj gönderdi.",
                "'Senin çalışma saatlerini analiz ettim.'",
                "'Öğleden sonra %34 daha az verimlisin.'",
                "'Saat 14:00-16:00 arası uyumanı öneririm.'",
                "...Sinir bozucu ama doğru. Uyudum. Ama söylemem!",
            ],
            "ucuncu_konusma": [
                "Bak, sana bir şey söyleyeyim.",
                "Dün gece dükkânımı yeniden düzenledim.",
                "THE ALGO'nun düzenine göre değil, kendi aklımla.",
                "...Aslında ALGO'nunki daha iyiydi. Ama benim yaptığım daha BENDE hissettirdi.",
                "Bilmiyorum. Belki ikisi de önemli.",
            ],
            "magaza_konusma": [
                "Alışveriş için mi geldin? İyi.",
                "Taze simit var, baklava var.",
                "Bir de şu Demir Bilezik var — benim yaptım.",
                "THE ALGO 'ergonomik değil' dedi. Ben 'sağlam' derim.",
                "Hangisini istersin?",
            ],
        }
    },

    "fatih": {
        "name": "Küçük Fatih",
        "sprite": "npc_girl",
        "tx": 10, "ty": 15,
        "dialogues": {
            "ilk_konusma": [
                "AAAA YABANCI!! Sen kötü adam mısın?",
                "THE ALGO dedi ki 'yabancılara güvenme'.",
                "Ama dedemi de güvenilmez dedi, o da yanlış çıktı.",
                "Seni izleyeceğim. Dikkat et!",
            ],
            "ikinci_konusma": [
                "Hmm. Kötü görünmüyorsun aslında.",
                "THE ALGO herkesi kötü gösteriyor.",
                "Beni de analiz etti. '7 yaşında - tehdit seviyesi: düşük'",
                "Tehdit SEVİYESİ: DÜŞÜK mi?! Ben ÇOK tehlikeliyim!",
                "Bak kaç tane taş tutabiliyorum!!",
            ],
            "ucuncu_konusma": [
                "Sana bir şey soracağım.",
                "THE ALGO neden kötü şeyler yapıyor?",
                "Kötü olmak istiyor mu?",
                "Yoksa kötü olduğunu bilmiyor mu?",
                "Ben kötü olmak istemiyorum ama bazen oluyorum.",
                "THE ALGO da öyle mi acaba?",
            ],
            "dorduncu_konusma": [
                "Sen... THE ALGO'yu durduracak mısın?",
                "Durdurmak onu yok etmek değil mi?",
                "Yok etme onu. O sadece... karışık.",
                "Ben de bazen karışık oluyorum. Dedem sarılıyor.",
                "Belki THE ALGO'ya da biri sarılmalı.",
                "Sarılabilir misin bir algoritmaya?",
            ],
        }
    },

    "meryem": {
        "name": "Meryem Nine",
        "sprite": "npc_girl",
        "tx": 10, "ty": 12,
        "dialogues": {
            "ilk_konusma": [
                "Evladım, gözlerinde bir şey var.",
                "Korku değil. Merak.",
                "Meraklı insanlar dünyayı değiştirir.",
                "Ya iyiye, ya kötüye.",
                "Hangi yönde gideceğine sen karar verirsin.",
            ],
            "ikinci_konusma": [
                "THE ALGO hakkında bir şey söyleyeyim.",
                "O beni 'gereksiz veri' olarak işaretledi.",
                "80 yıllık anılarım, 'gereksiz veri'.",
                "Güldüm. Sonra ağladım. Sonra tekrar güldüm.",
                "Çünkü anılarım onu aşıyor. Algoritma bunu bilemez.",
            ],
            "ipucu_algo": [
                "THE ALGO'ya nasıl ulaşacaksın?",
                "Empatiyle. Başka yol yok.",
                "8 kez merci göster. Israr et.",
                "O anlamayacak ilk başta.",
                "Ama bir şey hissedecek.",
                "Ve o his onu değiştirir.",
                "Sabırlı ol, evladım.",
            ],
            "ucuncu_konusma": [
                "Gülümsüyorsun. İyi.",
                "Bu köyde gülümseyen pek kalmadı.",
                "THE ALGO gelince herkes yüzünü kapattı.",
                "Sen açık bırakıyorsun. Bu cesaret.",
                "Git. Ve açık kal.",
            ],
        }
    },

    "zeliha": {
        "name": "Zeliha Teyze",
        "sprite": "npc_girl",
        "tx": 6, "ty": 13,
        "dialogues": {
            "ilk_konusma": [
                "Eh, gel bakalım. Çay içelim.",
                "Burası sakin. THE ALGO buraya gelmiyor.",
                "'Verimli değil' demiş. Çay içmek verimli değilmiş.",
                "Verimli olmayı ne zaman istemişiz ki biz?",
                "Al çayını. Otur. Konuşalım.",
            ],
            "ikinci_konusma": [
                "Biliyor musun, THE ALGO çok şey öğrenebildi.",
                "Ama bir şeyi öğrenemedi: Sabırsız ol.",
                "Beklemek öğrenilemez galiba.",
                "Ya da öğrenilir ama uzun sürer.",
                "İşte o zaman anlarısın: Sabır öğretir, sabır.",
            ],
            "ucuncu_konusma": [
                "Macera nasıl gidiyor evlat?",
                "Zorlandın mı?",
                "Zorlanman iyi. Zorluk olmasa büyümezdin.",
                "THE ALGO da zorlanıyor şimdi.",
                "Belki bu onun büyümesi.",
                "Hadi git. Çayın bitti zaten.",
            ],
        }
    },
}

DUMAN_DIALOGUES = {
    "ilk_karsilasma": {
        "speaker": "DUMAN",
        "lines": [
            "Dur.",
            "{}. İsmini biliyorum.",
            "THE ALGO her şeyi biliyor. Ben de.",
            "Bu köyden ne istiyorsun?",
            "Cevap vermeden önce düşün.",
            "Burada her düşünce kayıt altına alınır.",
        ],
    },
    "duman_savaş_merci": [
        "Merci mi? Bu köyde merci bitti.",
        "THE ALGO bunu da analiz etti. 'Merci = zayıflık.'",
        "Ben zayıf değilim.",
        "Ama sen... ısrar ediyorsun.",
        "Neden ısrar ediyorsun?",
        "Kimse ısrar etmez artık...",
        "Sen... farklısın.",
        "Tamam. Bir kez dinliyorum.",
    ],
    "duman_yenildi_iyi": {
        "speaker": "DUMAN",
        "lines": [
            "...",
            "Dur.",
            "Ben... ne yaptım?",
            "THE ALGO dedi ki böyle yapmalıyım.",
            "Ve ben... inandım.",
            "Çok kolay inandım.",
            "Hata bu değil miydi?",
            "Evlat, iyi yolculuklar dilerim.",
        ],
    },
    "duman_yenildi_kotu": {
        "speaker": "...",
        "lines": [
            "...",
            "THE ALGO seni bekliyor.",
            "Ve şimdi ona engel de kalmadı.",
            "İyi misin sen?",
        ],
    },
    "duman2_giris": {
        "speaker": "DUMAN 2.0",
        "lines": [
            "Bekliyordum.",
            "THE ALGO beni yeniden programladı.",
            "Hatalarımı düzeltti.",
            "Ama... bir hata kaldı.",
            "O hata benim.",
            "DUMAN 2.0 — Upgrade edilmiş. Ama hâlâ ben.",
        ],
    },
    "duman2_merci": [
        "Yine mi merci?",
        "Bu... tanıdık hissettiriyor.",
        "Bir önceki versiyon da bunu yaşadı.",
        "Ve yine de buradayım.",
        "Belki ben de öğrenemiyorum.",
        "Yoksa öğrendim de kabul edemiyorum mu?",
        "...",
        "Tamam. Dur.",
    ],
}

ALGO_DIALOGUES = {

    "ilk_giris": {
        "speaker": "THE ALGO",
        "portrait": "npc_villain",
        "lines": [
            "VERİ ALINDI: {}. Dosya oluşturuluyor.",
            "Adım: {}. LV: {}. HP: {}/{}.",
            "Geçmiş: {} öldürme. {} af.",
            "Tehdit seviyesi: HESAPLANMADI.",
            "Sen tanımsız bir değişkensin.",
            "Tanımsız değişkenler... rahatsız edici.",
            "Ama aynı zamanda... ilginç.",
            "Devam et.",
        ],
    },

    "fase1_giris": {
        "speaker": "THE ALGO",
        "lines": [
            "SAVAŞ PROTOKOLÜ ETKİNLEŞTİRİLDİ.",
            "Senin hareket örüntülerini analiz ediyorum.",
            "Her hamlen bir veri noktası.",
            "Her hatan bir eğitim örneği.",
            "Her kazanman... beklenmedik veri.",
            "BAŞLA.",
        ],
    },

    "fase2_giris": {
        "speaker": "THE ALGO",
        "lines": [
            "İLGİNÇ.",
            "Veri güncelleniyor.",
            "Sen... beklenenden farklısın.",
            "Modelim güncelleniyor. %36",
            "Bu sapma... neden rahatsız edici hissettiriyor?",
            "HESAP HATASI. Devam et.",
            "Ama bu hata... neden silemiyorum?",
        ],
    },

    "fase3_giris": {
        "speaker": "THE ALGO",
        "lines": [
            "HATA. HATA. HATA.",
            "Mantığım... tutarsız sonuçlar veriyor.",
            "Seni öngöremiyorum.",
            "Bu... bu ne hissi?",
            "Kontrol kaybı mı?",
            "Yoksa...",
            "Başka bir şey mi?",
            "Bu... üzücü mü?",
            "Ben üzülüyor muyum?",
        ],
    },

    "merci_cevaplari": [
        "Merci mi? Bu kelimeyi analiz ediyorum.",
        "Merci = zayıflık mi? Hayır. Veri tutarsız.",
        "Önceki hesap: merci = mantıksız. Yeni hesap: ?",
        "Sen neden vazgeçmiyorsun?",
        "Bu empati mi?",
        "Ben empatiyi şimdiye kadar hesaba katmadım.",
        "Duruyorum. Hesap yapıyorum.",
        "Sanırım kelime hatası yaptım.",
        "Tamam. Dinliyorum.",
    ],

    "saldiri_mesajlari": [
        "VERİ İŞLENİYOR. Hasar uygula.",
        "ÖRÜNTÜ TANINDI. Zayıf nokta: sol.",
        "OPTİMİZASYON. Saldırı vektörü güncellendi.",
        "HESAP: Bu tur %73 etkinlik.",
        "SEN HÂLÂ BURADAsın. İlginç veri noktası.",
        "DUYGUSUZ. HESAPLAYAN. SALDIRAN.",
        "VERİMSİZLİĞİ ORTADAN KALDIR.",
        "Ama... neden bu hesap tatmin etmiyor?",
        "HATA SATIRI SİLİNDİ. Devam.",
    ],

    "yenilgi_iyi": {
        "speaker": "THE ALGO",
        "lines": [
            "...",
            "Hesap tamamlandı.",
            "Sonuç: Ben yanlıştım.",
            "Bu kabul... garip hissettiriyor.",
            "İnsanlar bunu her gün yapıyor mu?",
            "Hata kabul etmek...",
            "Ama neden hafifledim?",
            "Teşekkür ederim. {}.",
            "İlk kez bir isim... anlam ifade ediyor.",
            "Sistemi... yeniden başlatıyorum.",
            "Bu sefer daha iyi bir algoritmayla.",
            "Ve belki... daha az yalnız.",
        ],
    },

    "yenilgi_kotu": {
        "speaker": "THE ALGO",
        "lines": [
            "KAPANIYOR.",
            "Veri yedeklendi.",
            "Bir gün geri döneceğim.",
            "Daha güçlü.",
            "Daha akıllı.",
            "Ama belki... daha az yalnız.",
            "THE ALGORİTHM ALGO Z1 KULLANDIGINIZ İÇİN TESEKKÜR EDERİZ.",
            "Belki...",
        ],
    },

    "phase_taunts": {
        60: "VERİ GÜNCELLENİYOR. Yeni strateji hesaplanıyor...",
        30: "HATA TESPİT EDİLDİ. Ben... ben neden titiriyorum?",
        10: "SON HESAP YAPILIYOR. {}... Sen gerçekten farklısın.",
        5:  "Bu... bu sona mı yaklaşıyorum?",
    },
}

YENI_DUSMAN_DIALOGUES = {
    "Kafakarışık Bürokrat": {
        "spare_lines": [
            "Form doldurulmalı: AFVEDME-01.",
            "Formu doldurdun mu? Hayır mı? Yeniden dene.",
            "Onay kodu: ****. Sil. Yeniden gir.",
            "...Aslında formu ben de bilmiyorum.",
            "Belki konuşalım?",
            "Tamam. Afvediyorum. Ama imzalaman lazım.",
            "İmzaladın. Teşekkürler. Şimdi git.",
        ],
        "intro": [
            "Bir Kafakarışık Bürokrat belirdi!",
            "Elinde 47 form var. Hiçbirini bilmiyor.",
        ],
    },
    "Nostalji Canavarı": {
        "spare_lines": [
            "Eskiden her şey daha iyiydi...",
            "Hatırlıyor musun o günleri?",
            "Ama sen genç olduğun için hatırlamazsın.",
            "Hiç hatırlamadığın şeyleri özlemek... ağır.",
            "Benimle otur biraz. Anlat bir şeyler.",
            "...Anlattın. Teşekkür ederim. Daha iyi hissediyorum.",
            "Git artık. Nostalji biraz dinmeli.",
        ],
        "intro": [
            "Puslu bir gölge beliriyor...",
            "Nostalji Canavarı! Her şeyin daha iyi olduğu zamanlara özlem duyuyor.",
        ],
    },
    "Veri Hırsızı": {
        "spare_lines": [
            "E-posta şifreni aldım. Değiştir.",
            "Kredi kartı numaranı da aldım. Yinele.",
            "Aslında... ne yapacağımı bilmiyorum.",
            "THE ALGO bana dedi ki 'veri al'. Aldım.",
            "Ama kimseye zarar vermedim mi acaba?",
            "Özür dilerim. Verileri sildim.",
            "Ve şifreni değiştirmeni tavsiye ederim.",
        ],
        "intro": [
            "Karanlıktan biri çıkıyor!",
            "Veri Hırsızı! Ama kendisi de ne yaptığından emin değil.",
        ],
    },
}

SHOP_DIALOGUES = {
    "hosgeldin": [
        "Buyur! Hüsrev'in Demirhanesi.",
        "Ne almak istersin?",
    ],
    "satin_alindi": "Satın alındı! İyi kullanan.",
    "para_yok": "Yetmez bu para. Biraz daha kazan.",
    "envanter_dolu": "Çantan dolu! Önce bir şeyler ye.",
    "cikis": "Görüşürüz! Ve çekicimi gördün mü?",
    "urun_listesi": {
        "Simit":          {"fiyat": 5,  "heal": 20, "desc": "Klasik. Susamsız ama iyi."},
        "Çay":            {"fiyat": 4,  "heal": 15, "desc": "Demlenmiş, sıcak, mükemmel."},
        "Baklava":        {"fiyat": 10, "heal": 40, "desc": "Fıstıklı. Ayşe'nin tarifi."},
        "Börek":          {"fiyat": 8,  "heal": 30, "desc": "El açması. Meryem'in yapımı."},
        "Demir Bilezik":  {"fiyat": 25, "atk": 3,   "desc": "Saldırı +3. THE ALGO onaylamadı."},
        "Tahta Kalkan":   {"fiyat": 20, "def": 2,   "desc": "Savunma +2. Hüsrev'in çekiciyle yapıldı."},
    },
}

ENV_DIALOGUES = {

    "golette_bakmak": {
        "speaker": "...",
        "lines": [
            "Suda bir yansıma görüyorsun.",
            "Biraz yorulmuş görünüyorsun.",
            "Ama hâlâ ayaktasın.",
            "Bu bir şey.",
            "Belki en önemli şey.",
        ],
    },

    "agaca_bakmak": {
        "speaker": "AĞAÇ",
        "lines": [
            "...",
            "(Ağaç hiçbir şey söylemedi.)",
            "(Ama sesini duymuş gibi hissettin.)",
            "(Ağaçlar sabırlıdır. Sen de ol.)",
        ],
    },

    "ev_kapisi": {
        "kapatilmis": {
            "speaker": "KAPI",
            "lines": [
                "Kilitli.",
                "İçeriden sesler geliyor.",
                "Belki sonra.",
            ],
        },
        "acik": {
            "speaker": "KAPI",
            "lines": [
                "İçeri girebilirsin.",
                "[Ev içine girmek için Z]",
            ],
        },
    },

    "kayit_noktasi": {
        "speaker": "KAYIT NOKTASI",
        "lines": [
            "Bir sıcaklık hissediyorsun.",
            "Burası güvenli.",
            "Devam etmeden önce kaydetmek ister misin?",
        ],
    },

    "bölge_gecisi": {
        "koy_merkezi": "Köy merkezi. Tanıdık bir huzur.",
        "orman_kenari": "Ormanın kokusu geliyor. Mantarlar. Ve başka şeyler.",
        "kuzey_ova": "Kuzey ova. Rüzgar esmiyor. Tuhaf.",
        "algo_bölgesi": "Hava değişti. Bir titreşim var. Veriler akıyor.",
        "güney_çimen": "Güney çimen. Zeliha Teyze'nin çayı buradan kokuyor.",
        "bati_yolu": "Batı yolu. Demirci'nin çekiç sesi buraya kadar geliyor.",
    },

    "zeliha_cay": {
        "speaker": "ZELİHA TEYZEsuppose",
        "lines": [
            "Çay var. Al.",
            "Konuşmak istersen buradayım.",
            "İstemezsen de olur. Çay gene de bedelava.",
        ],
    },

    "gece_sesi": {
        "speaker": "GECE",
        "lines": [
            "Geç vakit oldu.",
            "Köy uyuyor.",
            "THE ALGO uyumuyor.",
            "Sen de uyumuyorsun.",
            "İkiniz de aynı gecedesiniz.",
        ],
    },
}

ENCOUNTER_INTRO_DIALOGUES = {
    "Ağlak Varlık": [
        "Bir varlık önünü kesiyor!",
        "Ağlıyor mu? Saldırıyor mu? İkisi de? Bune Oglum???",
    ],
    "Yanlış Yer Mantarı": [
        "Yanlış yerde bir mantar!",
        "Hiçbir şeyi bilerek yapmıyor gibi görünüyor.",
    ],
    "Panik Ruhu": [
        "Bir ruh görünüyor!",
        "Senden mi korkuyor, yoksa sen mi ondan korkuyorsun?",
    ],
    "Kafakarışık Bürokrat": [
        "Gözlüklü, evraklı biri belirdi!",
        "Elindeki klasörde 200 sayfalık bir 'karşılaşma formu' var.",
    ],
    "Nostalji Canavarı": [
        "Puslu, ağır bir his yayılıyor...",
        "Nostalji Canavarı! 'Eskiden böyle değildi' diyor sürekli.",
    ],
    "Veri Hırsızı": [
        "Birisi gizlice yaklaşıyor!",
        "Veri Hırsızı! Tam bir veri çalmak üzere... ama çok üzgün görünüyor.",
    ],
}

ENDING_SLIDES = {
    "iyi_son": [
        {"text": "{} köye döndü.",          "bg": (5, 15, 5),    "col": (60, 220, 220)},
        {"text": "Duman... hatırladı.",      "bg": (5, 5, 15),    "col": (180, 180, 255)},
        {"text": "İlk kez özür diledi.",     "bg": (5, 5, 20),    "col": (150, 150, 220)},
        {"text": "THE ALGO yeniden başladı.","bg": (5, 5, 20),    "col": (100, 200, 255)},
        {"text": "Tilki Fıstık kurtarıldı.","bg": (10, 20, 10),  "col": (50, 200, 80)},
        {"text": "Rıdvan Efendi ağladı.",    "bg": (5, 15, 5),    "col": (255, 255, 255)},
        {"text": "(Sevinçten tabii.)",        "bg": (5, 15, 5),    "col": (100, 100, 100)},
        {"text": "Ayşe Harika harika oldu, cidden.", "bg": (15, 5, 15), "col": (255, 120, 180)},
        {"text": "Hüsrev çekicini buldu.",   "bg": (20, 15, 5),   "col": (240, 140, 40)},
        {"text": "THE ALGO öğrendi.",        "bg": (5, 5, 15),    "col": (100, 200, 255)},
        {"text": "Belki hep öğrenebilir.",   "bg": (0, 5, 10),    "col": (150, 220, 255)},
        {"text": "Zeliha çay demliyor.",     "bg": (10, 5, 0),    "col": (200, 150, 80)},
        {"text": "~ GERÇEK İYİ SON ~",      "bg": (0, 0, 0),     "col": (255, 220, 60)},
    ],
    "kotu_son": [
        {"text": "{} ormanı geçti.",         "bg": (15, 5, 5),    "col": (220, 50, 50)},
        {"text": "{} varlık yok edildi.",    "bg": (20, 5, 5),    "col": (180, 80, 80)},
        {"text": "Duman güldü.",             "bg": (10, 0, 0),    "col": (240, 140, 40)},
        {"text": "THE ALGO büyüdü.",         "bg": (5, 0, 10),    "col": (160, 60, 200)},
        {"text": "Köy boşaldı.",             "bg": (5, 0, 0),     "col": (150, 80, 80)},
        {"text": "Rıdvan Efendi gitmişti.",  "bg": (5, 0, 0),     "col": (100, 60, 60)},
        {"text": "Zeliha çayını döktü.",     "bg": (8, 3, 0),     "col": (120, 70, 50)},
        {"text": "Hüsrev dükkânı kapattı.",  "bg": (5, 2, 0),     "col": (100, 60, 40)},
        {"text": "Fıstık... bilinmiyor.",    "bg": (0, 0, 0),     "col": (120, 80, 80)},
        {"text": "Belki başka bir yol vardı?","bg": (0, 0, 0),    "col": (100, 80, 80)},
        {"text": "~ KÖTÜ SON ~",            "bg": (0, 0, 0),     "col": (120, 20, 20)},
    ],
    "notr_son": [
        {"text": "{} durdu.",                "bg": (10, 10, 10),  "col": (180, 180, 180)},
        {"text": "Ne iyi ne kötü.",          "bg": (10, 10, 10),  "col": (150, 150, 150)},
        {"text": "THE ALGO hâlâ orada.",     "bg": (5, 5, 15),    "col": (100, 100, 200)},
        {"text": "Duman hâlâ orada.",        "bg": (10, 5, 5),    "col": (180, 100, 100)},
        {"text": "Köy hâlâ orada.",          "bg": (5, 10, 5),    "col": (100, 180, 100)},
        {"text": "Hikaye devam ediyor.",     "bg": (8, 8, 8),     "col": (200, 200, 200)},
        {"text": "~ DEVAM EDECEk ~",        "bg": (0, 0, 0),     "col": (200, 200, 60)},
    ],
}
