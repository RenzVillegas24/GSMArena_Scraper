import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
import scipy.sparse as sp


phone_data = pd.read_csv('clean_phone_data.csv')

text_features = phone_data['details']
categorical_features = phone_data[['brand', 'os', 'has_cardslot', 'has_wifi', ]]
numerical_features = phone_data[['price_min', 'price_max', 'battery_size', 'battery_endurance', 'weight', 'release', 'screen_size', 'screen_resolution', 'camera_count_back', 'camera_count_front', 'benchmark_antutu', 'benchmark_geekbench', 'ram_min', 'ram_max', 'storage_min', 'storage_max', 'lazada_ratings', 'lazada_reviews',]]


# process tf-idf for text features
vectorizer = TfidfVectorizer(stop_words='english')
text_features_transformed = vectorizer.fit_transform(text_features)
print('tf__', text_features_transformed.shape)

# process tf-idf for each categorical text features ['colors', 'model', 'camera_resolution_back_recording', 'camera_resolution_front_recording', 'camera_list_resolution_back', 'camera_list_resolution_front', 'screen_type', 'gpu', 'build_material']
for feature in ['colors', 'model', 'camera_resolution_back_recording', 'camera_resolution_front_recording', 'camera_list_resolution_back', 'camera_list_resolution_front', 'screen_type', 'gpu', 'build_material']:
    vectorizer = TfidfVectorizer(stop_words='english')
    feature_transformed = vectorizer.fit_transform(phone_data[feature].str.replace('|', ' '))
    print('ft', feature_transformed.shape)
    text_features_transformed = sp.hstack((text_features_transformed, feature_transformed))

onehot_encoder = OneHotEncoder()
categorical_features_transformed = onehot_encoder.fit_transform(categorical_features)

print(categorical_features_transformed.shape)

scaler = StandardScaler()
numerical_features_transformed = scaler.fit_transform(numerical_features)

print(numerical_features_transformed.shape)




import scipy.sparse as sp

# Convert sparse matrix to dense for concatenation
text_features_dense = text_features_transformed.toarray()

# Combine all features
final_features = sp.hstack((text_features_dense, categorical_features_transformed, numerical_features_transformed))
