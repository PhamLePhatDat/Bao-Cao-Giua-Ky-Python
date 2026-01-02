import data_loader
import clean_data
import exploratory_analysis

def main():
    # 1. Load dữ liệu và tạo missing values
    dl = data_loader.Data_Loader("jobs_in_data.csv")
    df_missing = dl.get_missin_data(missing_rate=0.05)

    # 2. Khám phá dữ liệu trước khi làm sạch
    cd = clean_data.CleanData(df_missing)
    # cd.show_raw_data_info()

    # 3. Làm sạch dữ liệu
    df_clean = cd.get_clear_data()

    print("Dữ liệu sau khi làm sạch (5 dòng đầu tiên):")
    print(df_clean.head(), "\n")

    print("Kiểm tra lại số lượng giá trị bị thiếu sau khi làm sạch:")
    print(df_clean.isna().sum().sum(), "\n")

    ea = exploratory_analysis.ExploratoryAnalysis(df_clean)

    ea.count_unique_values()
    ea.show_value_counts()

    ea.order_company_size()

    ea.plot_job_category_distribution()
    ea.plot_salary_by_experience()
    ea.plot_salary_by_job_and_setting()

    print("Bảng lương trung bình theo ngành nghề:")
    print(ea.mean_salary_by_job())

    ea.job_distribution_by_country("United States")

    print("Bảng mô tả thống kê các biến số:")
    print(ea.describe_numerical(), "\n")   

    print("Thống kê chi tiết cho từng biến số:")
    ea.give_numerical_stats()

    ea.plot_salary_distribution()

    ea.plot_salary_kde()

    ea.plot_salary_kde_by_setting()

    ea.plot_salary_point_by_setting()
    ea.plot_salary_boxplot()

    ea.plot_salary_trend()

    print("=== BOXPLOT LƯƠNG TRƯỚC KHI XỬ LÝ OUTLIER ===")
    ea.plot_salary_boxplot_simple()

    print("=== BOXPLOT SAU KHI LOẠI BỎ OUTLIER (DATAFRAME MỚI) ===")
    ea.plot_salary_boxplot_after_outlier_removal()


if __name__ == "__main__":
    main()
