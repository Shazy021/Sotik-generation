from pyspark.sql import DataFrame
from pyspark.sql import functions as f
import matplotlib.pyplot as plt
import seaborn as sns
import io
import os
from PIL import Image
import folium
from folium.plugins import MarkerCluster


class ReportGenerator:
    def __init__(self, df_ord: DataFrame, df_prod: DataFrame, df_buy: DataFrame):
        self.df_prod = df_prod.withColumnRenamed("id", "prod_id")
        self.df_buy = df_buy

        self.data = df_ord.withColumn("item_id", f.explode(df_ord["item_ids"])).drop('item_ids')
        self.data = self.data.join(self.df_prod, self.data['item_id'] == self.df_prod['prod_id'], "left").drop(
            'prod_id')

    def count_models_boxplot(self, df: DataFrame, target_date: str, filename: str) -> None:
        models_top = df.groupby('item_id').count() \
            .join(self.df_prod, df.item_id == self.df_prod.prod_id, "left") \
            .drop('prod_id').orderBy('count', ascending=False) \
            .select('item_id', 'count').toPandas()
        mean_value = models_top['count'].mean()

        plt.figure(figsize=(7, 7))
        ax = sns.boxplot(models_top['count'], showmeans=True)
        ax = sns.stripplot(models_top['count'], color='orange', jitter=0.3, size=2.5)
        ax.legend([ax.lines[-2]], [f'Mean count: {mean_value:.2f}'])
        plt.xlabel('')
        plt.ylabel('count')
        plt.title(f'Разброс кол-ва проданных моделей {target_date}', fontsize=15)
        plt.savefig(f'./data/charts/{filename}.png')

    def buyers_revenue_boxplot(self, df: DataFrame, target_date: str, filename: str) -> None:
        buyers_top = df.groupby('buyers_id').agg(f.sum('price').alias('revenue')).toPandas()
        mean_value = buyers_top['revenue'].mean()

        plt.figure(figsize=(7, 7))
        ax = sns.boxplot(buyers_top['revenue'], showmeans=True)
        ax.legend([ax.lines[-2]], [f'Mean revenue: {mean_value:.2f}'])
        plt.xlabel('')
        plt.ylabel('revenue')
        plt.title(f'Разброс выручки с каждого пользователя {target_date}', fontsize=15)
        plt.savefig(f'./data/charts/{filename}.png')

    def get_map_top_buyers(self, df: DataFrame, file_name: str) -> None:
        df = df.groupby('buyers_id').agg(f.sum('price').alias('revenue')) \
            .orderBy('revenue', ascending=False) \
            .select('buyers_id', f.format_number('revenue', 2).alias('revenue')) \
            .join(self.df_buy, df.buyers_id == self.df_buy.id, 'left') \
            .select('buyers_id', 'geo_lat', 'geo_lon', 'revenue', 'place', 'region').toPandas()

        if len(df) > 20_000:
            df = df[:20_000]

        map_osm = folium.Map()
        marker_cluster = MarkerCluster().add_to(map_osm)

        for _, row in df.iterrows():
            folium.Marker(
                location=[row["geo_lat"], row["geo_lon"]],
                popup=f"<strong>{row['place']} {row['region']} Revenue:{row['revenue']}</strong>",
            ).add_to(marker_cluster)
        map_osm.save("./data/charts/map1.html")

        img_data = map_osm._to_png(5)
        img = Image.open(io.BytesIO(img_data))
        img.save(f'./data/charts/{file_name}.png')

    def create_last_day_report(self) -> list[str, str, str]:
        last_date = self.data.select(f.max("time")).first()[0].date()
        target_date = last_date.strftime("%Y-%m-%d")
        tar_data = self.data.filter(f.col("time").cast("date") == target_date)

        if f'{target_date}-bmap.png' in os.listdir('./data/charts'):
            pass
        else:
            self.count_models_boxplot(tar_data, target_date, f'{target_date}-countbp')
            self.buyers_revenue_boxplot(tar_data, target_date, f'{target_date}-revenuebp')
            self.get_map_top_buyers(tar_data, f'{target_date}-bmap')

        return [f'{target_date}-countbp.png', f'{target_date}-revenuebp.png', f'{target_date}-bmap.png']
