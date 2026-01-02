import pandas as pd
import numpy as np
import random 

#Duy
class Data_Loader:
    def __init__(self ,link: str):
        self._df = pd.read_csv(link)

    def add_random_missing_values( self ,missing_rate: float = 0.05, seed: random = 42) -> pd.DataFrame:
        df_missing = self._df.copy()
        df_size = self._df.size
        num_missing = int(df_size * missing_rate)

        if seed:
            random.seed(seed)

        for _ in range(num_missing):
            row_idx = random.randint(0,self._df.shape[0]- 1)
            col_idx = random.randint(0,self._df.shape[1]- 1)

            df_missing.iat[row_idx,col_idx] = np.nan

        return df_missing
    
    def get_missin_data(self ,missing_rate: float = 0.05, seed: random = 42 ) -> pd.DataFrame:
        return self.add_random_missing_values(missing_rate ,seed)
#Hết