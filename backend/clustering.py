
from dataColectionFunctions import getAccessTokenCC
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA
from sklearn.neighbors import kneighbors_graph

data = pd.read_csv('FinalDB.csv')
data1 = pd.read_csv('FinalDB.csv')
del data1['id']
del data1['popularity']
data1 = data1.to_numpy()

#Spectral CLustering was too expensive and didn't have enough of an increase in accuracy to justify using it over 
#kmeans clustering
def spectralClustering():
    A = kneighbors_graph(data1, n_neighbors=10).toarray()
    D = np.diag(A.sum(axis=1))
    L = D-A
    vals, vecs = np.linalg.eig(L)
    vecs = vecs[:,np.argsort(vals)]
    vals = vals[np.argsort(vals)]
    clusters = vecs[:,1] > 0
    return clusters





pca = PCA().fit(data1)
arr = pca.explained_variance_ratio_
variance = 0
for i in range(len(arr)):
    if variance > .80:
        break
    idx = i
    variance += arr[i]

pca = PCA(n_components = idx)
pca.fit(data1)
arr = pca.transform(data1)




def elbowMethod(data):
    wss = []
    sil = []
    for k in range(2, 21):
        kmeans = KMeans(n_clusters = k, n_init='auto').fit(data)
        labels = kmeans.labels_
        sil.append(silhouette_score(data, labels, metric = 'euclidean'))
        centroids = kmeans.cluster_centers_
        predClusters = kmeans.predict(data)
        currWss = 0


        for i in range(len(data)):
            currCenter = centroids[predClusters[i]]
            currWss += np.linalg.norm(currCenter - data[i,:])

        wss.append(currWss)
    
    # for currWss in ran

    return wss



kmeans = KMeans(n_clusters = 10, n_init=10).fit(arr)
centroids = kmeans.cluster_centers_
predClusters = kmeans.predict(arr)

data['Cluster'] = predClusters

closest = [(float('inf'), 0)] * 10
for i in range(len(arr)):
    cl = data.loc[i]['Cluster']
    dist = np.linalg.norm(centroids[cl] - arr[i,:])
    if dist < closest[cl][0]:
        closest[cl] = (dist, i)

closestDF = data.loc[[closest[0][1],closest[1][1],closest[2][1],closest[3][1],closest[4][1],closest[5][1],closest[6][1],closest[7][1],closest[8][1],closest[9][1]]]
closestDF.to_csv('ClosestDB.csv', index = False)

data.to_csv('FinalDF.csv', index = False)

for i in range(10):
    copy = data.loc[data['Cluster'] == i]
    copy.to_csv(f'cluster{i}.csv', index = False)
