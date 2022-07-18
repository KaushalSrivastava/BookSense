from flask import Flask,render_template,request
import pickle
import numpy as np

popular_df = pickle.load(open('popular.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
st = pickle.load(open('st.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           title = list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-L'].values),
                           publisher=list(popular_df['Publisher'].values),
                           year=list(popular_df['Year-Of-Publication'].values)
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/books',methods=['post'])
def recommend():
    book_name = request.form.get('user_input')
    try:
        index = np.where(pt.index==book_name)[0][0]
    except:
        return render_template('recommend.html',data='notfound', current_book= book_name)
    distances = list(enumerate(st[index]))
    sorted_distances = sorted(distances, key=lambda x:x[1], reverse=True)
    recoms = sorted_distances[1:11]
    rec_books = []
    
    for i in recoms:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-L'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Year-Of-Publication'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Publisher'].values))
        rec_books.append(item)
    
   
    return render_template('recommend.html',data=rec_books, current_book= book_name)

@app.route('/books/<book_name>')
def recommend_book(book_name): 
    try:
        index = np.where(pt.index==book_name)[0][0]
    except:
        return render_template('recommend.html',data='notfound', current_book= book_name)
    distances = list(enumerate(st[index]))
    sorted_distances = sorted(distances, key=lambda x:x[1], reverse=True)
    recoms = sorted_distances[1:11]
    rec_books = []
    
    for i in recoms:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-L'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Year-Of-Publication'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Publisher'].values))
        rec_books.append(item)
    
   
    return render_template('recommend.html',data=rec_books, current_book= book_name)

if __name__ == '__main__':
    app.run(debug=True)