from django.shortcuts import render,HttpResponse,redirect
import pickle
import numpy as np
popular_df=pickle.load(open('popular.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl','rb'))

# Create your views here.
def index(request):
    booktitle=list(popular_df['Book-Title'].values)
    bookauthor=list(popular_df['Book-Author'].values)
    image=list(popular_df['Image-URL-M'].values)
    votes=list(popular_df['num_ratings'].values)
    rating=list(popular_df['avg_rating'].values)
    
    count=len(booktitle)
    params=zip(image,booktitle,bookauthor,votes,rating) 
    # context={'params':params,'booktitle':booktitle,'bookauthor':bookauthor,'image':image,'votes':votes,'rating':rating,'count':count}
    context={'params':params}
    return render(request, 'index.html',context)


def recommender(request):
    if request.method=='POST':  
        user_input=request.POST['user_input']
        index = np.where(pt.index == user_input)[0][0]
        similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

        data = []
        for i in similar_items:
            item = []
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

            data.append(item)
        params={'data':data}
        return render(request, 'recommender.html',params)
    return render(request, 'recommender.html')