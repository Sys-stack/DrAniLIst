import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import requests
from io import BytesIO
import ast

#def image
def scale_img(image_path,x_axis,y_axis):
  req = requests.get(image_path)
  img = Image.open(BytesIO(req.content))
  resized_image = img.resize((x_axis,y_axis))
  return resized_image

def sublistcheck(sub, master):
    for i in sub:
        if i not in master:
            y = False
            break
        else:
            y = True
    return y
  
#page configuration
st.set_page_config(
  page_title = "DrAniList",
  page_icon = "",
  layout = 'wide',
  initial_sidebar_state = 'collapsed')
#page header and title

if 'nextpage' not in st.session_state:
  st.session_state.nextpage = True

if st.session_state.nextpage:
  st.title("DrAniList")
  st.image(scale_img("https://github.com/Sys-stack/DrAniLIst/blob/image/HorizontalLine1.png?raw=true",5000,40))

  st.text("""  DrAniList is your go-to app for tracking your anime and drama viewing habits.
  With features designed for convenience and efficiency, you can easily save your 
  lists locally, making it simple to access your favorite shows anytime, anywhere.
  
  Our user-friendly interface allows for quick file transfers, so you can share your
  lists effortlessly with friends or across devices. Plus, editing your entries is a
  breeze update your progress, add notes, or remove shows in just a few taps.
  
  Whether you’re looking to organize your viewing experience or share your 
  recommendations with others, DrAniList has you covered. Take control of your anime
  and drama journey today!""")
  checkbox = st.checkbox("Continue to use DrAniList")

if not st.session_state.nextpage:
    checkbox = 0
    anidictmodel = {'S.no':[], 'Title':[],'Status':[],'Type':[],'Episodes':[],'Watched Episodes':[],
            'Studio': [], 'Genre': [], 'Start-date': [], 
            'End-date': [], 'Source': [], 'Score': [], 
            'Tags': [], 'Season':[]}
    all_ani_list = pd.DataFrame(anidictmodel)
    csvfile = st.file_uploader("Upload your locally saved DrAniList: ")
    malfile = st.file_uploader("Upload your MyAnimeList csv file: ")
    mal = pd.DataFrame() 
    if bool(malfile) == True:
        mal = pd.read_csv(malfile)
        mal.rename(columns={
        'series_title': 'Title',
        'series_type': 'Type',
        'series_episodes': 'Episodes',
        'my_watched_ep': 'Watched Episodes',
        'my_start_date': 'Start-date',
        'my_finish_date': 'End-date',
        'my_score': 'Score',
        'my_status': 'Status'
         }, inplace=True)

        cols_to_drop = []

        for [col, cs] in mal.T.iterrows():
            if col not in all_ani_list.columns:
                cols_to_drop.append(col)
        mal.drop(columns=cols_to_drop, inplace=True)

        for col, cs in all_ani_list.T.iterrows():
            if col not in mal.columns:
                mal[col] = all_ani_list[col]
      
        i = 0
        for row,rs in mal.iterrows():
            i += 1
            mal['S.no'][row] = int(i)
        mal.set_index('S.no', inplace = True)
        mal = mal.reindex(columns = all_ani_list.columns)



    if csvfile != None:
        all_ani_list = pd.read_csv(csvfile, sep = '*', index_col = 'S.no')
    if mal.empty != True:
        all_ani_list = mal
    freshuse = st.checkbox("If you haven't already used DrAniLIst click here to get DrAniList file: ")
  
    if freshuse:
        freshfile = requests.get("https://raw.githubusercontent.com/Sys-stack/DrAniLIst/refs/heads/files/anilist.csv?token=GHSAT0AAAAAACXV5I46XJPDM6HIRMJNP63MZXPZSBA")
        st.download_button(label = "DrAnilist file format download: ",
        data = freshfile.content,
        file_name = "DrAniList.csv",
        mime = "text/csv")
      
    gimg = 'https://raw.githubusercontent.com/Sys-stack/IP-Test/test/japan-background-digital-art.jpg'
    bgimg = scale_img(gimg,800,100)
    st.markdown(f"<h2 style='text-align: center; background-image: {bgimg};'>DRANILIST</h2>", unsafe_allow_html=True)

    cmd = st.selectbox('Choose: ', ("None","Show List", "Errors", 'Timeline', 'Statistics', 'Profile'))
    #completed list
    owari_list = pd.DataFrame(anidictmodel)
    owari_list.set_index('S.no',inplace = True)
    i = 0
    for [row,rowseries] in all_ani_list.iterrows():
      if all_ani_list['Status'][row] == 'Completed':
        i += 1
        owari_list.loc[i] = rowseries
    #watching list
    wat_list = pd.DataFrame(anidictmodel)
    wat_list.set_index('S.no',inplace = True)
    for [row,rowseries] in all_ani_list.iterrows():
      if all_ani_list['Status'][row] == 'Watching':
        i += 1
        wat_list.loc[i] = rowseries
    #on_hold list
    oh_list = pd.DataFrame(anidictmodel)
    oh_list.set_index('S.no',inplace = True)
    for [row,rowseries] in all_ani_list.iterrows():
      if all_ani_list['Status'][row] == 'On-Hold':
        i += 1
        oh_list.loc[i] = rowseries
    #Dropped list
    drop_list = pd.DataFrame(anidictmodel)
    drop_list.set_index('S.no',inplace = True)
    for [row,rowseries] in all_ani_list.iterrows():
      if all_ani_list['Status'][row] == 'Dropped':
        i += 1
        drop_list.loc[i] = rowseries
    #ptw
    ptw_list = pd.DataFrame(anidictmodel)
    ptw_list.set_index('S.no',inplace = True)
    for [row,rowseries] in all_ani_list.iterrows():
      if all_ani_list['Status'][row] == 'Plan to Watch':
        i += 1
        ptw_list.loc[i] = rowseries

    if cmd == "Show List":
      key = st.selectbox("Choose: ", ("All", "Completed", 'Watching', 'On-Hold', 'Dropped', 'Plan to watch'))
      dict1 = {'All': all_ani_list,
               'Watching': wat_list, 
               'Completed': owari_list, 
               'On-Hold': oh_list, 
               'Dropped': drop_list, 
               'Plan to Watch': ptw_list}
      if key in dict1:
        st.table(dict1[key])

    #Error Checker
    genre = ["Action", "Adventure", "Comedy",
         "Drama", "Fantasy", "Horror",
         "Mystery", "Psychological", "Romance",
         "Sci-Fi", "Slice of Life", "Sports",
         "Supernatural", "Historical",
         "Music", "Mecha", "Magic",
         "Military", "Superpower",
         "Demons", "Isekai", "Harem",
         "Yaoi", "Yuri", "Tragedy",
         "Parody", "Ecchi", "Seinen",
         "Shoujo", "Shounen", "Josei",
         "Gender Bender", "Martial Arts", "Space",
         "Game","School", "Vampire",
         "Samurai", "Aliens", "Dystopian",
         "Romantic Comedy", "Psychological Thriller",
         "Gore", "Dark Fantasy", "Action Comedy",
         "Historical Drama", "Superhero", "Post-Apocalyptic",
         "CGDCT"]

    stxt = 'There are status errors in the following rows: '
    gtxt = 'There are genre errors in the following rows: '
    rtxt = 'There are Score errors in the following rows: '
    etxt = 'There are other errors in the following columns and rows: '
    earguement = 0
    sarguement = 0
    garguement = 0
    rarguement = 0

    if cmd =='Errors':
        for [row,rowseries] in all_ani_list.iterrows():
    #Status column
            if all_ani_list['Status'][row] != ('Completed' or 'Plan to Watch' or
                                               'Dropped' or 'On-hold' or
                                               'Watching'):
                stxt += ('''
                       ''' + '(Status)' + str(row))
                sarguement = True

#Genre Column
            if all_ani_list['Genre'][row] != np.nan:
                if sublistcheck(ast.literal_eval(all_ani_list['Genre'][row]),genre) == False:
                    gtxt += ('''
                                ''' + '(Genre)' + str(row))
                    arguement = True
            else: 
                gtxt += ('''
                                ''' + '(Genre)' + str(row))
                arguement = True
              
            if all_ani_list['Score'][row] not in range(0,11):
                rtxt += ('''
                ''' + '(Score)' + str(row))
                rarguement = True
            for col in ['S.no','Title','Type','Episodes','Studio','Start-date','End-date','Source','Season']:
                if bool(all_ani_list[col][row]) == False:
                    earguement = True
                    etxt += ('''
                    ''' + '(' + str(col) + ')' + str(row))
    if sarguement == True:
        st.text(stxt)
    if garguement == True:
        st.text(gtxt)
    if rarguement == True:
        st.text(rtxt)
    if earguement == True:
        st.text(etxt)
  
    
if checkbox:
    st.session_state.nextpage = True
else:
    st.session_state.nextpage = False
