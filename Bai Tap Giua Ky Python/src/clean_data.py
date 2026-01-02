import pandas as pd
#Bảo
class CleanData:
    def __init__(self ,df :pd.DataFrame):
        self.df = df

    def show_raw_data_info(self):
        df_raw = self.df.copy()
        print("Thông tin của dữ liệu góc trước khi làm sạch:")

        print("5 dòng đầu tiên của dữ liệu:")
        print(df_raw.head(), "\n")

        print("5 dòng cuối cùng của dữ liệu:")
        print(df_raw.tail(), "\n")

        print(f"Kích thước tập dữ liệu (số dòng, số cột): {df_raw.shape}\n")

        print("Danh sách các cột:")
        print(df_raw.columns, "\n")

        print(f"Trong tập dữ liệu có tổng cộng {len(df_raw.columns)} cột.")
        print(f"Kiểu dữ liệu mà df_raw.columns trả về là: {type(df_raw.columns)}\n")

        print("Thông tin tổng quát của DataFrame:")
        df_raw.info()
        print("\n")

        print("Kiểu dữ liệu của từng cột:")
        print(df_raw.dtypes, "\n")

        categorical_features = []
        numerical_features = []

        for col in df_raw.columns:
            if df_raw[col].dtype == "object" or str(df_raw[col].dtype) == "category":
                categorical_features.append(col)
            else:
                numerical_features.append(col)

        print("Các thuộc tính phân loại (Categorical Features):")
        print(categorical_features, "\n")

        print("Các thuộc tính số (Numerical Features):")
        print(numerical_features, "\n")

        for col in categorical_features:
            df_raw[col] = pd.Categorical(df_raw[col])

        print("Thông tin dữ liệu sau khi ép kiểu categorical:")
        df_raw.info()
        print("\n")

        print("Thông tin về quy mô công ty:")
        print(df_raw['company_size'][:3])
        print("\n")

        print("Mô tả thống kê các thuộc tính số:")
        print(df_raw.describe().T)

        print("Số lượng giá trị bị thiếu trên mỗi cột:")
        print(df_raw.isna().sum())

        print(f"Tổng số giá trị bị thiếu trong toàn bộ tập dữ liệu: {df_raw.isna().sum().sum()} \n")

        print("Số lượng giá trị không bị thiếu trên mỗi cột:")
        print(df_raw.notnull().sum())
        print(f"Tổng số giá trị không bị thiếu trong toàn bộ tập dữ liệu: {df_raw.notna().sum().sum()} \n")

    def get_clear_data(self) -> pd.DataFrame:
        clear_data = self.df.copy()

        clear_data.drop_duplicates(inplace=True)

        categorical_cols = clear_data.select_dtypes(include=["object", "category"]).columns
        for col in categorical_cols:
            if clear_data[col].isna().sum() > 0:
                clear_data[col].fillna(clear_data[col].mode()[0], inplace=True)

        numerical_cols = clear_data.select_dtypes(include=["int64", "float64"]).columns
        for col in numerical_cols:
            if clear_data[col].isna().sum() > 0:
                clear_data[col].fillna(clear_data[col].median(), inplace=True)

        for col in categorical_cols:
            clear_data[col] = clear_data[col].astype("category")

        return clear_data
#Hết