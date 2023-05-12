
import time
# import random
import pandas as pd
import numpy as np
import openai
import time

#  openapi

openai.api_key =


df = pd.read_csv('/Users/ruchiraray/Documents/UT CML/Cleaned (without citation).csv')
print(df.shape)
categories=["Social Movements, politics, policy, or Activism", "News", "Misinformation or Disinformation", "Social Stratification or Segregation", "Economic sociology", "Health"]
df=df[80:150]
for i, row in df.iterrows():
  name=row['Title']
  # print(name)
  # quit()
  for category in categories:
    
    query= "Answer in just one word (yes or no). Can the paper \"" +name+ "\" with the abstract \"" + row['Abstract Note']+"\" and the keywords \" "+ row['Keywords']+"\" be tagged by " + category +" category?"
    print("Query: ", query )
    time.sleep(30)
    completion = openai.ChatCompletion.create( model="gpt-3.5-turbo", messages=[{"role": "user", "content": query}])
    reply_content = completion.choices[0].message.content
    print("Reply: ", reply_content )
    if 'No' in reply_content:
      print("no")
      df.at[i,category]=0
      # df.to_csv("/Users/ruchiraray/Documents/UT CML/result4.csv")
      # quit()
    else:
      df.at[i,category]=1
      # df.to_csv("/Users/ruchiraray/Documents/UT CML/result4.csv")
  quit()



# df.to_csv("/Users/ruchiraray/Documents/UT CML/result4.csv")





