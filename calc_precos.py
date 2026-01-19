import streamlit as st
from time import sleep
st.set_page_config(layout="wide")

def formata_valor(valor):
    valor = f'R$ {valor:,.2f}'
    valor = valor.replace(",","X").replace(".",",").replace("X",".")
    return valor
st.title("SIMULADOR || CÁLCULOS DE PREÇOS DE VENDAS")
with st.container(border=True):
    dados_col1, dados_col2,dados_col3,dados_col4,dados_col5=st.columns(5)
    with dados_col1:
        regime = st.selectbox("Selecione o regime: ",["Simples Nacional - Hibrido","Lucro Real","Lucro Presumido"])
    with dados_col2:
        preco_compra = st.number_input("Insira o preço de compra :")
    with dados_col3:
        aliq_lucro_desejado = round((st.number_input("Insira o percentual de lucro desejado :")/100),2)
    with dados_col4:
        if regime == "Lucro Real":
            aliq_pis = 1.65/100
            aliq_cofins = 7.6/100
            aliq_simples=0
            aliq_icms = round((st.number_input("Insira a aliquota de ICMS :", format="%0.2f")/100),2)
        elif regime == "Lucro Presumido":
            aliq_pis = 0.65/100
            aliq_cofins = 3/100
            aliq_simples=0
            aliq_icms =round((st.number_input("Insira a aliquota de ICMS :", format="%0.2f")/100),2)
        else:
            aliq_pis = 0
            aliq_cofins = 0
            aliq_icms = 0
            aliq_simples =st.number_input("Insira o valor da aliquota do SN:", format="%0.2f")/100
    with dados_col5:
        icms_destacado = st.number_input("Icms destacado NF-e Compra: ")
preco_compra_limpo=0

col_radio1,col_radio2 = st.columns(2)
with col_radio1:
    fornecedor = st.radio("Selecione o Regime do seu fornecedor", ("Lucro Real","Lucro Presumido","Simples Nacional","SN - Apuração por Fora"),horizontal=True)
with col_radio2:
    ano = st.radio("Selecione o ano: ",["2026","2027/2028","2029","2030","2031","2032","2033"],horizontal=True)

icms_compra = preco_compra*(icms_destacado/100)
bc_pis_cofins = preco_compra - icms_compra
if fornecedor in ["Simples Nacional","SN - Apuração por Fora"]:
    preco_compra_limpo = preco_compra
elif fornecedor == "Lucro Real":  
    pis_cofins = bc_pis_cofins*((1.65+7.6)/100)
    preco_compra_limpo = preco_compra - icms_compra - pis_cofins  
elif fornecedor == "Lucro Presumido":
    pis_cofins = bc_pis_cofins*((0.65+3)/100)
    preco_compra_limpo = preco_compra - icms_compra - pis_cofins 
#Preco_compra_limpo vai permanecer estático durante a execução do código inteiro

#Definir em campos Streamlit
red_aliq = 1
ref_ibs = 17.7
#---------------

#Primeiro ajustar para Lucro Real
if ano == '2026':
    aliq_cbs = (0.9/100)*red_aliq
    aliq_ibs = (0.1/100)*red_aliq
    icms_reforma = aliq_icms
elif ano == '2027/2028':
    aliq_cbs = (8.7/100)*red_aliq
    aliq_ibs = (0.1/100)*red_aliq
    icms_reforma = aliq_icms
    aliq_pis = 0
    aliq_cofins = 0
elif ano == '2029':
    aliq_cbs = (8.8/100)*red_aliq
    aliq_ibs = ((ref_ibs*0.10)/100)*red_aliq
    icms_reforma = aliq_icms*0.90
    aliq_pis = 0
    aliq_cofins = 0
elif ano == '2030':
    aliq_cbs = (8.8/100)*red_aliq
    aliq_ibs = ((ref_ibs*0.20)/100)*red_aliq
    icms_reforma = aliq_icms*0.80
    aliq_pis = 0
    aliq_cofins = 0
elif ano == '2031':
    aliq_cbs = (8.8/100)*red_aliq
    aliq_ibs = ((ref_ibs*0.30)/100)*red_aliq
    icms_reforma = aliq_icms*0.70
    aliq_pis = 0
    aliq_cofins = 0
elif ano == '2032':
    aliq_cbs = (8.8/100)*red_aliq
    aliq_ibs = ((ref_ibs*0.40)/100)*red_aliq
    icms_reforma = aliq_icms*0.60
    aliq_pis = 0
    aliq_cofins = 0
elif ano == '2033':
    aliq_cbs = (8.8/100)*red_aliq
    aliq_ibs = ((ref_ibs)/100)*red_aliq
    icms_reforma = 0
    aliq_pis = 0
    aliq_cofins = 0


#Calculo do preço de venda
valor_cbs = aliq_cbs*preco_compra_limpo
valor_ibs = aliq_ibs*preco_compra_limpo


preco_venda = preco_compra/(1-icms_reforma-aliq_pis-aliq_cofins-aliq_lucro_desejado-aliq_simples)
valor_icms = icms_reforma*preco_venda
preco_venda_ibs_cbs = (preco_venda + valor_ibs+valor_cbs)if ano!="2026"else preco_venda
#COLUNAS DE APRESENTAÇÃO
col1,col2, col3 = st.columns(3)
with col1:
    st.metric("Preço descontaminado",formata_valor(preco_compra_limpo))
    st.metric("Preco de Venda",formata_valor(preco_venda))
    st.metric("Preco de Venda com IBS e CBS",formata_valor(preco_venda_ibs_cbs))
with col2:
    if regime != "Simples Nacional - Hibrido":
        st.metric("ICMS",formata_valor((preco_venda*icms_reforma)))
    else:
        st.metric("Simples Nacional",formata_valor((preco_venda*aliq_simples)))
    st.metric("IBS",formata_valor(valor_ibs))
    st.metric("CBS", formata_valor(valor_cbs))
with col3:
    st.metric("Aliq ICMS", round(icms_reforma,4))
    st.metric("Lucro",formata_valor((preco_venda*aliq_lucro_desejado)))
    st.metric("PIS e Cofins", formata_valor(preco_venda*(aliq_pis+aliq_cofins)))
st.divider()
