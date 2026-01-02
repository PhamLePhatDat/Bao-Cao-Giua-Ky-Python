import pandas as pd
from pandas.api.types import CategoricalDtype
import matplotlib.pyplot as plt
import seaborn as sns

class ExploratoryAnalysis:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def get_categorical_columns(self):
        return self.df.select_dtypes(include=["object", "category"])

    def get_numerical_columns(self):
        return self.df.select_dtypes(include=["float", "int"])

    def show_head(self, n=5):
        df_categorical = self.get_categorical_columns()
        return df_categorical.head(n)

    def show_unique_values(self, column):
        return self.df[column].unique()
    

    def count_unique_values(self):
        df_categorical = self.get_categorical_columns()

        for col in df_categorical.columns:
            print(
                f'Trong biến phân loại "{col}" có '
                f'{df_categorical[col].nunique()} giá trị khác nhau.\n'
            )

    def show_value_counts(self):
        df_categorical = self.get_categorical_columns()

        for col in df_categorical.columns:
            print(f"Tần suất các giá trị trong cột '{col}':")
            print(df_categorical[col].value_counts())
            print(5 * "*********")

    def order_company_size(self, column="company_size"):
        comp_categories = self.df[column].unique().tolist()[::-1]

        cat_type = CategoricalDtype(categories=comp_categories, ordered=True)
        self.df[column] = self.df[column].astype(cat_type)

        print("5 giá trị đầu tiên của biến company_size sau khi sắp xếp thứ tự:")
        return self.df[column].head()
    
    def plot_job_category_distribution(self):
        plt.figure(figsize=(10,6))
        sns.countplot(
            data=self.df,
            y="job_category",
            order=self.df["job_category"].value_counts().index ,palette = "Set1")
        plt.title("Phân bố số lượng theo ngành nghề")
        plt.xlabel("Số lượng")
        plt.ylabel("Ngành nghề")
        plt.show()
    
    def plot_salary_by_experience(self):
        plt.figure(figsize=(10,6))
        sns.barplot(
            data=self.df,
            x="experience_level",
            y="salary_in_usd",
            hue = "job_category"
        )
        plt.title("Mức lương trung bình theo cấp độ kinh nghiệm")
        plt.xlabel("Cấp độ kinh nghiệm")
        plt.ylabel("Lương (USD)")
        plt.show()

    def mean_salary_by_job(self):
        return (
            self.df
            .groupby("job_category")["salary_in_usd"]
            .mean()
            .to_frame(name="Lương trung bình (USD)")
            .reset_index()
            .sort_values(by="Lương trung bình (USD)", ascending=False)
        )

    def job_distribution_by_country(self, country = "United States"):
        print(self.df.groupby(by = "company_location")["job_category"].value_counts())
        df_location = self.df.groupby(by = "company_location")["job_category"].value_counts().to_frame().reset_index().sort_values(by ="count" , ascending=False)
        df_location_usa= df_location[df_location["company_location"] == country]
        df_location_usa    

        plt.figure(figsize=(12,8))
        plt.xticks(rotation=90, ha="right", fontsize=10)
        sns.barplot(data = df_location_usa, x = "job_category", y= "count" , hue = "job_category", order=df_location_usa["job_category"])
        plt.title(f"Phân bố ngành nghề tại {country}")
        plt.xlabel("Quốc gia")
        plt.ylabel("Số lượng")
        plt.show()

    def describe_numerical(self):
        return self.get_numerical_columns().describe().T
    
    def give_numerical_stats(self):
        num_df = self.get_numerical_columns()

        for col in num_df.columns:
            print(f"*********** {col} **********")
            print(f"Mean value of {col} is {num_df[col].mean():.2f}")
            print(f"Std value of {col} is {num_df[col].std():.2f}")
            print(f"Max value of {col} is {num_df[col].max()}")
            print(f"Min value of {col} is {num_df[col].min()}")
            print(f"Count value of {col} is {num_df[col].count()}")
            print(f"Median value of {col} is {num_df[col].median()}")

    def plot_salary_distribution(self):
        sns.histplot(
            data=self.df,
            x="salary_in_usd",
            kde=True,
            hue="work_setting"
        )
        plt.title("Phân phối lương theo hình thức làm việc")
        plt.show()

    def plot_salary_kde(self):
        sns.kdeplot(self.df["salary_in_usd"], fill=True)
        plt.title("Phân phối KDE của lương")
        plt.show()

    def plot_salary_kde_by_setting(self):
        sns.FacetGrid(
            data=self.df,
            hue="work_setting",
            height=7,
            xlim=(0, 400000)
        ).map(sns.kdeplot, "salary_in_usd", fill=True).add_legend()
        plt.show()


    def plot_salary_point_by_setting(self):
        sns.catplot(
            data=self.df,
            x="work_setting",
            y="salary_in_usd",
            hue="company_size",
            kind="point"
        )
        plt.show()

    def plot_salary_boxplot(self):
        sns.boxplot(
            data=self.df,
            x="work_setting",
            y="salary_in_usd",
            hue="company_size"
        )
        plt.show()

    def plot_salary_trend(self):
        sns.lineplot(
            data=self.df,
            x="work_year",
            y="salary_in_usd",
            hue="work_setting"
        )
        plt.show()

    def detect_salary_outliers_iqr(self):
        salary = self.df["salary_in_usd"]

        Q1 = salary.quantile(0.25)
        Q3 = salary.quantile(0.75)
        IQR = Q3 - Q1

        lower_fence = Q1 - 1.5 * IQR
        upper_fence = Q3 + 1.5 * IQR

        outliers = self.df[
            (salary < lower_fence) | (salary > upper_fence)
        ]

        print(f"Số lượng outlier: {outliers.shape[0]}")
        return outliers, lower_fence, upper_fence
    
    def remove_salary_outliers(self):
        outliers, lower_fence, upper_fence = self.detect_salary_outliers_iqr()

        df_clean = self.df[
            (self.df["salary_in_usd"] >= lower_fence) &
            (self.df["salary_in_usd"] <= upper_fence)
        ]

        return df_clean

    def plot_salary_boxplot_simple(self):
        plt.figure(figsize=(8,6))
        sns.boxplot(
            y=self.df["salary_in_usd"],
            orient="v"
        )
        plt.title("Boxplot Salary (Original)")
        plt.show()

    def plot_salary_boxplot_after_outlier_removal(self):
        df_no_outlier = self.remove_salary_outliers()

        plt.figure(figsize=(8,6))
        sns.boxplot(
            y=df_no_outlier["salary_in_usd"],
            orient="v"
        )
        plt.title("Boxplot Salary (After Outlier Removal)")
        plt.show()
