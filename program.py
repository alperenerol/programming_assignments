import pandas as pd
import logging


logger = logging.getLogger('tiqets')
                           
df_orders = pd.read_csv ("data/orders.csv")
df_barcodes = pd.read_csv ("data/barcodes.csv")

# Input data validation
try:
    assert df_barcodes['barcode'].unique().shape[0] == df_barcodes['barcode'].count()      
except AssertionError:     
    logger.info(df_barcodes[df_barcodes.duplicated(subset=['barcode'], keep='first')]
                .to_string(header=False))           
    df_barcodes = df_barcodes.sort_values(by=['order_id'],
                    ascending=True).reset_index(drop=True).drop_duplicates(
                        subset='barcode', keep='first', ignore_index=True)      
try:
    assert df_barcodes[(df_barcodes['order_id'].notna()) & (df_barcodes['barcode'].isna())].count()[0] == 0
except AssertionError:
    logger.info(df_barcodes[(df_barcodes['order_id'].notna()) 
                            & (df_barcodes['barcode'].isna())].to_string(header=False))
    df_barcodes = df_barcodes[(df_barcodes['order_id'].notna()) 
                              & (df_barcodes['barcode'].notna())]
# Print the amount of unused barcodes (barcodes left)
print(df_barcodes[(df_barcodes['order_id'].isna())].shape[0])

df_output = pd.merge(df_orders, df_barcodes, on="order_id").sort_values(
    ["customer_id", "order_id"], ascending = (True, True)).reset_index(drop=True)
top_customers_amounts = df_output['customer_id'].value_counts()[:5]
for item in zip(top_customers_amounts.index, top_customers_amounts):
    print(str(item)[1:-1].replace(" ", ""))

df_output.groupby(['customer_id','order_id'])['barcode'].apply(list).reset_index().to_csv('output.csv', index=False)
