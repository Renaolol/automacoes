import requests
import dearpygui.dearpygui as dpg
dpg.create_context()

def soma_valores(sender,app_data):
    print(sender)
    return x+y

calc = False
with dpg.window(tag="primary window"):
    dpg.add_button(label="Primeiro botão")
    with dpg.group(horizontal=True):
        dpg.add_button(label="DCTFWEB")
        dpg.add_button(label="Segundo botão",callback=soma_valores)

    x=dpg.add_input_int(label="Valor de X")
    y=dpg.add_input_int(label= "Valor de Y")
    calcula = soma_valores(x,y)
    dpg.add_text(f"Soma dos valores é {calcula}")

dpg.create_viewport()
dpg.set_primary_window("primary window",True)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()