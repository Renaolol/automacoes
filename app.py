import dearpygui.dearpygui as dpg
dpg.create_context()
dpg.create_viewport(title="Leitor XML desktop")
dpg.add_file_dialog(directory_selector=True)

def callback_files(sender, app_data):
    print('Ok was clicked')
    print(f"Sender:{sender}")
    print(f'App Data: {app_data}')

with dpg.file_dialog(directory_selector=False, show=False, callback=callback_files,label="Selecionar xmls", id="select_files", width=700 ,height=400):
    dpg.add_file_extension(".*")
    dpg.add_file_extension(".xml", color=(255, 0, 255, 255), custom_text="[Xml]")

with dpg.window(tag="Leitor XML desktop janela"):
    dpg.add_text("Selecione os XML a serem lidos")
    dpg.add_button(label="Fechar",callback=dpg.destroy_context)
    dpg.add_button(label="Selecionar XMLS",tag="Select files",callback=lambda: dpg.show_item("select_files"))


dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Leitor XML desktop janela", True)
dpg.start_dearpygui()
dpg.destroy_context()