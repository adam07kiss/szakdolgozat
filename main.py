from flask import Flask, render_template, request
import pandas as pd

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
            # print(df[df['Kód:.4'] == kod]['Név.4'].to_list()[0])
            # break
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

        return render_template('result.html', eredmény_3_név_3=export_df, eredmenyek_ossz=eredmenyek_ossz)

    return 'Hiba: Nem sikerült feltölteni a fájlt.'


if __name__ == '__main__':
    app.run()
