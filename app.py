import dearpygui.dearpygui as dpg
dpg.create_context()
dpg.create_viewport(title="Leitor XML desktop")
dpg.add_file_dialog(directory_selector=True)

def callback_files(sender, app_data):
    print('Ok was clicked')
    print(f"Sender:{sender}")
    print(f'App Data: {app_data}')

def soma_itens(sender,app_data,user_data):
    for x in user_data:
        print(x)

with dpg.window(tag="Leitor XML desktop janela"):
    dpg.add_text("Selecione os XML a serem lidos")
    dpg.add_button(label="Fechar",callback=dpg.destroy_context)
    dpg.add_button(label="somar",callback=soma_itens,user_data=[1,2])


dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Leitor XML desktop janela", True)
dpg.start_dearpygui()
dpg.destroy_context()