import pandas as pd
import tabula
from tabula.io import read_pdf

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        filename = file.filename
        file.save(filename)

        pd.read_excel(filename).to_csv("valami.csv", header=False)

        kodok = set(pd.read_csv('valami.csv')['Tárgycsoport kódja'].to_list())

        df = pd.read_csv('valami.csv')

        nedf = df[df['Tárgycsoport kódja'] == 'MK-SZV']

        kreditszam = set(nedf['Kredit'].to_list())

        Eredmeny = []
        for i in nedf.columns.to_list():
            if 'Eredmény' in i:
                Eredmeny.append(i)

        eredmeny_listak = []
        for i in Eredmeny:
            eredmeny_listak.append(nedf[i].to_list())

        unnamed_5_set = set(pd.read_excel('export.xlsx', header=0)['Unnamed: 5'].to_list())

        df = df.fillna(0)

        eredmenyek2 = set(df[df['Eredmény.2'] != 0.0][df['Név.2'] != 0.0][df['Kredit.2'] != 0.0][
                              ['Eredmény.2', 'Név.2', 'Kredit.2', 'Kód:.2']][
                              df['Eredmény.2'].str.contains('Elégtelen') == False]['Kód:.2'])

        eredmenyek3 = set(df[df['Eredmény.3'] != 0.0][df['Név.3'] != 0.0][df['Kredit.3'] != 0.0][
                              ['Eredmény.3', 'Név.3', 'Kredit.3', 'Kód:.3']][
                              df['Eredmény.3'].str.contains('Elégtelen') == False]['Kód:.3'])

        eredmenyek4 = set(df[df['Eredmény.4'] != 0.0][df['Név.4'] != 0.0][df['Kredit.4'] != 0.0][
                              ['Eredmény.4', 'Név.4', 'Kredit.4', 'Kód:.4']][
                              df['Eredmény.4'].str.contains('Elégtelen') == False]['Kód:.4'])

        eredmenyek_osszes = eredmenyek2.union(eredmenyek3).union(eredmenyek4)

        eredmenyek4_kredit = 0
        export_df = pd.DataFrame({'Név': [], 'Eredmény': [], 'Kredit': []})
        for kod in eredmenyek4.intersection(eredmenyek_osszes):
            eredmenyek4_kredit += int(df[df['Kód:.4'] == kod]['Kredit.4'][:1])
            export_df.loc[len(export_df.index)] = [str(df[df['Kód:.4'] == kod]['Név.4'][:1].to_list()[0]),
                                                   str(df[df['Kód:.4'] == kod]['Eredmény.4'][:1].to_list()[0]),
                                                   int(df[df['Kód:.4'] == kod]['Kredit.4'][:1].to_list()[0])]

        eredmenyek3_kredit = 0
        for kod in eredmenyek3.intersection(eredmenyek_osszes - eredmenyek4):
            eredmenyek3_kredit += int(df[df['Kód:.3'] == kod]['Kredit.3'][:1])
            export_df.loc[len(export_df.index)] = [str(df[df['Kód:.3'] == kod]['Név.3'][:1].to_list()[0]),
                                                   str(df[df['Kód:.3'] == kod]['Eredmény.3'][:1].to_list()[0]),
                                                   int(df[df['Kód:.3'] == kod]['Kredit.3'][:1].to_list()[0])]

        eredmenyek2_kredit = 0
        for kod in eredmenyek2.intersection(eredmenyek_osszes - eredmenyek3 - eredmenyek4):
            eredmenyek2_kredit += int(df[df['Kód:.2'] == kod]['Kredit.2'][:1])
            export_df.loc[len(export_df.index)] = [str(df[df['Kód:.2'] == kod]['Név.2'][:1].to_list()[0]),
                                                   str(df[df['Kód:.2'] == kod]['Eredmény.2'][:1].to_list()[0]),
                                                   int(df[df['Kód:.2'] == kod]['Kredit.2'][:1].to_list()[0])]

        eredmenyek_ossz = sum(export_df['Kredit'].to_list())


        pdf_path = "templates/20171112___pti_bsc.pdf"
        excel_output = "output.xlsx"
        csv_output = "tablazat.csv"

        tables = tabula.read_pdf(pdf_path, pages="all", encoding='ISO-8859-1')

        pdf_output = pd.concat(tables, ignore_index=True)
        pdf_output.loc[-1] = pdf_output.columns
        pdf_output.index = pdf_output.index + 1
        pdf_output = pdf_output.sort_index()
        pdf_output.to_excel(excel_output, index=False)
        pdf_output.to_csv(csv_output, index=False)

        pd.read_excel('output.xlsx').to_csv("tablazat.csv", header=True)
        pdf = pd.read_csv('tablazat.csv')
        pdf.fillna(0).head(47)

        merged_pdf = pd.concat([pdf["Diszkrét matematika I. ea"], pdf["Programozás alapjai ea"],
                               pdf["Szakdolgozat készítése 1. (pti)"]]).dropna()
        merged_kod = pd.concat([pdf["MBNXK111E"], pdf["IB104E"], pdf["IB3000"]]).dropna()
        merged_kod.name = "Tárgycsoport kódja"
        merged_kod = merged_kod.reset_index(drop=True)
        merged_kod = merged_kod[~merged_kod.str.isnumeric()]

        merged_pdf.name = "Név"
        merged_pdf = merged_pdf.reset_index(drop=True)
        merged_pdf = merged_pdf[~merged_pdf.str.isnumeric()]


        eredmenyek4_kredit2 = 0
        export_df2 = pd.DataFrame({'Név': [], 'Tárgycsoport kódja': []})
        for kod in eredmenyek4.intersection(eredmenyek_osszes):
            eredmenyek4_kredit2 += int(df[df['Kód:.4'] == kod]['Kredit.4'][:1])
            export_df2.loc[len(export_df2.index)] = [str(df[df['Kód:.4'] == kod]['Név.4'][:1].to_list()[0]),
                                                     str(df[df['Kód:.4'] == kod]['Tárgycsoport kódja.4'][:1].to_list()[
                                                             0])]
        eredmenyek3_kredit2 = 0
        for kod in eredmenyek3.intersection(eredmenyek_osszes - eredmenyek4):
            eredmenyek3_kredit2 += int(df[df['Kód:.3'] == kod]['Kredit.3'][:1])
            export_df2.loc[len(export_df2.index)] = [str(df[df['Kód:.3'] == kod]['Név.3'][:1].to_list()[0]),
                                                     str(df[df['Kód:.3'] == kod]['Tárgycsoport kódja.3'][:1].to_list()[
                                                             0])]
        eredmenyek2_kredit2 = 0
        for kod in eredmenyek2.intersection(eredmenyek_osszes - eredmenyek3 - eredmenyek4):
            eredmenyek2_kredit2 += int(df[df['Kód:.2'] == kod]['Kredit.2'][:1])
            export_df2.loc[len(export_df2.index)] = [str(df[df['Kód:.2'] == kod]['Név.2'][:1].to_list()[0]),
                                                     str(df[df['Kód:.2'] == kod]['Tárgycsoport kódja.2'][:1].to_list()[
                                                             0])]

        export_df2 = export_df2.sort_values(by='Név', ascending=True).reset_index(drop=True)

        merged_kod = merged_kod.str.upper()
        export_df2["Tárgycsoport kódja"] = export_df2["Tárgycsoport kódja"].str.upper()

        merged = pd.DataFrame(merged_pdf).join(merged_kod)

        row_index = 2
        column_name = 'Tárgycsoport kódja'  # Replace with the column name
        new_value = 'MBNXK311E'  # Replace with the new value
        merged[column_name].loc[row_index] = new_value
        #
        row_index = 27
        column_name = 'Tárgycsoport kódja'  # Replace with the column name
        new_value = 'IB204E-00001'  # Replace with the new value
        merged[column_name].loc[row_index] = new_value
        #
        row_index = 28
        column_name = 'Tárgycsoport kódja'  # Replace with the column name
        new_value = 'IB204L'  # Replace with the new value
        merged[column_name].loc[row_index] = new_value
        #
        row_index = 46
        column_name = 'Tárgycsoport kódja'  # Replace with the column name
        new_value = 'IB3000G'  # Replace with the new value
        merged[column_name].loc[row_index] = new_value

        row_index = 47
        column_name = 'Tárgycsoport kódja'  # Replace with the column name
        new_value = 'IB3001G'  # Replace with the new value
        merged[column_name].loc[row_index] = new_value

        merged = merged.sort_values(by="Név", ascending=True).reset_index(drop=True)

        kotelezo_targyak = export_df2[export_df2["Tárgycsoport kódja"].isin(merged["Tárgycsoport kódja"])]
        kotelezo_targyak = kotelezo_targyak.sort_values(by="Név", ascending=True).reset_index(drop=True)

        fennmarado_kotelezo_targyak = pd.concat([merged, kotelezo_targyak]).drop_duplicates(subset=['Tárgycsoport kódja'],
                                                                                            keep=False)

        return render_template('result.html', eredmény_3_név_3=export_df, eredmenyek_ossz=eredmenyek_ossz,
                               fennmarado_kotelezo_targyak=fennmarado_kotelezo_targyak)

    return 'Hiba: Nem sikerült feltölteni a fájlt.'


if __name__ == '__main__':
    app.run()
