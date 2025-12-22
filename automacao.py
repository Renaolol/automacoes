import pyautogui
import pymsgbox
from pathlib import Path
pyautogui.FailSafeException
def abre_dominio():
    pasta_atual = Path(__file__).parent
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


pasta_atual = Path(__file__).parent
pasta_imagens = pasta_atual / 'imagens'
dominio_barra = pasta_imagens /'dominio_barra_tarefas.png'
try:
    dominio_barra_identificacao = pyautogui.locateOnScreen(str(dominio_barra),confidence=0.9)
except:
    dominio_barra_identificacao=False
if dominio_barra_identificacao:
    print("Domínio já está aberta...")
else:
    abre_dominio()