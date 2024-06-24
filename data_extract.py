from modules.scrapper import *
import pandas as pd

def main():

    df = pd.DataFrame()
    data = get_data_from_instagram()

    for dfCandidate in data:
        df_temp = pd.DataFrame(dfCandidate)
        df = pd.concat([df, df_temp])
    
    df.to_excel('data.xlsx', index=False)

if __name__ == '__main__':
    main()
    