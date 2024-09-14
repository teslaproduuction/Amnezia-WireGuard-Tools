# ui.py
import asyncio

from nicegui import ui, events
import webview
# from nicegui.native import native_mode

webview.settings['ALLOW_DOWNLOADS'] = True
from timeline import show_timeline
from main import *
from warp import *
import sys



@ui.page('/')
def main():
    def on_switch(e):
        if e.value:
            dark_mode.enable()
            code_editor.theme = 'monokai'
        else:
            dark_mode.disable()
            code_editor.theme = 'basicLight'

    dark_mode = ui.dark_mode()

    async def on_upload(e: events.UploadEventArguments):
        content = e.content.read().decode('utf-8')
        code_editor.value = load_config(content)

    def on_convert():
        if code_editor.value:
            converted = convert_to_amnezia(code_editor.value)
            code_editor.value = converted
            ui.notify('Конвертация завершена', type='success')
        else:
            ui.notify('Пожалуйста, загрузите конфигурацию перед конвертацией', type='warning')

    def on_add_listen_port():
        if code_editor.value:
            updated_config = add_random_listen_port(code_editor.value)
            code_editor.value = updated_config
        else:
            ui.notify('Пожалуйста, загрузите конфигурацию перед добавлением порта', type='warning')

    with ui.dialog() as qr_dialog:
        qr_image = ui.image().classes('w-64 h-64')

    def on_generate_qr_code():
        if code_editor.value:
            qr_image_data = generate_qr_code(code_editor.value)
            qr_image.source = f'data:image/png;base64,{qr_image_data}'
            qr_dialog.open()
        else:
            ui.notify('Пожалуйста, загрузите конфигурацию перед генерацией QR-кода', type='warning')

    with ui.dialog() as loading_dialog:
        ui.spinner(size='lg')
        ui.label('Создание WARP конфигурации ...')

    async def generate_warp_config_with_loading():
        loading_dialog.open()
        try:
            wgcf_config = await asyncio.to_thread(generate_wgcf_config)
            if wgcf_config:
                code_editor.value = wgcf_config
                ui.notify('WARP конфигурация сгенерирована', type='success')
            else:
                ui.notify('Не удалось сгенерировать WARP конфигурацию', type='error')
        finally:
            loading_dialog.close()

    def show_proxy_dialog():
        with ui.dialog() as proxy_dialog, ui.card():
            ui.label('SOCKS5 Proxy')
            host_input = ui.input('Хост', value=USER_SOCKS5_PROXY['host']).tooltip(
                    "Ip адрес или доменное имя")
            port_input = ui.input('Порт', value=str(USER_SOCKS5_PROXY['port'])).tooltip(
                    "порт сервера")
            username_input = ui.input('Логин', value=USER_SOCKS5_PROXY['username']).tooltip(
                    "Логин (опционально)")
            password_input = ui.input('Пароль', value=USER_SOCKS5_PROXY['password']).tooltip(
                    "Пароль (опционально)")

            def update_proxy_settings():
                USER_SOCKS5_PROXY['host'] = host_input.value
                USER_SOCKS5_PROXY['port'] = port_input.value
                USER_SOCKS5_PROXY['username'] = username_input.value
                USER_SOCKS5_PROXY['password'] = password_input.value
                save_user_proxy_settings(USER_SOCKS5_PROXY)
                proxy_dialog.close()
                ui.notify('Настройки прокси сохранены', type='success')

            ui.button('Сохранить', on_click=update_proxy_settings).tooltip(
                    "Заменит стандартный прокси и создаст json файл")

        proxy_dialog.open()

    def on_convert_to_json():
        if code_editor.value:
            json_config = convert_to_json(code_editor.value)
            if json_config:
                code_editor.value = json_config
                ui.notify('Конвертация в JSON завершена', type='success')
            else:
                ui.notify('Не удалось конвертировать конфигурацию в JSON', type='error')
        else:
            ui.notify('Пожалуйста, загрузите конфигурацию перед конвертацией', type='warning')

    def copy_to_clipboard():
        if code_editor.value:
            ui.run_javascript(f'navigator.clipboard.writeText(`{code_editor.value}`)')
            ui.notify('Содержимое скопировано в буфер обмена', type='success')
        else:
            ui.notify('Нет содержимого для копирования', type='warning')

    with ui.dialog().classes('flex w-full rounded-lg') as dialog, ui.card().classes('flex w-full rounded-lg'):
        ui.label('Сохранить как...').classes('flex w-full rounded-lg').tailwind.font_weight('bold').font_size('lg')
        with ui.column().classes('flex w-full'):
            ui.label('Имя файла:')
            filename = ui.input(' ', placeholder='Введите имя файла...').props('outlined dense').classes(
                'flex w-full h-25')

        def save():
            if code_editor.value:
                file_content = code_editor.value.encode('utf-8')

                ui.download(src=file_content, filename=f"{filename.value}.conf")
                dialog.close()
            else:
                ui.notify('Нет содержимого для сохранения', type='warning')

        ui.button('Сохранить', on_click=save).classes('w-full bg-green-5 p-2 shadow-lg rounded-lg').style(
            'background-color: #70d777 !important').tooltip("Сохранить конфигурацию в файл .conf")
        ui.button('Закрыть', on_click=dialog.close).classes('w-full bg-#ededed p-2 shadow-lg rounded-lg').style(
            'background-color: #f2546c !important').tooltip("Отменить сохранение конфигурации в файл")

    with ui.column().classes('flex w-full h-full'):
        with ui.row().classes('flex w-full justify-between items-start flex-nowrap'):
            ui.image('https://i.yapx.cc/X8ZR6.png').classes('w-1/2')
            with ui.column().classes('flex w-full justify-between items-center pl-5'):
                ui.label('Amnezia WireGuard Tools').classes('flex w-full pt-10').tailwind.font_weight(
                    'bold').font_size('4xl')
                with ui.row().classes('flex w-75 justify-start'):
                    ui.upload(on_upload=on_upload, auto_upload=True, label='Загрузить .conf файл', max_files=1) \
                        .props('accept=.conf color=teal').classes('flex w-4/5 shadow-lg rounded-lg')

                    with ui.button_group().classes('flex flex-nowrap rounded-lg'):
                        ui.button('Amnezia', on_click=on_convert).props('icon=recycling').classes(
                            'bg-blue-6 p-2 shadow-lg').tooltip("Преобразовать WireGuard в Amnezia WG")
                        ui.button('ListenPort', on_click=on_add_listen_port).props('icon=add_circle_outline').classes(
                            'bg-blue-6 p-2 shadow-lg').tooltip("Добавить ListenPort в конфиг")
                        ui.button('UDP', on_click=lambda: send_udp_message(code_editor.value)).props(
                            'icon=send').classes('bg-blue-6 p-2 shadow-lg').tooltip("Отправить UDP пакет на адрес из конфига")
                        ui.button('WARP', on_click=generate_warp_config_with_loading).props('icon=rocket').classes(
                            'bg-blue-6 p-2 shadow-lg').tooltip("Сгенерировать конфиг cloudflare WARP")
                        ui.button('JSON', on_click=on_convert_to_json).props('icon=code').classes(
                            'bg-blue-6 p-2 shadow-lg').tooltip("Преобразовать конфиг в json формат")
                        ui.button('PROXY', on_click=show_proxy_dialog).props('icon=vpn_lock').classes(
                            'bg-blue-6 p-2 shadow-lg').tooltip("Настройки прокси для генерации  WARP")

        with ui.column().classes('flex w-full justify-center items-start'):
            ui.label('Редактор конфигурации:').classes('flex w-full self-start pl-3 pr-3 pt-3').style(
                'margin-bottom: -10px').tailwind.font_weight('normal') \
                .font_size('lg')
            code_editor = ui.codemirror('', language='ini').classes('w-full h-64-full pl-3 pr-3 pb-3')

        with ui.row().classes('flex w-full h-full justify-between items-center flex-nowrap pr-4 pl-2'):
            switcher = ui.switch('Тёмная тема', on_change=on_switch).props('color=white').classes(
                'w-50').tooltip("Переключатель темы").tailwind.font_weight('bold')
            with ui.row().classes('flex w-full h-full justify-end items-center flex-nowrap'):
                ui.button('Сохранить', on_click=dialog.open).props('icon=save').classes(
                    'bg-blue-6 p-2 shadow-lg rounded-lg').style('background-color: #70d777 !important').tooltip(
                    "Сохранить конфиг в файл")
                ui.button('Копировать', on_click=copy_to_clipboard).props('icon=content_copy').classes(
                    'bg-orange-6 p-2 shadow-lg rounded-lg').tooltip(
                    "Скопировать конфиг в буфер обмена")
                ui.button('QR-Код', on_click=on_generate_qr_code).props('icon=qr_code').classes(
                    'bg-black p-2 shadow-lg rounded-lg').tooltip(
                    "Генератор QR кода")
                ui.button('О программе', on_click=show_timeline).props('icon=timeline').classes(
                    'bg-purple-6 p-2 shadow-lg rounded-lg').tooltip(
                    "Информация о программе и использованных технологиях")


if __name__ == "__main__":
    main()
    ui.run(native=True, reload=False, window_size=(1100, 750), title='Amnezia WireGuard Tools')

