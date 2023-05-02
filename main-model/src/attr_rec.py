import pandas as pd
import numpy as np
import ipywidgets as w
from ipywidgets import HBox, VBox
from ipywidgets import Layout, widgets
from IPython.display import display, IFrame, HTML
from utils import Util
from rbm import RBM
import math, re, datetime as dt, glob
from urllib.parse import quote
from urllib.request import Request, urlopen
from google_images_download import google_images_download
from PIL import Image
from nltk.corpus import wordnet
import constants as const



def f(row):
    avg_cat_rat = dict()
    for i in range(len(row['category'])):
        if row['category'][i] not in avg_cat_rat:
            avg_cat_rat[row['category'][i]] = [row['rating'][i]]
        else:
            avg_cat_rat[row['category'][i]].append(row['rating'][i])
    for key,value in avg_cat_rat.items():
        avg_cat_rat[key] = sum(value)/len(value)
    return avg_cat_rat



def sim_score(row):
    score = 0.0
    match = 0
    col1 = row['cat_rat']
    col2 = row['user_data']
    for key, value in col2.items():
        if key in col1:
            match+=1
            score += (value-col1[key])**2
    if match != 0:
        return ((math.sqrt(score)/match) + (len(col2) - match))
    else:
        return 100



def get_recc(att_df, cat_rating):
    util = Util()
    epochs = 20
    rows = 5000
    alpha = 0.01
    H = 128
    batch_size = 16

    # epochs = 20
    # rows = 5000
    # alpha = 0.01
    # H = 128
    # batch_size = 8

    dir = const.DIR_DATA_ATTR
    attractions_filename = const.ATTR_FILENAME
    ratings_attr_filename = const.RATING_ATTR_FILENAME

    attractions = util.read_data(dir, attractions_filename)
    ratings = util.read_data(dir, ratings_attr_filename)

    ratings = util.clean_subset(ratings, rows)
    rbm_att, train = util.preprocess(ratings)
    num_vis =  len(ratings)
    rbm = RBM(alpha, H, num_vis)
    
    # Join 2 DF ratings và attractions (lấy thêm cột category cho ratings và sắp xếp lại theo attraction_id)
    joined = ratings.set_index('attraction_id').join(attractions[["attraction_id", "category"]].set_index("attraction_id")).reset_index('attraction_id')

    # Nhóm joined lại theo user_id
    grouped = joined.groupby('user_id')

    # DF về category lấy từ grouped 
    # (mỗi hàng của DF tương ứng với 1 user_id khác nhau)
    # (nghĩa là ứng với mỗi một người dùng khác nhau)
    # (cột category là một list gồm các danh mục du lịch mà user đó đã xếp hạng)
    category_df = grouped['category'].apply(list).reset_index()
    
    # DF về ratings lấy từ grouped
    # (ý nghĩa tương tự DF về category)
    rating_df = grouped['rating'].apply(list).reset_index()
    
    # Gộp lại của category_df và rating_df
    cat_rat_df = category_df.set_index('user_id').join(rating_df.set_index('user_id'))
    
    # vẫn là cat_rat_df nhưng có thêm cột cat_rat
    # cột này là một dict, có cấu trúc tương tự cat_rating
    # cột này là tổng hợp lại 2 cột còn lại, 
    # các key là các giá trị phân biệt của cột category, 
    # các giá trị là trung bình cộng của cột rating ứng với từng category
    cat_rat_df['cat_rat'] = cat_rat_df.apply(f,axis=1)

    # cat_rat_df giờ chỉ có 2 cột user_id và cat_rat
    cat_rat_df = cat_rat_df.reset_index()[['user_id','cat_rat']]
    
    # cat_rat_df giờ có thêm cột user_data lấy từ cat_rating là input từ phía người dùng hiện tại
    cat_rat_df['user_data'] = [cat_rating for i in range(len(cat_rat_df))]
    
    # cat_rat_df giờ có thêm cột sim_score, 
    # giá trị cột này tính thông qua hàm sim_score() ở phía trên
    # tham số là các giá trị của các cột cat_rat và user_data
    # sim_score là Simple matching score => đánh giá mức độ tương đồng của 2 dict trong trường hợp này
    # sim_score càng nhỏ thì càng tương đồng (theo cách tính của hàm sim_score() phía trên)
    cat_rat_df['sim_score'] = cat_rat_df.apply(sim_score, axis=1)

    # Lấy ra id của user có sim_score nhỏ nhất (tương đồng với người dùng hiện tại nhất)
    user = cat_rat_df.sort_values(['sim_score']).values[0][0]
    
    print("Similar User: {u}".format(u=user))
    filename = "e"+str(epochs)+"_r"+str(rows)+"_lr"+str(alpha)+"_hu"+str(H)+"_bs"+str(batch_size)
    
    # 
    reco, weights, vb, hb = rbm.load_predict(filename,train,user)
    
    # tạo file csv từ reco để phục vụ cho filter_df()
    # unseen là kiểu gợi ý tự vẽ ra những chỗ CÓ THỂ thích (vì là unseen)
    # seen là kiểu gợi ý những chỗ khá chắc chắn như ý (vì đã seen rồi)
    unseen, seen = rbm.calculate_scores(ratings, attractions, reco, user)
    rbm.export(unseen, seen, const.DIR_RBM_MODELS + filename, str(user))
    
    return filename, user, rbm_att


def filter_df(filename, user, low, high, city, att_df):
    # recc_df này chứa att_id, att_name, att_cat và att_price
    # có thể lấy theo cái seen hoặc unseen
    # nếu lấy unseen thì có thêm cột score

    # recc_df = pd.read_csv(const.DIR_RBM_MODELS + filename + '/user{u}_unseen.csv'.format(u=user), index_col=0)
    recc_df = pd.read_csv(const.DIR_RBM_MODELS + filename + '/user{u}_seen.csv'.format(u=user), index_col=0)
    
    # recc_df.columns = ['attraction_id', 'att_name', 'att_cat', 'att_price', 'score']
    recc_df.columns = ['attraction_id', 'att_name', 'att_cat', 'att_price']

    # att_df là DF raw lấy từ file attractions.json
    # recommendation là kiểu kết hợp att_df với recc_df
    # recommendation = att_df[['attraction_id','name','category','city','latitude','longitude','avg_price', 'rating']].set_index('attraction_id').join(recc_df[['attraction_id','score']].set_index('attraction_id'), how="inner").reset_index().sort_values("score",ascending=False)
    recommendation = att_df[['attraction_id','name','category','city','latitude','longitude','avg_price', 'rating']].set_index('attraction_id').join(recc_df[['attraction_id']].set_index('attraction_id'), how="inner").reset_index() # đang chưa biết sort theo cái chiiii
    
    unseen_recc_df = pd.read_csv(const.DIR_RBM_MODELS + filename + '/user{u}_unseen.csv'.format(u=user), index_col=0)
    unseen_recc_df.columns = ['attraction_id', 'att_name', 'att_cat', 'att_price', 'score']
    unseen_recommendation = att_df[['attraction_id','name','category','city','latitude','longitude','avg_price', 'rating']].set_index('attraction_id').join(unseen_recc_df[['attraction_id','score']].set_index('attraction_id'), how="inner").reset_index().sort_values("score",ascending=False)
    unseen_recommendation.pop('score')

    final_recommendation = pd.concat([recommendation, unseen_recommendation])

    filtered = final_recommendation[(final_recommendation.city == city) & (final_recommendation.avg_price >= low) & (final_recommendation.avg_price <= high)]

    return filtered



def get_image(name):
    name = name.split(",")[0]
    response = google_images_download.googleimagesdownload()
    args_list = ["keywords", "keywords_from_file", "prefix_keywords", "suffix_keywords",
             "limit", "format", "color", "color_type", "usage_rights", "size",
             "exact_size", "aspect_ratio", "type", "time", "time_range", "delay", "url", "single_image",
             "output_directory", "image_directory", "no_directory", "proxy", "similar_images", "specific_site",
             "print_urls", "print_size", "print_paths", "metadata", "extract_metadata", "socket_timeout",
             "thumbnail", "language", "prefix", "chromedriver", "related_images", "safe_search", "no_numbering",
             "offset", "no_download"]
    args = {}
    for i in args_list:
        args[i]= None
    args["keywords"] = name
    args['limit'] = 1
    params = response.build_url_parameters(args)
    url = 'https://www.google.com/search?q=' + quote(name) + '&espv=2&biw=1366&bih=667&site=webhp&source=lnms&tbm=isch' + params + '&sa=X&ei=XosDVaCXD8TasATItgE&ved=0CAcQ_AUoAg'
    try:
        response.download(args)
        
        for filename in glob.glob("downloads/{name}/*jpg".format(name=name)) + glob.glob("downloads/{name}/*png".format(name=name)):
            return filename
    except:
        for filename in glob.glob("downloads/*jpg"):
            return filename



def top_recc(filtered, final):
    i=0
    while(1):
        if i >= filtered.shape[0]:
            # todo: do something to fill the final
            # final.append()
            return final
        
        first_recc = filtered.iloc[[i]]

        if(first_recc['name'].values.T[0] not in final['name']):
            final['name'].append(first_recc['name'].values.T[0])
            final['location'].append(first_recc[['latitude','longitude']].values.tolist()[0])
            final['avg_price'].append(first_recc['avg_price'].values.T[0])
            final['rating'].append(first_recc['rating'].values.T[0])
            final['image'].append(get_image(first_recc['name'].values.T[0]))
            final['category'].append(first_recc['category'].values.T[0])
            return final
        else:
            i+=1


'''
Xác định khoảng cách các địa điểm để chọn những địa điểm gần nhau trong cùng 1 ngày
'''
def find_closest(filtered, loc, tod, final):
    # todo: wordnet dùng để tạo ra các từ liên quan tới 'evening' và 'night' nhưng hiện tại chưa cần dùng đến
    # syns1 = wordnet.synsets("evening")
    # syns2 = wordnet.synsets("night")
    # evening = [word.lemmas()[0].name() for word in syns1] + [word.lemmas()[0].name() for word in syns2]
        
    distance = list()
    for i in filtered[['latitude','longitude']].values.tolist():
        distance.append(math.sqrt((loc[0]-i[0])**2 + (loc[1]-i[1])**2))
    with_dist = filtered
    with_dist["distance"] = distance
    sorted_d = with_dist.sort_values(['distance','avg_price'], ascending=[True, False])

    # if tod == "Evening":
    #     mask = sorted_d.name.apply(lambda x: any(j in x for j in evening))
    # else:
    #     mask = sorted_d.name.apply(lambda x: all(j not in x for j in evening))

    final = top_recc(sorted_d, final)
    return final



def final_output(days, final):
    time = ['MORNING', 'EVENING']
    fields = ['NAME', 'CATEGORY', 'LOCATION', 'AVG_PRICE', 'RATING']
    recommendations = ['Recommendation 1:', 'Recommendation 2:']

    box_layout = Layout(justify_content='space-between',
                        display='flex',
                        flex_flow='row', 
                        align_items='stretch',
                       )
    column_layout = Layout(justify_content='space-between',
                        width='75%',
                        display='flex',
                        flex_flow='column', 
                       )
    tab = []
    for i in range(days):
        images = final['image'][i*4:(i+1)*4]

        # check None in images
        images = list(map(lambda item: const.DIR_NO_IMAGE if item is None else item, images))

        if len(images) < 4:
            while len(images) < 4:
                images.append(const.DIR_NO_IMAGE)

        images = [open(i, "rb").read() for i in images]
        name = [re.sub('_',' ',i).capitalize() for i in final['name'][i*4:(i+1)*4]]

        print('name:')
        print(i)
        print(name)
        print('\n')

        category = [re.sub('_',' ',i).capitalize() for i in final['category'][i*4:(i+1)*4]]
        location = ["("+str(i[0])+","+str(i[1])+")" for i in final['location'][i*4:(i+1)*4]]
        avg_price = [str(i) for i in final['avg_price'][i*4:(i+1)*4]]
        rating = [str(i) for i in final['rating'][i*4:(i+1)*4]]
        tab.append(VBox(children=
                        [HBox(children=
                              [VBox(children=
                                    [widgets.HTML(value = f"<b><font color='orange'>{time[0]}</b>"),
                                     widgets.HTML(value = f"<b><font color='purple'>{recommendations[0]}</b>"),
                                     widgets.Image(value=images[0], format='jpg', width=300, height=400), 
                                     widgets.HTML(description=fields[0], value=f"<b><font color='black'>{name[0]}</b>", disabled=True), 
                                     widgets.HTML(description=fields[1], value=f"<b><font color='black'>{category[0]}</b>", disabled=True),
                                     widgets.HTML(description=fields[2], value=f"<b><font color='black'>{location[0]}</b>", disabled=True), 
                                     widgets.HTML(description=fields[3], value=f"<b><font color='black'>{avg_price[0]}</b>", disabled=True), 
                                     widgets.HTML(description=fields[4], value=f"<b><font color='black'>{rating[0]}</b>", disabled=True)
                                    ], layout=column_layout), 
                                VBox(children=
                                    [widgets.HTML(value = f"<b><font color='orange'>{time[1]}</b>"), 
                                     widgets.HTML(value = f"<b><font color='purple'>{recommendations[0]}</b>"),
                                     widgets.Image(value=images[2], format='jpg', width=300, height=400), 
                                     widgets.HTML(description=fields[0], value=f"<b><font color='black'>{name[2]}</b>", disabled=True), 
                                     widgets.HTML(description=fields[1], value=f"<b><font color='black'>{category[2]}</b>", disabled=True),
                                     widgets.HTML(description=fields[2], value=f"<b><font color='black'>{location[2]}</b>", disabled=True), 
                                     widgets.HTML(description=fields[3], value=f"<b><font color='black'>{avg_price[2]}</b>", disabled=True), 
                                     widgets.HTML(description=fields[4], value=f"<b><font color='black'>{rating[2]}</b>", disabled=True)
                                    ], layout=column_layout)
                              ], layout=box_layout),

                         HBox(children=
                              [VBox(children=
                                    [widgets.HTML(value = f"<b><font color='purple'>{recommendations[1]}</b>"),
                                     widgets.Image(value=images[1], format='jpg', width=300, height=400), 
                                     widgets.HTML(description=fields[0], value=f"<b><font color='black'>{name[1]}</b>", disabled=True), 
                                     widgets.HTML(description=fields[1], value=f"<b><font color='black'>{category[1]}</b>", disabled=True),
                                     widgets.HTML(description=fields[2], value=f"<b><font color='black'>{location[1]}</b>", disabled=True), 
                                     widgets.HTML(description=fields[3], value=f"<b><font color='black'>{avg_price[1]}</b>", disabled=True), 
                                     widgets.HTML(description=fields[4], value=f"<b><font color='black'>{rating[1]}</b>", disabled=True)
                                    ], layout=column_layout), 
                                VBox(children=
                                    [widgets.HTML(value = f"<b><font color='purple'>{recommendations[1]}</b>"),
                                     widgets.Image(value=images[3], format='jpg', width=300, height=400), 
                                     widgets.HTML(description=fields[0], value=f"<b><font color='black'>{name[3]}</b>", disabled=True), 
                                     widgets.HTML(description=fields[1], value=f"<b><font color='black'>{category[3]}</b>", disabled=True),
                                     widgets.HTML(description=fields[2], value=f"<b><font color='black'>{location[3]}</b>", disabled=True), 
                                     widgets.HTML(description=fields[3], value=f"<b><font color='black'>{avg_price[3]}</b>", disabled=True), 
                                     widgets.HTML(description=fields[4], value=f"<b><font color='black'>{rating[3]}</b>", disabled=True)
                                    ], layout=column_layout),
                              ], layout=box_layout)

                        ]))

    tab_recc = widgets.Tab(children=tab)
    for i in range(len(tab_recc.children)):
        tab_recc.set_title(i, str('Day '+ str(i+1)))
    return tab_recc
