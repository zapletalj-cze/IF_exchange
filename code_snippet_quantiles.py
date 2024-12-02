class_1 = gdf[gdf['variable_1'].between(0, 5)]
remaining_data = gdf[~gdf['variable_1'].between(0, 5)]
quantiles = pd.qcut(remaining_data['variable_1'], q=4, labels=['class_2', 'class_3', 'class_4', 'class_5'])
remaining_data['class'] = quantiles
class_1['class'] = 'class_1'
result = pd.concat([class_1, remaining_data])
result.head()
