# St3g4n0 — стеганография в изображениях и аудио

Здесь показаны классические и современные методы сокрытия информации в данных: изображениях и аудиофайлах.

---

## Структура проекта

```
input_data/         # Исходные данные
├── big_secret.txt  # Крупное текстовое сообщение
├── small_secret.txt # Короткое сообщение для тестов
├── img.png         # Оригинальное цветное изображение
├── gs_img.png      # Ч/б изображение (градации серого)
├── KINO.wav        # Оригинальный аудиофайл
├── KINO_FULL.wav   # Длинная версия аудиофайла
│
output_data/        # Результаты работы алгоритмов
└── gan_out.png     # Пример результата GAN-встраивания
│
src/                # Исходный код методов
├── st3g4n0_lsb_img.py   # LSB-встраивание в изображение
├── st3g4n0_lsb_snd.py   # LSB-встраивание в аудио
├── st3g4n0_dct_img.py   # Частотный метод (DCT) для изображений
├── st3g4n0_gan_img.py   # Нейросетевой (GAN) метод
└── compare.py           # Побайтовое сравнение и тепловая карта различий
```

---

## Подготовка к запуску

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## 🧩 Методы

| Файл | Метод | Описание |
|------|--------|-----------|
| `st3g4n0_lsb_img.py` | **LSB Matching** | Пространственное внедрение в младшие биты пикселей |
| `st3g4n0_dct_img.py` | **DCT-встраивание** | Изменение среднечастотных коэффициентов блоков 8×8 |
| `st3g4n0_lsb_snd.py` | **LSB Audio** | Встраивание в звуковые сэмплы WAV |
| `st3g4n0_gan_img.py` | **GAN-based Steganography** | Встраивание сообщения с помощью генеративной модели |
| `compare.py` | **Diff-анализ** | Визуализация различий и тепловая карта изменений |

---

## Примеры использования

### Встраивание текста в изображение (LSB)
```bash
python src/st3g4n0_lsb_img.py encode -i input_data/img.png -o output_data/stego.png -m input_data/small_secret.txt
```

Извлечение:
```bash
python src/st3g4n0_lsb_img.py decode -i output_data/stego.png -o output_data/result.txt
```

---

### Скрытие данных через DCT
```bash
python src/st3g4n0_dct_img.py encode -i input_data/img.png -o output_data/stego_dct.png -m input_data/small_secret.txt
python src/st3g4n0_dct_img.py decode -i output_data/stego_dct.png -o output_data/result.txt
```

---

### Встраивание в аудио
```bash
python src/st3g4n0_lsb_snd.py encode -i input_data/KINO.wav -o output_data/stego.wav -m input_data/small_secret.txt
python src/st3g4n0_lsb_snd.py decode -i output_data/stego.wav -o output_data/result.txt
```

---

### Встраивание c помощью GAN (энкодинг + декодинг одновременно)
```bash
python src/st3g4n0_gan_img.py
```
---

### Анализ изменений
```bash
python src/compare.py
```

Покажет:
- процент изменённых пикселей и бит;
- карту различий;
- тепловую карту активности изменений.