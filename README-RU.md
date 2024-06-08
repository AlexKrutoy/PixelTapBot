[![Static Badge](https://img.shields.io/badge/Telegram-Channel-Link?style=for-the-badge&logo=Telegram&logoColor=white&logoSize=auto&color=blue)](https://t.me/hidden_coding)

[![Static Badge](https://img.shields.io/badge/Telegram-Chat-yes?style=for-the-badge&logo=Telegram&logoColor=white&logoSize=auto&color=blue)](https://t.me/hidden_codding_chat)

[![Static Badge](https://img.shields.io/badge/Telegram-Bot%20Link-Link?style=for-the-badge&logo=Telegram&logoColor=white&logoSize=auto&color=blue)](https://t.me/pixelversexyzbot?start=737844465)

<img src="https://github.com/AlexKrutoy/PixelTapBot/assets/65369825/bb62126e-269a-46cd-984b-33b8b80462c6" width="695" height="425"/>

<img src="https://github.com/AlexKrutoy/PixelTapBot/assets/65369825/9e7de3f0-358a-4240-899e-43b4c3dedeb9" width="695" height="425"/>

## Рекомендация перед использованием

# 🔥🔥 Используйте PYTHON 3.10 🔥🔥

> 🇪🇳 README in english available [here](README.md)

## Функционал  
| Функционал                                                     | Поддерживается  |
|----------------------------------------------------------------|:----------------:|
| Многопоточность                                                |        ✅        |
| Привязка прокси к сессии                                       |        ✅        |
| Автоматический сбор монет                                      |        ✅        |
| Автоматическое улучшение всех питомцев                         |        ✅        |
| Автоматическая покупка нового питомца                          |        ✅        |
| Поддержка tdata / pyrogram .session / telethon .session        |        ✅        |


## [Настройки](https://github.com/AlexKrutoy/PixelTapBot/blob/main/.env-example/)
| Настройка                | Описание                                                                                    |
|--------------------------|:---------------------------------------------------------------------------------------------:|
| **API_ID / API_HASH**    | Данные платформы, с которой запускать сессию Telegram (сток - Android)                      |
| **AUTO_CLAIM**           | Переменная для автоматического сбора монет (по умолчанию - True)                            |                                
| **AUTO_UPGRADE**         | Переменная для автоматического улучшения питомца по имени (по умолчанию - True)             |
| **AUTO_BUY**             | Переменная для автоматической покупки новых питомцев (по умолчанию - False)                 |
| **USE_PROXY_FROM_FILE**  | Использовать-ли прокси из файла `bot/config/proxies.txt` (True / False)                     |

## Быстрый старт 📚

Для быстрой установки и последующего запуска - запустите файл run.bat на Windows или run.sh на Линукс

## Предварительные условия
Прежде чем начать, убедитесь, что у вас установлено следующее:
- [Python](https://www.python.org/downloads/) **версии 3.10**

## Получение API ключей
1. Перейдите на сайт [my.telegram.org](https://my.telegram.org) и войдите в систему, используя свой номер телефона.
2. Выберите **"API development tools"** и заполните форму для регистрации нового приложения.
3. Запишите `API_ID` и `API_HASH` в файле `.env`, предоставленные после регистрации вашего приложения.

## Установка
Вы можете скачать [**Репозиторий**](https://github.com/AlexKrutoy/PixelTapBot) клонированием на вашу систему и установкой необходимых зависимостей:
```shell
git clone https://github.com/AlexKrutoy/PixelTapBot.git
cd PixelTapBot
```

Затем для автоматической установки введите:

Windows:
```shell
run.bat
```

Linux:
```shell
run.sh
```

# Linux ручная установка
```shell
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
cp .env-example .env
nano .env  # Здесь вы обязательно должны указать ваши API_ID и API_HASH , остальное берется по умолчанию
python3 main.py
```

Также для быстрого запуска вы можете использовать аргументы, например:
```shell
~/PixelTapBot >>> python3 main.py --action (1/2)
# Or
~/PixelTapBot >>> python3 main.py -a (1/2)

# 1 - Запускает кликер
# 2 - Создает сессию
```


# Windows ручная установка
```shell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env-example .env
# Указываете ваши API_ID и API_HASH, остальное берется по умолчанию
python main.py
```

Также для быстрого запуска вы можете использовать аргументы, например:
```shell
~/PixelTapBot >>> python main.py --action (1/2)
# Или
~/PixelTapBot >>> python main.py -a (1/2)

# 1 - Запускает кликер
# 2 - Создает сессию
```




### Контакты

Для поддержки или вопросов, свяжитесь со мной в Telegram: [@UNKNXWNPLXYA](https://t.me/UNKNXWNPLXYA)