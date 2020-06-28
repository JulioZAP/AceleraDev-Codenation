import streamlit as st
import pandas as pd
import missingno as msno
import seaborn as sns
import matplotlib.pyplot as plt
import altair as alt


def criar_histograma(coluna, df):
    chart = alt.Chart(df, width=600).mark_bar().encode(
        alt.X(coluna, bin=True),
        y='count()', tooltip=[coluna, 'count()']
    ).interactive()
    return chart


def criar_barras(coluna_num, coluna_cat, df):
    bars = alt.Chart(df, width=600).mark_bar().encode(
        x=alt.X(coluna_num, stack='zero'),
        y=alt.Y(coluna_cat),
        tooltip=[coluna_cat, coluna_num]
    ).interactive()
    return bars


def criar_scatterplot(x, y, color, df):
    scatter = alt.Chart(df, width=800, height=400).mark_circle().encode(
        alt.X(x),
        alt.Y(y),
        color=color,
        tooltip=[x, y]
    ).interactive()
    return scatter


# Começa aqui
def main():
    st.title('Codenation')
    st.subheader("Análise Exploratória de Dados")
    st.sidebar.markdown("<<<Feito por>>>")
    st.sidebar.image("logoec.jpeg", width=300)
    st.sidebar.markdown("https://github.com/JulioZAP\nhttps://github.com/Andrade21R")

    st.title('AceleraDev - Semana 3')
    st.subheader('Semana 3 - Análise de dados exploratória')
    st.image('https://media.giphy.com/media/lkdIhnHHnFma6xvICt/giphy.gif', width=400)
    sep_choose = st.radio("Como é feita a separação do seu arquivo?: ", [',', ';'])
    file = st.file_uploader('Selecione seu arquivo csv', type='csv')
    if file is not None:
        df = pd.read_csv(file, sep=sep_choose)
        backup = df.copy()

        if st.sidebar.button('Resetar alterações'):
            df = backup.copy()

        options = st.sidebar.selectbox(
            "Quais informações pretende visualizar?",
            ("Selecione uma opção", "Básicas", "Dados faltantes", "Outliers", "Correlação",
             "Distribuição e Visualização dos dados")
        )

        aux = pd.DataFrame({"colunas": df.columns, 'tipos': df.dtypes})
        colunas_numericas = list(aux[aux['tipos'] != 'object']['colunas'])
        colunas_object = list(aux[aux['tipos'] == 'object']['colunas'])
        colunas = list(df.columns)
        if options == 'Básicas':
            st.subheader("Visualizar dados")
            numeros = st.slider(
                'Note que limitamos o tamanho da visualização para obtermos maior performancena execução do app',
                min_value=5, max_value=30
            )
            st.dataframe(df.head(numeros))

            st.subheader('Estatística descritiva univariada')
            col = st.selectbox('Selecione a coluna :', colunas_numericas)
            if col is not None:
                st.markdown('Selecione o que deseja analisar :')
                mean = st.checkbox('Média')
                if mean:
                    st.markdown(df[col].mean())
                median = st.checkbox('Mediana')
                if median:
                    st.markdown(df[col].median())
                desvio_pad = st.checkbox('Desvio padrão')
                if desvio_pad:
                    st.markdown(df[col].std())
                kurtosis = st.checkbox('Kurtosis')
                if kurtosis:
                    st.markdown(df[col].kurtosis())
                skewness = st.checkbox('Skewness')
                if skewness:
                    st.markdown(df[col].skew())
                describe = st.checkbox('Describe')
                if describe:
                    st.table(df[colunas_numericas].describe().transpose())

        elif options == 'Dados faltantes':
            st.subheader('Dados faltantes: ')
            heat = msno.bar(df)
            st.write(heat)
            st.pyplot()
            opt = st.radio('Imputar dados faltantes a partir de :', ("Mediana", "Média", "Zero", "Moda"))
            options = st.multiselect('Em quais colunas?', df.columns.tolist())
            if st.button("Imputar dados"):
                for i in options:
                    if df[i].dtype == 'object':
                        if opt == "Moda":
                            df.fillna({i: df[i].mode()[0]}, inplace=True)
                            st.success("Valores imputados com sucesso!")
                        else:
                            st.error("Erro! Variáveis categóricas só podem ser preenchidas com a moda")
                    else:
                        if opt == "Média":
                            df.fillna({i: df[i].mean()}, inplace=True)
                        elif opt == "Moda":
                            df.fillna({i: df[i].mode()[0]}, inplace=True)
                        elif opt == "Mediana":
                            df.fillna({i: df[i].median()}, inplace=True)
                        elif opt == "Zero":
                            df.fillna({i: 0}, inplace=True)
                        st.success("Valores imputados com sucesso!")

        elif options == "Correlação":
            st.subheader('Correlação: ')
            options = st.multiselect('Quais colunas?', df.columns.tolist(), default=list(df.columns))
            if len(df[options].columns) > 19:
                plt.subplots(figsize=(15, 12))
            elif len(df[options].columns) > 10:
                plt.subplots(figsize=(12, 10))
            else:
                plt.subplots(figsize=(8, 5))
            sns.heatmap(df[options].corr(), square=True, annot=True)
            st.pyplot()

        elif options == 'Distribuição e Visualização dos dados':
            st.subheader('Gráficos de distribuição: ')
            var_select = st.selectbox('Selecione a variável: ', df.columns)
            if var_select:
                if df[var_select].dtype == 'object':
                    df[var_select].value_counts().plot(kind='bar')
                else:
                    sns.distplot(df[var_select])
                    st.write('Assimetria (Skewness): ', df[var_select].skew(), 'Achatamento (Kurtosis): ',
                             df[var_select].kurtosis())

                plt.title("Distribuição de " + var_select)
                st.pyplot()

            st.subheader('Visualização dos dados')
            st.image('https://media.giphy.com/media/l41YvpiA9uMWw5AMU/giphy.gif', width=300)
            st.markdown('Selecione a visualizacao')
            histograma = st.checkbox('Histograma')
            if histograma:
                col_num = st.selectbox('Selecione a Coluna Numerica: ', colunas_numericas, key='unique')
                st.markdown('Histograma da coluna : ' + str(col_num))
                st.write(criar_histograma(col_num, df))
            barras = st.checkbox('Gráfico de barras')
            if barras:
                col_num_barras = st.selectbox('Selecione a coluna numerica: ', colunas_numericas, key='unique')
                col_cat_barras = st.selectbox('Selecione uma coluna categorica : ', colunas_object, key='unique')
                st.markdown('Gráfico de barras da coluna ' + str(col_cat_barras) + ' pela coluna ' + col_num_barras)
                st.write(criar_barras(col_num_barras, col_cat_barras, df))
            scatter = st.checkbox('Scatterplot')
            if scatter:
                col_num_x = st.selectbox('Selecione o valor de x ', colunas_numericas, key='unique')
                col_num_y = st.selectbox('Selecione o valor de y ', colunas_numericas, key='unique')
                col_color = st.selectbox('Selecione a coluna para cor', colunas)
                st.markdown('Selecione os valores de x e y')
                st.markdown(criar_scatterplot(col_num_x, col_num_y, col_color, df))

        elif options == 'Outliers':
            st.subheader('Outliers: ')
            out_select = st.selectbox('Selecione a variável que deseja ver os outliers: ', colunas_numericas)
            st.markdown("Note que apenas colunas numéricas são uma opção")
            if out_select:
                sns.boxplot(df[out_select])
                plt.title("Distribuição de " + out_select)
                st.pyplot()


if __name__ == '__main__':
    main()
