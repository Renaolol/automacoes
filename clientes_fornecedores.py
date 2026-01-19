import pandas as pd
import pyodbc
import datetime
import streamlit as st
import altair as alt
from time import sleep
st.set_page_config(layout="wide")
codigo = st.session_state.get("empresa_codigo")
nome = st.session_state.get("name")

if not codigo:  # sem empresa na sessão -> bloqueia
    codigo = st.text_input("Insira o código da empresa")
    st.info("Acesso de Administrador.")

# se seu banco espera número, tente converter:
try:
    codigo_int = int(str(codigo).strip())
except Exception:
    # se o banco aceita STRING, você pode manter como está e usar direto
    codigo_int = codigo  # fallback

conexao = (
    "DSN=ContabilPBI;UID=PBI;PWD=Pbi"
)
data_inicial = st.sidebar.date_input("Data inicial", datetime.date(2025, 1, 1),width=150,format="DD/MM/YYYY")   
data_final = st.sidebar.date_input("Data final", datetime.date.today(),width=150,format="DD/MM/YYYY")
#funções
def get_clientes(cod_empresa,data_inicio=data_inicial, data_fim=data_final):
    conn = pyodbc.connect(conexao)
    cursor = conn.cursor()
    query = """
            SELECT COUNT(e.codi_cli) AS quantidade, SUM(e.vcon_sai), f.nome_cli, a.NOME_ACU, f.regime_cli, f.cgce_cli
            FROM
                bethadba.efsaidas e
            JOIN bethadba.efclientes f
                ON e.codi_emp = f.codi_emp AND e.codi_cli = f.codi_cli
            JOIN bethadba.EFACUMULADOR a
                ON e.codi_emp = a.CODI_EMP AND a.CODI_ACU = e.codi_acu   
            WHERE
                e.codi_emp = ? AND e.ddoc_sai >= ? AND e.ddoc_sai <= ?
            GROUP BY f.nome_cli, a.NOME_ACU, f.regime_cli, f.cgce_cli
            ORDER BY quantidade DESC;
            """
    cursor.execute(query, (cod_empresa,data_inicio, data_fim))
    rows = cursor.fetchall()
    lista=[]
    for row in rows:
        lista.append((row[2], row[0], row[3], row[4],row[5],row[1]))

    cursor.close()
    conn.close()       
    return lista   

# Função para buscar a contagem de notas por fornecedor e também por acumuladores
def conectar_banco(cod_empresa,data_inicio=data_inicial, data_fim=data_final):
    conn = pyodbc.connect(conexao)
    cursor = conn.cursor()
    query = """
            SELECT COUNT(e.codi_for) AS quantidade, SUM (e.vcon_ent), f.nome_for, a.NOME_ACU, f.regime_for, f.cgce_for
            FROM
                bethadba.efentradas e
            JOIN bethadba.effornece f
                ON e.codi_emp = f.codi_emp AND e.codi_for = f.codi_for
            JOIN bethadba.EFACUMULADOR a
                ON e.codi_emp = a.CODI_EMP AND a.CODI_ACU = e.codi_acu   
            WHERE
                e.codi_emp = ? AND e.ddoc_ent >= ? AND e.ddoc_ent <= ?
            GROUP BY f.nome_for, a.NOME_ACU, f.regime_for, f.cgce_for
            ORDER BY quantidade DESC;
            """
    cursor.execute(query, (cod_empresa,data_inicio, data_fim))
    rows = cursor.fetchall()
    lista=[]
    for row in rows:
        lista.append((row[2], row[0], row[3], row[4],row[5],row[1]))

    cursor.close()
    conn.close()       
    return lista

# Função para formatar em R$
def formatar_reais(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

st.title(f"Dashboard de Clientes e Fornecedores | {nome}")
aba_fornecedores, aba_clientes, aba_analise=st.tabs(["🏭 Fornecedores", "🛒 Clientes","📈 Analise"])
with aba_fornecedores:

    st.subheader("Análise de Fornecedores")
    st.markdown(
        """
        Nesta seção, você pode analisar os fornecedores associados à empresa sua empresa.
        Utilize os filtros na barra lateral para ajustar o período da análise.
        """
    )
    aba1,aba2=st.tabs(["🏭 Tabela - Fornecedores", "📈 Gráfico - Fornecedores"])



    fornecedores=(conectar_banco(codigo_int))

    if not fornecedores:
        st.title(f"Dashboard do Faturamento | {nome}")
        st.warning(f"Nenhum dado encontrado para a empresa: {codigo}")
        st.stop()

    df_fornecedores=pd.DataFrame(fornecedores, columns=["NOME EMPRESA", "CONTAGEM", "ACUMULADORES","REGIME","CNPJ","VALOR"]).fillna("NÃO INFORMADO")
    df_fornecedores["VALOR"] = pd.to_numeric(df_fornecedores["VALOR"], errors="coerce").fillna(0)
    # Mapeamento dos códigos de regime para descrição
    regime_map = {
        "N": "Normal",
        "M": "ME",
        "E": "EPP",
        "O": "Outros",
        "S": "ME - Simples Nacional",
        "P": "EPP - Simples Nacional",
        "U": "Imune",
        "I": "Isenta"
    }

    df_fornecedores["REGIME"] = df_fornecedores["REGIME"].map(regime_map).fillna(df_fornecedores["REGIME"])

    with aba1:
        st.subheader("Fornecedores em tabela")
        st.markdown(
            """
            <style>
            .tooltip {
                position: relative;
                display: inline-block;
                cursor: pointer;
                color: #fad32b;
                font-weight: bold;
            }
            .tooltip .tooltiptext {
                visibility: hidden;
                width: 350px;
                background-color: #ffffff;
                color: #333;
                text-align: left;
                border-radius: 6px;
                padding: 10px;
                border: 1px solid #fad32b;
                position: absolute;
                z-index: 1;
                bottom: -175%; /* Show above */
                left: 100%;
                margin-left: -175px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.15);
            }
            .tooltip:hover .tooltiptext {
                visibility: visible;
            }
            </style>
            <div class="tooltip">
                Legenda dos Regimes
                <div class="tooltiptext">
                    <strong>Legenda dos Regimes:</strong><br>
                    <ul>
                        <li><b>Normal</b>: Empresas dos regimes Lucro Real ou Presumido</li>
                        <li><b>Outros</b>: Outros tipos de regime</li>
                        <li><b>ME - Simples Nacional</b>: Microempresa do Simples Nacional</li>
                        <li><b>EPP - Simples Nacional</b>: Empresa de Pequeno Porte do Simples Nacional</li>
                        <li><b>Imune</b>: Empresas Imunes</li>
                        <li><b>Isenta</b>: Empresas Isentas</li>
                    </ul>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.dataframe(df_fornecedores, use_container_width=True)
    with aba2:
        st.subheader("Fornecedores em gráfico")
        chart = (
            alt.Chart(df_fornecedores)
            .mark_bar(color="#fad32b")
            .encode(
                x=alt.X("NOME EMPRESA", sort="-y"),  # ordena do maior para menor
                y="CONTAGEM",
                tooltip=["NOME EMPRESA", "CONTAGEM"]
            )
        )

        st.altair_chart(chart, use_container_width=True)

with aba_clientes:
    st.subheader("Análise de Clientes")
    st.markdown("""
        Nesta seção, você pode analisar os clientes associados à sua empresa.
        Utilize os filtros na barra lateral para ajustar o período da análise.
        """
    )
    aba1,aba2=st.tabs(["🛒 Tabela - Clientes", "📈 Gráfico - Clientes"])
    # Função para buscar a contagem de notas por cliente e também por acumuladores

    clientes_list=(get_clientes(codigo_int))     
    if not clientes_list:
        st.warning(f"Nenhum dado encontrado para a empresa: {codigo}")
        st.stop()
    df_clientes = pd.DataFrame(clientes_list, columns=["NOME CLIENTE", "CONTAGEM", "ACUMULADORES", "REGIME", "CPF/CNPJ","VALOR"]).fillna("NÃO INFORMADO")
    df_clientes["VALOR"] = pd.to_numeric(df_clientes["VALOR"], errors="coerce").fillna(0)
    # Mapeamento dos códigos de regime para descrição
    regime_map = {
        "N": "Normal",
        "M": "ME",
        "E": "EPP",
        "O": "Outros",
        "S": "ME - Simples Nacional",
        "P": "EPP - Simples Nacional",
        "U": "Imune",
        "I": "Isenta"
    }
    df_clientes["REGIME"] = df_clientes["CPF/CNPJ"].apply(
        lambda x: "Física" if len(str(x)) == 11 else regime_map.get(df_clientes.loc[df_clientes["CPF/CNPJ"] == x, "REGIME"].values[0], df_clientes.loc[df_clientes["CPF/CNPJ"] == x, "REGIME"].values[0])
    )
    df_clientes.loc[df_clientes["CPF/CNPJ"] == "NÃO INFORMADO", "REGIME"] = "Física"
    with aba1:
        st.subheader("Clientes em tabela")
        st.markdown(
            """
            <style>
            .tooltip {
                position: relative;
                display: inline-block;
                cursor: pointer;
                color: #fad32b;
                font-weight: bold;
            }
            .tooltip .tooltiptext {
                visibility: hidden;
                width: 350px;
                background-color: #ffffff;
                color: #333;
                text-align: left;
                border-radius: 6px;
                padding: 10px;
                border: 1px solid #fad32b;
                position: absolute;
                z-index: 1;
                bottom: -175%; /* Show above */
                left: 100%;
                margin-left: -175px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.15);
            }
            .tooltip:hover .tooltiptext {
                visibility: visible;
            }
            </style>
            <div class="tooltip">
                Legenda dos Regimes
                <div class="tooltiptext">
                    <strong>Legenda dos Regimes:</strong><br>
                    <ul>
                        <li><b>Normal</b>: Empresas dos regimes Lucro Real ou Presumido</li>
                        <li><b>Outros</b>: Outros tipos de regime</li>
                        <li><b>ME - Simples Nacional</b>: Microempresa do Simples Nacional</li>
                        <li><b>EPP - Simples Nacional</b>: Empresa de Pequeno Porte do Simples Nacional</li>
                        <li><b>Imune</b>: Empresas Imunes</li>
                        <li><b>Isenta</b>: Empresas Isentas</li>
                    </ul>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.dataframe(df_clientes, use_container_width=True)
    with aba2:
        st.subheader("Clientes em gráfico")
        chart = (
            alt.Chart(df_clientes)
            .mark_bar(color="#fad32b")
            .encode(
                x=alt.X("NOME CLIENTE", sort="-y"),  # ordena do maior para menor
                y="CONTAGEM",
                tooltip=["NOME CLIENTE", "CONTAGEM"]
            )
        )

        st.altair_chart(chart, use_container_width=True)

with aba_analise:
    st.subheader("Análise Comparativa de Clientes e Fornecedores")
    st.markdown("""
        Nesta seção, você pode comparar a quantidade de clientes e fornecedores associados à sua empresa.
        Utilize os filtros na barra lateral para ajustar o período da análise.
        """
    )
    # --- Análise de Clientes (CONTAGEM) ---
    clientes_pf = df_clientes[df_clientes["REGIME"] == "Física"]["CONTAGEM"].sum()
    clientes_normal = df_clientes[df_clientes["REGIME"] == "Normal"]["CONTAGEM"].sum()
    clientes_simples = df_clientes[df_clientes["REGIME"].isin(["ME - Simples Nacional", "EPP - Simples Nacional"])]["CONTAGEM"].sum()
    clientes_outros = df_clientes[df_clientes["REGIME"] == "Outros"]["CONTAGEM"].sum()

    # --- Análise de Fornecedores (CONTAGEM) ---
    fornecedores_normal = df_fornecedores[df_fornecedores["REGIME"] == "Normal"]["CONTAGEM"].sum()
    fornecedores_simples = df_fornecedores[df_fornecedores["REGIME"].isin(["ME - Simples Nacional", "EPP - Simples Nacional"])]["CONTAGEM"].sum()
    fornecedores_outros = df_fornecedores[df_fornecedores["REGIME"] == "Outros"]["CONTAGEM"].sum()
    fornecedores_imune_isenta = df_fornecedores[df_fornecedores["REGIME"].isin(["Imune", "Isenta"])]["CONTAGEM"].sum()

    # --- Análise de Clientes (VALOR) ---
    valor_normal_clientes = df_clientes[df_clientes["REGIME"] == "Normal"]["VALOR"].sum()
    valor_simples_clientes = df_clientes[df_clientes["REGIME"].isin(["ME - Simples Nacional", "EPP - Simples Nacional"])]["VALOR"].sum()
    valor_outros_clientes = df_clientes[df_clientes["REGIME"] == "Outros"]["VALOR"].sum()
    valor_pf_clientes = df_clientes[df_clientes["REGIME"] == "Física"]["VALOR"].sum()
    valor_total_clientes = df_clientes["VALOR"].sum()

    # --- Análise de Fornecedores (VALOR) ---
    valor_normal_fornecedores = df_fornecedores[df_fornecedores["REGIME"] == "Normal"]["VALOR"].sum()
    valor_simples_fornecedores = df_fornecedores[df_fornecedores["REGIME"].isin(["ME - Simples Nacional", "EPP - Simples Nacional"])]["VALOR"].sum()
    valor_outros_fornecedores = df_fornecedores[df_fornecedores["REGIME"] == "Outros"]["VALOR"].sum()
    valor_imune_isenta_fornecedores = df_fornecedores[df_fornecedores["REGIME"].isin(["Imune", "Isenta"])]["VALOR"].sum()
    valor_total_fornecedores = df_fornecedores["VALOR"].sum()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Análise de Clientes")
        analise_clientes_data = {
            "Categoria": [
                "Clientes Físicos",
                "Clientes Normal",
                "Clientes Simples Nacional",
                "Clientes Outros"
            ],
            "Contagem": [
                clientes_pf,
                clientes_normal,
                clientes_simples,
                clientes_outros
            ]
        }
        df_analise_clientes = pd.DataFrame(analise_clientes_data)
        st.dataframe(df_analise_clientes, use_container_width=True)

        st.markdown("#### Análise por Valor dos Clientes")
        analise_valor_clientes_data = {
            "Categoria": [
                "Clientes Físicos",
                "Clientes Normal",
                "Clientes Simples Nacional",
                "Clientes Outros",
                "Total"
            ],
            "Valor": [
                valor_pf_clientes,
                valor_normal_clientes,
                valor_simples_clientes,
                valor_outros_clientes,
                valor_total_clientes
            ]
        }
        df_analise_valor_clientes = pd.DataFrame(analise_valor_clientes_data)
        df_analise_valor_clientes["Valor"] = df_analise_valor_clientes["Valor"].map(formatar_reais)
        st.dataframe(df_analise_valor_clientes, use_container_width=True)

    with col2:
        st.markdown("#### Análise de Fornecedores")
        analise_fornecedores_data = {
            "Categoria": [
                "Fornecedores Normal",
                "Fornecedores Simples Nacional",
                "Fornecedores Outros",
                "Fornecedores Imune/Isenta"
            ],
            "Contagem": [
                fornecedores_normal,
                fornecedores_simples,
                fornecedores_outros,
                fornecedores_imune_isenta
            ]
        }
        df_analise_fornecedores = pd.DataFrame(analise_fornecedores_data)
        st.dataframe(df_analise_fornecedores, use_container_width=True)

        st.markdown("#### Análise por Valor dos Fornecedores")
        analise_valor_fornecedores_data = {
            "Categoria": [
                "Fornecedores Normal",
                "Fornecedores Simples Nacional",
                "Fornecedores Outros",
                "Fornecedores Imune/Isenta",
                "Total"
            ],
            "Valor": [
                valor_normal_fornecedores,
                valor_simples_fornecedores,
                valor_outros_fornecedores,
                valor_imune_isenta_fornecedores,
                valor_total_fornecedores
            ]
        }
        df_analise_valor_fornecedores = pd.DataFrame(analise_valor_fornecedores_data)
        df_analise_valor_fornecedores["Valor"] = df_analise_valor_fornecedores["Valor"].map(formatar_reais)
        st.dataframe(df_analise_valor_fornecedores, use_container_width=True)
