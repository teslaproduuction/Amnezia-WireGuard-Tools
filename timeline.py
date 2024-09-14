from nicegui import ui
import webbrowser

def show_timeline():
    with ui.dialog() as dialog, ui.card():
        ui.label('О программе').classes('text-h5 q-mb-md')
        with ui.timeline(side='right'):
            ui.timeline_entry(
                'Разработка программы для исследования протоколов и включая преобразование конфигураций WireGuard в формат Amnezia, генерацию конфигураций Cloudflare WARP, создание QR-кодов и настройку прокси.',
                title='Начало разработки',
                subtitle='Август 29, 2024')
            ui.timeline_entry(
                'Запуск тестирования функционала программы и финальная настройка интерфейса для улучшения пользовательского опыта.',
                title='Тестирование и настройка интерфейса',
                subtitle='Сентябрь 8, 2024')
            ui.timeline_entry(
                'Проведена большая переработка программы для улучшения функционала и интерфейса.',
                title='Релиз версии 1.0',
                subtitle='Сентябрь 14, 2024',
                icon='rocket')

        with ui.row().classes('flex w-full h-full justify-between items-center flex-nowrap pr-4 pl-2'):
            with ui.row().classes('flex w-full h-full justify-end items-center flex-nowrap'):
                    # Иконка Cloudflare
                    with ui.link(target='https://github.com/ViRb3/cloudflare-warp-wireguard-client', new_tab=True).tooltip('Репозиторий генератора CloudFlare WARP'):
                        ui.image('https://www.svgrepo.com/show/353564/cloudflare.svg').classes('w-12 h-12')

                    # Иконка Telegram
                    with ui.link(target='https://t.me/hyouka_hyouka', new_tab=True).tooltip('Тгк разработчика визуальной части'):
                        ui.image('https://upload.wikimedia.org/wikipedia/commons/8/82/Telegram_logo.svg').classes('w-12 h-12')

                    # Иконка GitHub
                    with ui.link(target='https://github.com/your_github_link', new_tab=True).tooltip('Репозиторий проекта'):
                        ui.image('https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png').classes('w-12 h-12')

                    # Иконка Amnezia
                    with ui.link(target='https://github.com/amnezia-vpn/amneziawg-windows-client?ysclid=m122et7lbq370461163', new_tab=True).tooltip('AmneziaWG for Windows'):
                        ui.image('https://docs.amnezia.org/ru/img/a-logo.png').classes('w-12 h-12')

                    with ui.link(target='https://github.com/hiddify/hiddify-next', new_tab=True).tooltip('Hiddify-next'):
                        ui.image('https://raw.githubusercontent.com/hiddify/hiddify-next/main/assets/images/logo.svg').classes('w-12 h-12')

            with ui.row().classes('flex w-full h-full justify-between items-center flex-nowrap pr-4 pl-2'):
                with ui.row().classes('flex w-full h-full justify-end items-center flex-nowrap'):
                    ui.button('Закрыть', on_click=dialog.close).tooltip('Закрыть раздел: О программе')


    dialog.open()
