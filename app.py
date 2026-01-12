import dearpygui.dearpygui as dpg
dpg.create_context()
dpg.create_viewport(title="Leitor XML desktop")

dpg.add_file_dialog(directory_selector=True)

with dpg.window(tag="Leitor XML desktop janela"):
    dpg.add_text("Selecione os XML a serem lidos")
    dpg.add_button(label="Fechar",callback=dpg.destroy_context)
    dpg.add_button(label="Select files")

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Leitor XML desktop janela", True)
dpg.start_dearpygui()
dpg.destroy_context()