
import streamlit as st
import pandas as pd
import numpy as np
import pickle
import base64


with open("what-is-airbnb-thumbnail.jpg", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())
st.markdown(
f"""
<style>
.stApp {{
    background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
    background-size: cover
}}
</style>
""",
unsafe_allow_html=True
)

st.title("Check your Instant Bookable status")

st.markdown(":red[Tell us about your property 🏠]")

# Loading all encoding variables

# Amenities
with open('amenities_TFIDF.pkl','rb') as file:
    en_amenities = pickle.load(file)
    
# encoder_city

with open('encoder_city.pkl','rb') as file:
    en_city = pickle.load(file)
    
# encoder_host_response_time.pkl
with open('encoder_host_response_time.pkl','rb') as file:
    en_response_time = pickle.load(file)
    
#encoder_neighbourhood.pkl
with open('encoder_neighbourhood.pkl','rb') as file:
    en_neighbourhood = pickle.load(file)
    
# encoder_property_type.pkl
with open('encoder_property_type.pkl','rb') as file:
    en_property_type = pickle.load(file)
    
# encoder_region.pkl

with open('encoder_region.pkl','rb') as file:
    en_region = pickle.load(file)

# encoder_room_type.pkl
with open('encoder_room_type.pkl','rb') as file:
    en_room_type = pickle.load(file)
    
    
# Loading transformation
with open('accommodates.pkl','rb') as file:
    trans_accommodates = pickle.load(file)
    
with open('bedrooms.pkl','rb') as file:
    trans_bedroom = pickle.load(file)

with open('host_total_listings_count.pkl','rb') as file:
    trans_host_listing_count = pickle.load(file)
    
with open('minimum_nights.pkl','rb') as file:
    trans_min_nights = pickle.load(file)
    
with open('price.pkl','rb') as file:
    trans_price = pickle.load(file)
    
with open('review_scores_location.pkl','rb') as file:
    trans_re_location = pickle.load(file)
    
# Scaling

with open('scaling_host_acceptance_rate.pkl','rb') as file:
    scal_accet_rate = pickle.load(file)

with open('scaling_host_response_rate.pkl','rb') as file:
    scal_response_rate = pickle.load(file)
    
with open('scaling_longitude.pkl','rb') as file:
    scal_longitude = pickle.load(file)
    
with open('scaling_review_scores_rating.pkl','rb') as file:
    scal_re_rating = pickle.load(file)
    
    
#Load model
with open('Cat_boost.pkl','rb') as file:
    cat_boost = pickle.load(file)

    
# Getting user input

host_response_time = st.selectbox('Select response time',('unknown', 'within a day', 'within an hour', 'within a few hours',
       'a few days or more'))
host_response_rate = st.slider('Your response rate',1,100,1)
host_acceptance_rate = st.slider('Your acceptance rate',1,100,1)
host_is_superhost = st.selectbox('Your superhost status',('Yes','No'))
host_total_listings_count = st.number_input('Enter no. of properties listed',1,50,1)
host_identity_verified = st.selectbox('Do you want id verified status',('Yes','No'))
neighbourhood = st.selectbox('Select your neighbourhood',('Buttes-Montmartre', 'Elysee', 'Vaugirard', 'Passy', 'Temple',
       'Popincourt', 'Buttes-Chaumont', 'Opera', 'Gobelins',
       'Hotel-de-Ville', 'Pantheon', 'Enclos-St-Laurent',
       'Batignolles-Monceau', 'Luxembourg', 'Reuilly', 'Menilmontant',
       'Observatoire', 'Palais-Bourbon', 'Bourse', 'Louvre',
       'Lower East Side', 'Harlem', 'Crown Heights', 'Nolita', 'Midtown',
       'Greenwich Village', 'Williamsburg', 'East Village',
       'Upper West Side', "Hell's Kitchen", 'Park Slope', 'Chinatown',
       'Upper East Side', 'Columbia St', 'Inwood', 'Bedford-Stuyvesant',
       'Astoria', 'Little Italy', 'Fort Greene', 'Bushwick',
       'East Harlem', 'Washington Heights', 'Woodside', 'Greenpoint',
       'Ditmars Steinway', 'Sheepshead Bay', 'West Village',
       'Murray Hill', 'Prospect Heights', 'Brooklyn Heights',
       'Richmond Hill', 'Roosevelt Island', 'Flatiron District',
       'Ridgewood', 'Kips Bay', 'Chelsea', 'Battery Park City',
       'Long Island City', 'Flatbush', 'SoHo', 'Theater District',
       'Clinton Hill', 'Tribeca', 'Borough Park', 'Sunset Park',
       'Canarsie', 'Gramercy', 'Queens Village', 'DUMBO', 'Glendale',
       'Flushing', 'Jamaica', 'Prospect-Lefferts Gardens',
       'Downtown Brooklyn', 'Sunnyside', 'Windsor Terrace',
       'Financial District', 'East New York', 'Carroll Gardens',
       'Jackson Heights', 'Jamaica Estates', 'Morris Heights',
       'Boerum Hill', 'Vinegar Hill', 'Fort Hamilton', 'Woodhaven',
       'Maspeth', 'East Elmhurst', 'Flatlands', 'Ozone Park', 'Gowanus',
       'Cobble Hill', 'Morrisania', 'South Slope', 'St. George',
       'East Morrisania', 'Civic Center', 'Forest Hills', 'Cypress Hills',
       'Morningside Heights', 'Bayside', 'East Flatbush', 'Bay Ridge',
       'Kensington', 'Williamsbridge', 'Bensonhurst', 'NoHo', 'Midwood',
       "Prince's Bay", 'New Dorp', 'Stuyvesant Town', 'Two Bridges',
       'Concourse', 'Elmhurst', 'Kew Gardens', 'Norwood', 'Coney Island',
       'Kew Gardens Hills', 'Rego Park', 'Manhattan Beach',
       'Brighton Beach', 'Red Hook', 'Hunts Point', 'Mott Haven',
       'Gravesend', 'Longwood', 'Mount Eden', 'Middle Village',
       'Dyker Heights', 'Corona', 'Randall Manor', 'Bath Beach',
       'Parkchester', 'Kingsbridge', 'Hollis', 'Highbridge', 'Navy Yard',
       'Riverdale', 'Wakefield', 'Bronxdale', 'Arverne', 'Brownsville',
       'Mariners Harbor', 'Tompkinsville', 'Port Morris', 'Briarwood',
       'Tremont', 'Great Kills', 'Springfield Gardens', 'Arden Heights',
       'St. Albans', 'Spuyten Duyvil', 'Eastchester', 'Arrochar',
       'Mount Hope', 'Far Rockaway', 'Castleton Corners', 'Dongan Hills',
       'Van Nest', 'Stapleton', 'Laurelton', 'Unionport',
       'Rockaway Beach', 'South Ozone Park', 'Jamaica Hills',
       'Pelham Gardens', 'North Riverdale', "Bull's Head", 'Douglaston',
       'Morris Park', 'City Island', 'Oakwood', 'Bellerose',
       'College Point', 'Grymes Hill', 'Rosedale', 'Claremont Village',
       'Todt Hill', 'University Heights', 'Soundview', 'Howard Beach',
       'Woodlawn', 'Fieldston', 'Edenwald', 'Fresh Meadows',
       'Silver Lake', 'Graniteville', 'Grant City', 'Pelham Bay',
       'Lighthouse Hill', 'Baychester', 'Westerleigh', 'Concord',
       'New Springville', 'Cambria Heights', 'Clason Point', 'Allerton',
       'Willowbrook', 'Belle Harbor', 'Holliswood', 'Shore Acres',
       'Marble Hill', 'Little Neck', 'Sea Gate', 'West Brighton',
       'Concourse Village', 'New Brighton', 'Bayswater', 'Howland Hook',
       'Woodrow', 'Throgs Neck', 'Emerson Hill', 'Eltingville', 'Clifton',
       'Fordham', 'Whitestone', 'Westchester Square', 'Port Richmond',
       'Midland Beach', 'Rosebank', 'Edgemere', 'Mill Basin',
       'Co-op City', 'Olinville', 'Belmont', 'Bay Terrace', 'Melrose',
       'West Farms', 'New Dorp Beach', 'Bergen Beach', 'Huguenot',
       'Schuylerville', 'South Beach', 'Gerritsen Beach', 'Country Club',
       'Richmondtown', 'Fort Wadsworth', 'Tottenville', 'Rossville',
       'Castle Hill', 'Vadhana', 'Khlong Toei', 'Lat Krabang',
       'Rat Burana', 'Sathon', 'Bang Sue', 'Yan na wa', 'Chatu Chak',
       'Bang Kapi', 'Phasi Charoen', 'Bang Phlat', 'Khlong San',
       'Ratchathewi', 'Huai Khwang', 'Bang Na', 'Phra Khanong',
       'Din Daeng', 'Pra Wet', 'Bang Kho laen', 'Thon buri', 'Bang Rak',
       'Sai Mai', 'Parthum Wan', 'Bangkok Noi', 'Wang Thong Lang',
       'Don Mueang', 'Bang Khen', 'Bang Khae', 'Phra Nakhon', 'Suanluang',
       'Bueng Kum', 'Phaya Thai', 'Khan Na Yao', 'Bangkok Yai',
       'Chom Thong', 'Thawi Watthana', 'Taling Chan', 'Lak Si',
       'Bang Khun thain', 'Saphan Sung', 'Nong Khaem', 'Khlong Sam Wa',
       'Lat Phrao', 'Samphanthawong', 'Dusit', 'Pom Prap Sattru Phai',
       'Min Buri', 'Thung khru', 'Nong Chok', 'Bang Bon', 'Leblon',
       'Ipanema', 'Copacabana', 'Humaita', 'Recreio dos Bandeirantes',
       'Leme', 'Barra da Tijuca', 'Tijuca', 'Botafogo', 'Laranjeiras',
       'Centro', 'Flamengo', 'Catete', 'Vila Isabel', 'Gloria',
       'Jacarepagua', 'Camorim', 'Santa Teresa', 'Lagoa', 'Campo Grande',
       'Rio Comprido', 'Gavea', 'Sao Francisco Xavier', 'Sao Conrado',
       'Maracana', 'Cidade de Deus', 'Praca da Bandeira', 'Pechincha',
       'Jardim Botanico', 'Freguesia (Jacarepagua)', 'Grajau', 'Urca',
       'Cosme Velho', 'Riachuelo', 'Benfica', 'Curicica', 'Taquara',
       'Engenho de Dentro', 'Higienopolis', 'Engenho da Rainha',
       'Quintino Bocaiuva', 'Senador Vasconcelos', 'Cosmos', 'Encantado',
       'Sampaio', 'Pilares', 'Piedade', 'Cidade Nova', 'Andarai',
       'Engenho Novo', 'Sao Cristovao', 'Itanhanga', 'Mangueira',
       'Gardenia Azul', 'Praca Seca', 'Rocha', 'Campinho', 'Guaratiba',
       'Joa', 'Realengo', 'Todos os Santos', 'Guadalupe',
       'Parada de Lucas', 'Pavuna', 'Estacio', 'Jardim Guanabara', 'Anil',
       'Freguesia (Ilha)', 'Vargem Pequena', 'Meier', 'Saude',
       'Vargem Grande', 'Vidigal', 'Rocinha', 'Inhoaiba', 'Santa Cruz',
       'Bancarios', 'Lins de Vasconcelos', 'Zumbi', 'Madureira',
       'Paqueta', 'Tanque', 'Vicente de Carvalho', 'Abolicao',
       'Portuguesa', 'Cachambi', 'Iraja', 'Jardim Carioca',
       'Tomas Coelho', 'Penha Circular', 'Barra de Guaratiba',
       'Del Castilho', 'Sepetiba', 'Ribeira', 'Vila da Penha',
       'Ricardo de Albuquerque', 'Vigario Geral', 'Bonsucesso', 'Ramos',
       'Monero', 'Taua', 'Bras de Pina', 'Gamboa', 'Maria da Graca',
       'Bangu', 'Vasco da Gama', 'Santissimo', 'Jardim Sulacap', 'Penha',
       'Magalhaes Bastos', 'Bento Ribeiro', 'Alto da Boa Vista',
       'Pedra de Guaratiba', 'Paciencia', 'Catumbi', 'Pitangueiras',
       'Cacuia', 'Vila Valqueire', 'Honorio Gurgel', 'Galeao',
       'Vila Militar', 'Padre Miguel', 'Grumari', 'Manguinhos',
       'Rocha Miranda', 'Cascadura', 'Olaria', 'Coelho Neto', 'Vaz Lobo',
       'Anchieta', 'Praia da Bandeira', 'Marechal Hermes', 'Inhauma',
       'Jacare', 'Parque Anchieta', 'Cordovil', 'Cocota',
       'Cidade Universitaria', 'Gericino', 'Santo Cristo', 'Barros Filho',
       'Vista Alegre', 'Cavalcanti', 'Senador Camara',
       'Complexo do Alemao', 'Deodoro', 'Vila Kosmos', 'Osvaldo Cruz',
       'Mare', 'Acari', 'Agua Santa', 'Waverley', 'North Sydney',
       'Parramatta', 'Ryde', 'Sydney', 'Rockdale', 'Manly', 'Warringah',
       'Randwick', 'Hurstville', 'Pittwater', 'Canterbury',
       'City Of Kogarah', 'Fairfield', 'Woollahra', 'Auburn', 'Ashfield',
       'Bankstown', 'Sutherland Shire', 'Willoughby', 'Hornsby',
       'Marrickville', 'Liverpool', 'Leichhardt', 'Mosman', 'Botany Bay',
       'Canada Bay', 'Burwood', 'Blacktown', 'Strathfield',
       'The Hills Shire', 'Hunters Hill', 'Ku-Ring-Gai', 'Lane Cove',
       'Holroyd', 'Penrith', 'Camden', 'Campbelltown', 'Adalar',
       'Uskudar', 'Sisli', 'Beyoglu', 'Kadikoy', 'Sariyer', 'Besiktas',
       'Pendik', 'Maltepe', 'Bakirkoy', 'Bagcilar', 'Fatih', 'Eyup',
       'Beylikduzu', 'Basaksehir', 'Esenyurt', 'Bayrampasa',
       'Buyukcekmece', 'Kucukcekmece', 'Umraniye', 'Avcilar', 'Kartal',
       'Zeytinburnu', 'Kagithane', 'Atasehir', 'Silivri', 'Gaziosmanpasa',
       'Beykoz', 'Sancaktepe', 'Sultangazi', 'Bahcelievler', 'Gungoren',
       'Cekmekoy', 'Tuzla', 'Sultanbeyli', 'Arnavutkoy', 'Sile',
       'Esenler', 'Catalca', 'I Centro Storico', 'II Parioli/Nomentano',
       'IV Tiburtina', 'V Prenestino/Centocelle',
       'VII San Giovanni/Cinecitta', 'XIII Aurelia', 'III Monte Sacro',
       'X Ostia/Acilia', 'XV Cassia/Flaminia', 'VIII Appia Antica',
       'XIV Monte Mario', 'XII Monte Verde', 'IX Eur',
       'XI Arvalia/Portuense', 'VI Roma delle Torri', 'Southern',
       'Yau Tsim Mong', 'Islands', 'Wan Chai', 'Central & Western',
       'Sham Shui Po', 'Kowloon City', 'Eastern', 'Yuen Long',
       'Tsuen Wan', 'Wong Tai Sin', 'North', 'Sha Tin', 'Sai Kung',
       'Kwun Tong', 'Kwai Tsing', 'Tuen Mun', 'Tai Po',
       'A\x81lvaro Obregon', 'Coyoacan', 'Benito Juarez', 'Cuauhtemoc',
       'Azcapotzalco', 'Miguel Hidalgo', 'Cuajimalpa de Morelos',
       'Iztacalco', 'Venustiano Carranza', 'Tlahuac', 'Tlalpan',
       'Iztapalapa', 'La Magdalena Contreras', 'Gustavo A. Madero',
       'Xochimilco', 'Milpa Alta', 'Ward 115', 'Ward 3', 'Ward 77',
       'Ward 55', 'Ward 64', 'Ward 54', 'Ward 59', 'Ward 61', 'Ward 113',
       'Ward 105', 'Ward 8', 'Ward 15', 'Ward 100', 'Ward 74', 'Ward 27',
       'Ward 84', 'Ward 71', 'Ward 107', 'Ward 83', 'Ward 11', 'Ward 62',
       'Ward 73', 'Ward 23', 'Ward 53', 'Ward 21', 'Ward 69', 'Ward 1',
       'Ward 57', 'Ward 58', 'Ward 70', 'Ward 60', 'Ward 85', 'Ward 4',
       'Ward 86', 'Ward 2', 'Ward 10', 'Ward 103', 'Ward 109', 'Ward 112',
       'Ward 48', 'Ward 66', 'Ward 5', 'Ward 102', 'Ward 43', 'Ward 14',
       'Ward 67', 'Ward 7', 'Ward 20', 'Ward 63', 'Ward 46', 'Ward 44',
       'Ward 26', 'Ward 30', 'Ward 72', 'Ward 56', 'Ward 9', 'Ward 104',
       'Ward 116', 'Ward 94', 'Ward 65', 'Ward 78', 'Ward 22', 'Ward 17',
       'Ward 108', 'Ward 51', 'Ward 32', 'Ward 49', 'Ward 92', 'Ward 19',
       'Ward 75', 'Ward 110', 'Ward 68', 'Ward 12', 'Ward 76', 'Ward 93',
       'Ward 16', 'Ward 31', 'Ward 6', 'Ward 50', 'Ward 91', 'Ward 81',
       'Ward 29', 'Ward 25', 'Ward 28', 'Ward 82', 'Ward 111', 'Ward 101',
       'Ward 41', 'Ward 96', 'Ward 38', 'Ward 45', 'Ward 18', 'Ward 40'))
    

city = st.selectbox('Select city',('Paris', 'New York', 'Bangkok', 'Rio de Janeiro', 'Sydney',
       'Istanbul', 'Rome', 'Hong Kong', 'Mexico City', 'Cape Town'))

property_type = st.selectbox('Select your property type',('Entire apartment', 'Entire loft', 'Entire house',
       'Entire condominium', 'Private room in apartment',
       'Private room in condominium', 'Entire guest suite', 'Earth house',
       'Entire townhouse', 'Room in serviced apartment',
       'Private room in bed and breakfast', 'Entire serviced apartment',
       'Private room in house', 'Entire villa', 'Tiny house',
       'Private room in guest suite', 'Private room in loft',
       'Room in boutique hotel', 'Entire place', 'Room in hotel',
       'Entire floor', 'Entire guesthouse', 'Houseboat', 'Entire cottage',
       'Boat', 'Private room in guesthouse', 'Entire home/apt',
       'Room in bed and breakfast', 'Room in aparthotel',
       'Private room in villa', 'Private room in cabin',
       'Shared room in apartment', 'Private room in townhouse',
       'Private room in chalet', 'Entire bed and breakfast', 'Cave',
       'Shared room in condominium', 'Private room in boat',
       'Shared room in serviced apartment', 'Shared room in hostel',
       'Entire bungalow', 'Private room',
       'Private room in serviced apartment',
       'Private room in earth house', 'Campsite', 'Shared room in loft',
       'Shared room in cabin', 'Room in hostel',
       'Shared room in bed and breakfast', 'Private room in hostel',
       'Shared room in boutique hotel', 'Private room in houseboat',
       'Shared room in house', 'Shared room in townhouse',
       'Shared room in igloo', 'Treehouse',
       'Private room in casa particular', 'Shared room in tiny house',
       'Shared room in guesthouse', 'Shared room in guest suite',
       'Entire chalet', 'Private room in nature lodge', 'Island',
       'Dome house', 'Camper/RV', 'Barn', 'Casa particular',
       'Private room in resort', 'Private room in tiny house',
       'Private room in camper/rv', 'Private room in barn',
       'Private room in tent', 'Private room in bungalow',
       'Private room in dome house', 'Private room in castle',
       'Shared room in floor', 'Shared room in bungalow',
       'Private room in in-law', 'Private room in farm stay',
       'Private room in lighthouse', 'Bus', 'Shared room in island',
       'Private room in cottage', 'Entire resort',
       'Shared room in earth house', 'Private room in dorm',
       'Room in resort', 'Private room in floor', 'Private room in train',
       'Lighthouse', 'Castle', 'Farm stay', 'Private room in island',
       'Entire dorm', 'Entire cabin', 'Private room in kezhan',
       'Shared room in dorm', 'Shared room in kezhan', 'Entire hostel',
       'Shared room in chalet', 'Shared room in cave',
       'Shared room in villa', 'Private room in hut',
       'Shared room in parking space', 'Shared room in dome house',
       'Shared room', 'Shared room in casa particular',
       'Private room in tipi', 'Room in nature lodge',
       'Private room in holiday park', 'Pension',
       'Shared room in cottage', 'Shared room in farm stay', 'Hut',
       'Shared room in nature lodge', 'Private room in treehouse',
       'Shared room in castle', 'Entire vacation home', 'Yurt',
       'Room in apartment', 'Private room in minsu',
       'Private room in pension', 'Private room in yurt', 'Tent', 'Train',
       'Shared room in tent', 'Shared room in boat',
       'Private room in bus', 'Holiday park', 'Room in casa particular',
       'Shared room in yurt', 'Private room in pousada',
       'Shared room in pension', 'Shared room in aparthotel',
       'Shared room in hotel', 'Room in pension', 'Igloo', 'Tipi',
       'Shared room in hut', 'Entire in-law', 'Private room in cave',
       'Room in guesthouse', 'Room in heritage hotel'))
room_type = st.selectbox('Select Room type',('Entire place', 'Private room', 'Hotel room', 'Shared room'))

accommodates = st.number_input('No. of people can be accommodated',1,16,1)

bedrooms = st.number_input('No.of bedrooms',1,20,1)

price = st.number_input('Price')

min_nights = st.slider('Minimum nights allowed',1,50,1)

region = st.selectbox('Enter your region',('East', 'North', 'West', 'South'))

amenities = st.multiselect('Select amenities',('long term stay','parking','hanger','hair dryer','tv','wifi','iron','washer','water heating','workspace','kitchen essential',
'fire alarm'))


# Applying encoding ,transformation,scaling on user data

encode_res_time = en_response_time.transform(pd.DataFrame([host_response_time]))
scale_res_rate = scal_response_rate.transform(pd.DataFrame([host_response_rate]))
scale_act_rate = scal_accet_rate.transform(pd.DataFrame([host_acceptance_rate]))
encode_superhost = [1 if host_is_superhost == "Yes" else 0]
trans_list_count = trans_host_listing_count.transform(pd.DataFrame([host_total_listings_count]))
encode_id_verified = [1 if host_identity_verified == "Yes" else 0]
encode_neighbourhood = en_neighbourhood.transform(pd.DataFrame({"neighbourhood" :[neighbourhood]}))
encode_city = en_city.transform(pd.DataFrame({"city" :[city]}))
encode_property_type = en_property_type.transform(pd.DataFrame({"property_type" :[property_type]}))
encode_room_type = en_room_type.transform(pd.DataFrame([room_type]))
trans_acc = trans_accommodates.transform(pd.DataFrame([accommodates]))
trans_bed = trans_bedroom.transform(pd.DataFrame([bedrooms]))
trans_pri = trans_price.transform(pd.DataFrame([price]))
trans_min = trans_min_nights.transform(pd.DataFrame([min_nights]))
encode_region = en_region.transform(pd.DataFrame({'Region':[region]}))


data_1 = {'host_response_time' : encode_res_time[0],
        'host_response_rate': scale_res_rate[0]/100,
        'host_acceptance_rate':scale_act_rate[0]/100,
       'host_is_superhost' : encode_superhost[0],
       'host_total_listings_count':trans_list_count[0],
       'host_identity_verified':encode_id_verified[0],
       'neighbourhood' : encode_neighbourhood.iloc[0,0],
       'city' : encode_city.iloc[0,0],
       'property_type' : encode_property_type.iloc[0,0],
       'room_type' : encode_room_type[0],
       'accommodates' : trans_acc[0],
       'bedrooms' : trans_bed[0],
       'price' : trans_pri[0],
       'minimum_nights' : trans_min[0],
       'review_scores_rating' : scal_re_rating.transform(pd.DataFrame([55]))[0],
       'review_scores_location' : trans_re_location.transform(pd.DataFrame([50]))[0],
       'Region' : encode_region.iloc[0,0]}
data_1 = pd.DataFrame(data_1)

data_2 = en_amenities.transform([' '.join(amenities)]).toarray()
data_2 = pd.DataFrame(data_2,columns=en_amenities.get_feature_names_out())

df = pd.concat([data_1,data_2],axis=1)

# Model prediction
prediction = cat_boost.predict(df)
if st.button('predict'):
    if prediction ==1 :
        st.success('Your property is instantly bookable')
    else:
        st.error('Please increase the quality of the property to get instant bookable status')
