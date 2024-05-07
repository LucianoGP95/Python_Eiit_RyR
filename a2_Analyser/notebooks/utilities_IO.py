import os
import pandas as pd

html_string = '''
<html>
  <head>
    <title>Analyser results</title>
    <link rel="icon" type="image/png" href="../../assets/icon.ico">
  </head>
  <link rel="stylesheet" type="text/css" href="../../resources/df_style.css"/>
  <body>
    {table}
  </body>
</html>
'''

def output_html(df, name):
  pd.set_option('display.width', 1000)
  pd.set_option('colheader_justify', 'center')
  os.chdir(os.path.dirname(__file__))
  filename = name
  filepath = os.path.join(os.path.abspath("../a2_output/reports/"), filename)
  with open(filepath, 'w') as f:
    for i, data in enumerate(df):
      f.write(html_string.format(table=df[i].to_html(classes='mystyle')))