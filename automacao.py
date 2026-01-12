import pyautogui
import pymsgbox
from pathlib import Path
import dearpygui.dearpygui as dpg
dpg.create_context()

pyautogui.FailSafeException
def abre_dominio():
    pasta_atual = Path(r"C:\Users\gcont\OneDrive\Documentos\GitHub\automacoes")
    pasta_imagens = pasta_atual / 'imagens'
    pasta_dominio = pasta_imagens / 'pasta_dominio.png'
    dominio_icone = pasta_imagens / 'dominio_escrita_fiscal.png'
    senha_dominio = pasta_imagens / 'senha_dominio.png'
    ok_dominio = pasta_imagens / 'ok.png'
    if pasta_dominio.is_file():
        pasta_dominio_mover = pyautogui.locateOnScreen(str(pasta_dominio),confidence=0.9)
        pyautogui.moveTo(pasta_dominio_mover,duration=1)
        pyautogui.doubleClick()
        pyautogui.sleep(1)
        if dominio_icone.is_file():
            icone_dominio_mover = pyautogui.locateOnScreen(str(dominio_icone),confidence=0.9)
            pyautogui.moveTo(icone_dominio_mover,duration=1)
            pyautogui.doubleClick()
            pyautogui.sleep(2)
            while True:
                print("Aguardando tela de login...")
                try:
                    pyautogui.locateOnScreen(str(senha_dominio),confidence=0.9)
                    break
                except:
                    print("Reprocessando...")
                    pyautogui.sleep(1)
                    pass
            senha_mover = pyautogui.locateOnScreen(str(senha_dominio),confidence=0.9)
            pyautogui.moveTo(senha_mover,duration=1)
            pyautogui.click()
            pyautogui.write("RS",interval=0.01)
            ok_mover = pyautogui.locateOnScreen(str(ok_dominio),confidence=0.9)
            pyautogui.moveTo(ok_mover,duration=1)
            pyautogui.click()
    else:
        print('Erro, pasta não encontrada')
    return

with dpg.window(tag="Abrir dominio"):
    dpg.add_text("Tela de testes para futuras automações.")
    dpg.add_button(label="Abrir",callback=abre_dominio)


dpg.create_viewport(title='Custom Title', width=600, height=300)
dpg.set_viewport_large_icon('icone.ico')
dpg.set_viewport_small_icon('icone.ico')
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Abrir dominio",True)
dpg.start_dearpygui()
dpg.destroy_context()

