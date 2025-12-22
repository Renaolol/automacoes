import pyautogui
import pymsgbox
from pathlib import Path
# print('Press Ctrl-C to quit.')
# try:
#     while True:
#         x, y = pyautogui.position()
#         positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
#         print(positionStr, end='')
#         print('\b' * len(positionStr), end='', flush=True)
# except KeyboardInterrupt:
#     print('\n')
# pyautogui.sleep(2)
def abre_dominio():
    pasta_atual = Path(__file__).parent
    pasta_imagens = pasta_atual / 'imagens'
    pasta_dominio = pasta_imagens / 'pasta_dominio.png'
    dominio_icone = pasta_imagens / 'dominio_escrita_fiscal.png'
    senha_dominio = pasta_imagens / 'senha_dominio.png'
    ok_dominio = pasta_imagens / 'ok.png'
    if pasta_dominio.is_file():
        pasta_dominio_mover = pyautogui.locateOnScreen(str(pasta_dominio))
        pyautogui.moveTo(pasta_dominio_mover,duration=1)
        pyautogui.doubleClick()
        pyautogui.sleep(1)
        if dominio_icone.is_file():
            icone_dominio_mover = pyautogui.locateOnScreen(str(dominio_icone))
            pyautogui.moveTo(icone_dominio_mover,duration=1)
            pyautogui.doubleClick()
            pyautogui.sleep(2)
            while True:
                print("Aguardando tela de login...")
                pyautogui.sleep(2)
                try:
                    pyautogui.locateOnScreen(str(senha_dominio))
                    break
                except:
                    print("Reprocessando...")
                    pass
            senha_mover = pyautogui.locateOnScreen(str(senha_dominio))
            pyautogui.moveTo(senha_mover,duration=1)
            pyautogui.click()
            pyautogui.write("RS",interval=0.01)
            ok_mover = pyautogui.locateOnScreen(str(ok_dominio))
            pyautogui.moveTo(ok_mover,duration=1)
            pyautogui.click()
    else:
        print('Erro, pasta não encontrada')
    return
pymsgbox.alert(text="teste",title="teste de título")
abre_dominio()