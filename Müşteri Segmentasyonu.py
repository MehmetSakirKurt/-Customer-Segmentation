#gerekli kütüphaneleri import ettik projemizde kullanmamız gereken k means clustering(kümeleme) yöntemi için KMeans algoritmasını çektik. 
#Kaggledan aldığım veriseti olan Avm_Musterileri.csv dosyasını programa okuttuk
from sklearn.cluster import KMeans
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from matplotlib import pyplot as plt

df = pd.read_csv("Avm_Musterileri.csv")
df.head()

# Veri setimize bir göz atalım:
plt.scatter(df['Annual Income (k$)'], df['Spending Score (1-100)'])
plt.xlabel('Annual Income (k$)')
plt.ylabel('Spending Score (1-100)')
plt.savefig('1.png', dpi=300)
plt.show()

# Bazı sütun isimleri çok uzun onları kısaltalım:
df.rename(columns = {'Annual Income (k$)':'income'}, inplace = True)
df.rename(columns = {'Spending Score (1-100)':'score'}, inplace = True)

#sklearn yardımıyla normalizasyon yaptım
#MinMaxScaler() fonksiyonunu kullanacağız
scaler = MinMaxScaler()

scaler.fit(df[['income']])
df['income'] = scaler.transform(df[['income']])

scaler.fit(df[['score']])
df['score'] = scaler.transform(df[['score']])
plt.savefig('2normalizsyon.png', dpi=300)
df.head()

#k means clustering algoritmasında optimazsyon için en iyi k değeri belirlenmeli 
#for döngüsü ile en iyi k değerimi belirledim
k_range = range(1,11)

list_dist = []

for k in k_range:
    kmeans_modelim = KMeans(n_clusters=k)
    kmeans_modelim.fit(df[['income','score']])
    list_dist.append(kmeans_modelim.inertia_)
    
    plt.xlabel('K')
plt.ylabel('Distortion değeri (inertia)')
plt.plot(k_range,list_dist)
plt.savefig('3EniyiKdeğeri.png', dpi=500)
plt.show()
# K = 5 için bir K-Means modeli oluşturalım:
kmeans_modelim = KMeans(n_clusters = 5)
y_predicted = kmeans_modelim.fit_predict(df[['income','score']])
plt.savefig('4K-Means Modeli.png', dpi=300)
y_predicted

df['cluster'] = y_predicted
df.head()

#K-Means modelinin bitmiş grafik halini görüntülemek için kümeleri renklerine ayırt ediyorum
df1 = df[df.cluster==0]
df2 = df[df.cluster==1]
df3 = df[df.cluster==2]
df4 = df[df.cluster==3]
df5 = df[df.cluster==4]


plt.xlabel('income')
plt.ylabel('score')
plt.scatter(df1['income'],df1['score'],color='green')
plt.scatter(df2['income'],df2['score'],color='red')
plt.scatter(df3['income'],df3['score'],color='black')
plt.scatter(df4['income'],df4['score'],color='orange')
plt.scatter(df5['income'],df5['score'],color='purple')
# kmeans_modelim.cluster_centers_ numpy 2 boyutlu array olduğu için x ve y sütunlarını kmeans_modelim.cluster_centers_[:,0] 
# ve kmeans_modelim.cluster_centers_[:,1] şeklinde scatter plot için alıyoruz:
plt.scatter(kmeans_modelim.cluster_centers_[:,0], kmeans_modelim.cluster_centers_[:,1], color='blue', marker='X', label='centroid')
plt.legend()
plt.show()

#kırmızı olanlar zengin kesim, siyah olanlar geliri yüksek avm alışverişi az olan
#sarı olanlar geliri az avm alışverişi az , mor olanlar geliri az ama avm alışverişi çok
#yeşil olanlar ise dengeli