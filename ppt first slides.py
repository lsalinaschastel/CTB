from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statistics
from datetime import date, timedelta, datetime
import io
from pptx import Presentation
from pptx.util import Inches
from pptx import Presentation



# Import data
df=pd.read_csv('concat_datas_elea.csv', index_col=0, sep=';')
dictio = pd.read_csv('Dict_final.csv', delimiter=';')

# Create ppt
ppt = Presentation()

# First slide
title_slide_layout = ppt.slide_layouts[0]
slide = ppt.slides.add_slide(title_slide_layout)
slide.shapes.title.text = "CLARIFY"
subtitle = slide.placeholders[1]
subtitle.text = "Generated on {:%m-%d-%Y}".format(date.today())

# Second slide
# Initial analysis
info=[]
for i in df.columns:
    info.append(f'{i} : {df[i].nunique()} values')

second_slide = ppt.slide_layouts[5]
second = ppt.slides.add_slide(second_slide)
second.shapes.title.text = "Data has been extracted"  + "\n Unique values:  " +"\n " + str(info[1:(round(len(info)/2))]
# add a text box
textbox = second.shapes.add_textbox(Inches(3), Inches(1.5),Inches(3), Inches(1))
textframe = textbox.text_frame
paragraph = textframe.add_paragraph()
paragraph.text = "Data from " + str(len(df)) +" women has been processed"




ppt.save("test.pptx")