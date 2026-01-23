import psutil
import platform
import cpuinfo
import wmi
import dearpygui.dearpygui as dpg


def salvar(sender, app_data,user_data):
    print(user_data)

dpg.create_context()

c = wmi.WMI()
for board in c.Win32_BaseBoard():
    marca_mb = board.Manufacturer
    modelo_mb = board.Product
    serie_mb = board.SerialNumber

for video in c.Win32_VideoController():
    video = video.Description
#infos do CPU
#Nome do Computador
pc_name = platform.node()
#modelo do Processador ["brand_raw"]
processor = cpuinfo.get_cpu_info()
modelo_processador = processor["brand_raw"]

#nucleos de processamento
cpu_count = psutil.cpu_count()

#infos da Memória
mem = psutil.virtual_memory()
mem_total = round(mem.total/1073741824,2)

#Versão do Windows
for os in c.Win32_OperatingSystem():
    sys_op = os.Caption
    
#infos HD/SSD
disk = psutil.disk_partitions()


with dpg.window(tag="Componentes"):
    with dpg.group():
        dpg.add_text(f"Nome:                -> {pc_name}")
        dpg.add_text(f"Marca Placa Mãe:     -> {marca_mb}")
        dpg.add_text(f"Modelo Placa Mãe:    -> {modelo_mb}")
        dpg.add_text(f"Serie Placa Mãe:     -> {serie_mb}")
        dpg.add_text(f"Placa Vídeo:         -> {video}")
        dpg.add_text(f"Processador:         -> {modelo_processador}")
        dpg.add_text(f"Núcleos:             -> {cpu_count}")
        dpg.add_text(f"Memória RAM:         -> {mem_total}")
        dpg.add_text(f"Sistema Operacional: -> {sys_op}")
        dpg.add_separator()
        with dpg.collapsing_header(label="Armazenamento:"):
            lista_discos = []
            for local in disk:
                try:
                    total, used, free, percent = psutil.disk_usage(local[0])
                    lista_discos.append([local[0],round(total/1073741824,2) ])
                    dpg.add_text(f'{local[0]}')
                    dpg.add_text(f' Total {round(total/1073741824,2)}Gb') 
                    dpg.add_text(f' Used {round(used/1073741824,2)}Gb')
                    dpg.add_text(f' Free {round(free/1073741824,2)}Gb')
                except Exception as e:
                    pass
    with dpg.group(horizontal=True):
        dpg.add_button(label="Fechar",callback=dpg.destroy_context)
        dpg.add_button(label="Salvar",callback=salvar,user_data=[pc_name,marca_mb,modelo_mb,serie_mb,video,
                                                                 modelo_processador,cpu_count,mem_total,
                                                                 sys_op,lista_discos])
dpg.create_viewport(title="Inventario de PCs",width=600,height=400)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Componentes", True)
dpg.start_dearpygui()
dpg.destroy_context()