import pickle
import streamlit as st
from tmdbv3api import Movie, TMDb

def get_recommendations(title):
    idx=movies[movies['title']==title].index[0]   #영화 제목 통해서 전체 데이터의 영화 인덱스 얻기
    sim_scores=list(enumerate(cosine_sim[idx]))
    sim_scores=sorted(sim_scores, key=lambda x:x[1], reverse=True)
    sim_scores=sim_scores[1:11]
    movie_indices=[i[0] for i in sim_scores]
    
    images=[]
    titles=[]
    for i in movie_indices:
        id=movies['id'].iloc[i]
        detail=movie.details(id)

        image_path=detail['poster_path']
        if image_path:
            image_path='https://image.tmdb.org/t/p/w500'+image_path
        else:
            image_path='no_image.jpg'

        images.append(image_path)
        titles.append(detail['title'])

    return images, titles


movie=Movie()
tmdb=TMDb()
tmdb.api_key = 'c8ecbe5b3e7b946e5c072a28e723ed95'
tmdb.language='ko-KR'   #우리나라 기준으로 데이터 가져오게 하기

#python에서 제작한 pickle 불러오기
movies=pickle.load(open('movies.pickle', 'rb'))
cosine_sim=pickle.load(open('cosine_sim.pickle','rb'))

#인터넷 화면 넓게 배치하기
st.set_page_config(layout='wide')
st.header('Cheonan GirlFlix')  #title

movie_list=movies['title'].values
title=st.selectbox('당신이 재밌게 감상한 영화를 선택하세요', movie_list)   #선택할 수 있는 네모칸

if st.button('영화 추천받기'):
    with st.spinner('검색중입니다...'):
        images, titles=get_recommendations(title)

        #화면에 추천영화 2행 5열로 출력
        idx=0
        for i in range(0,2):
            cols=st.columns(5)     #5col 생성
            for col in cols:       #각 col마다
                col.image(images[idx])  #우리가 받아온 images의 idx를 col에 추가
                col.write(titles[idx])  #우리가 받아온 title의 idx를 col에 추가
                idx+=1
