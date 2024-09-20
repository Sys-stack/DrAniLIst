import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image

#def image
def scale_img(image_path,x_axis,y_axis):
  img = Image.open(image_path)
  resized_image = image.resize((x_axis,y_axis))
  return resized_image
  
  
#page configuration
st.set_page_config(
  page_title = "DrAniList",
  page_icon = "",
  layout = 'wide',
  initial_sidebar_state = 'collapsed',
  theme = {'primaryColor':'',
           'backgroundColor:'',
           'font':'sans serif',
           'textColor':''
          })
print(scale_img("https://github.com/Sys-stack/DrAniLIst/blob/image/HorizontalLine1.png?raw=true",300,40))
#page header and title
st.title("DrAniList")
st.image(scale_img("https://github.com/Sys-stack/DrAniLIst/blob/image/HorizontalLine1.png?raw=true",300,40))
