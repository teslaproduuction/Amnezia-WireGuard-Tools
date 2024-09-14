# Amnezia WireGuard Tools

Amnezia WireGuard Tools — это мощный инструмент для работы с конфигурациями WireGuard и их преобразования в формат Amnezia VPN. Программа также поддерживает генерацию конфигураций Cloudflare WARP, создание QR-кодов для удобного импорта настроек и настройку SOCKS5 прокси-серверов.

![WG_to_Amnesia_logo](https://github.com/user-attachments/assets/ede429a4-8a0d-46ad-b3d9-bc7e2bede29e)


## Основные функции

- Преобразование конфигураций WireGuard в формат Amnezia
- Генерация конфигураций Cloudflare WARP
- Создание QR-кодов для быстрого импорта конфигураций
- Добавление случайного ListenPort в конфигурации
- Настройка и сохранение параметров SOCKS5 прокси
- Отправка UDP сообщений с параметрами из конфигурации
- Поддержка тёмной темы интерфейса для удобства работы
- Конвертация конфигураций в JSON формат

## Как использовать
**Скачивание скомпилированной версии:**

Помимо возможности использования исходного кода приложения прямо из репозитория, предоставляем возможность скачивания готовой, скомпилированной версии приложения. Это позволяет пользователям, не знакомым с процессом компиляции Python-приложений, быстро получить и использовать приложение на своих устройствах.

Для скачивания скомпилированной версии приложения, следуйте этим шагам:

1. Перейдите на страницу "Releases" (Релизы) в репозитории на GitHub или воспользуйтесь ссылкой [релиз](https://github.com/teslaproduuction/Amnezia-WireGuard-Tools/releases/).
2. Найдите последний релиз, в котором доступна скомпилированная версия приложения.
3. В разделе "Assets" (Ресурсы) найдите и скачайте файл с расширением, соответствующим вашей операционной системе (например, .exe для Windows, .app для macOS (будет позже), или .tar.gz для Linux).
4. После завершения загрузки, выполните установку или запускайте приложение согласно инструкциям для вашей операционной системы.

   
**Установка:**   
1. Убедитесь, что у вас установлен Python версии 3.7 или выше.
2. Клонируйте репозиторий:
   ```
   git clone https://github.com/teslaproduuction/Amnezia-WireGuard-Tools.git
   cd Amnezia-WireGuard-Tools
   ```
3. Установите зависимости:
   ```
   pip install -r requirements.txt
   ```

## Использование

1. Запустите программу:
   ```
   python ui.py
   ```
2. Загрузите конфигурационный файл WireGuard (.conf) через интерфейс программы.
3. Используйте кнопки на панели инструментов для выполнения различных операций с конфигурацией.

## Скриншоты

![image](https://github.com/user-attachments/assets/22c7f763-f6c3-42e7-b336-a1e065579c3d)
![image](https://github.com/user-attachments/assets/d5ea5b2e-5e7c-4920-b138-c2f4c83cf153)
![image](https://github.com/user-attachments/assets/c0c669e2-f60e-489b-9488-c0b4337d4eaa)


## История изменений

- **Версия 1.0** (14 сентября 2024):
  - Проведена значительная переработка программы для улучшения функционала и интерфейса.
  - Добавлена поддержка интеграции с Amnezia и Hiddify.
  - Оптимизирован пользовательский интерфейс.

- **Версия 0.9** (8 сентября 2024):
  - Запуск тестирования функционала программы и финальная настройка интерфейса.
  - Исправлены ошибки в отображении QR-кодов.

- **Версия 0.8** (29 августа 2024):
  - Начало разработки программы, добавлен функционал для работы с конфигурациями WireGuard и Cloudflare WARP.

## Используемые библиотеки и ресурсы

- [NiceGUI](https://github.com/zauberzeug/nicegui) - для создания интерфейса программы
- [Cloudflare WARP WireGuard Client](https://github.com/ViRb3/cloudflare-warp-wireguard-client) - для генерации конфигураций Cloudflare WARP
- [AmneziaWG for Windows](https://github.com/amnezia-vpn/amneziawg-windows-client) - для работы с конфигурациями Amnezia
- [Hiddify-next](https://github.com/hiddify/hiddify-next) - для работы с конфигурациями json формата

## Лицензия

Этот проект распространяется по лицензии MIT. Подробности можно найти в файле LICENSE.
