# st3g4n0 — стеганография в изображениях и аудио

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

## Методы

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

Для примера.
1. Картинка ДО:
<img width="3840" height="2160" alt="img" src="https://github.com/user-attachments/assets/c474e738-a401-4379-8429-e5f73eb26fb3" />


2. Картинка ПОСЛЕ:
<img width="3840" height="2160" alt="out" src="https://github.com/user-attachments/assets/636c3759-3d8e-42ce-94a8-5d9c5717fd87" />

3. Встроенное и декодированные сообщение: Ask, and it shall be given you; seek, and ye shall find; knock, and it shall be opened unto you.

---

### Скрытие данных через DCT
```bash
python src/st3g4n0_dct_img.py encode -i input_data/img.png -o output_data/stego_dct.png -m input_data/small_secret.txt
python src/st3g4n0_dct_img.py decode -i output_data/stego_dct.png -o output_data/result.txt
```

Для примера.
1. Картинка ДО:
<img width="3840" height="2160" alt="gs_img" src="https://github.com/user-attachments/assets/dda06e6f-f226-471a-8952-d8abc5533753" />

2. Картинка ПОСЛЕ:
<img width="3840" height="2160" alt="out" src="https://github.com/user-attachments/assets/a0b4dc51-b7be-4c58-8a60-80265f74374c" />

3. Встроенное и декодированные сообщение можно посмотреть в файле big_secret.txt.
4. Различия в ДКП картинки до и после встравания сообщения:
  - <img width="3840" height="2160" alt="out_dct_before" src="https://github.com/user-attachments/assets/5c1d9037-44fd-4f57-b995-96177d8ea044" />
  - <img width="3840" height="2160" alt="out_dct_after" src="https://github.com/user-attachments/assets/6a9bf481-f526-4362-8b73-c825e9a78494" />
  - <img width="3840" height="2160" alt="out_dct_delta" src="https://github.com/user-attachments/assets/dbe311bd-1461-4239-94f6-f4be4f4aa07b" />
  
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
