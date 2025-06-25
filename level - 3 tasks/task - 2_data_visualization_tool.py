import pandas as pd

def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        print("\n✅ Dataset loaded successfully!")
        print("📌 Columns:", df.columns.tolist())
        return df
    except Exception as e:
        print(f"❌ Error: {e}")
        return None
import matplotlib.pyplot as plt

def matplotlib_plot(df, x, y):
    plt.plot(df[x], df[y], marker='o')
    plt.title("Matplotlib Line Plot")
    plt.xlabel(x)
    plt.ylabel(y)
    plt.grid(True)
    plt.tight_layout()
    plt.show()
import seaborn as sns

def seaborn_plot(df, x, y):
    sns.set(style='whitegrid')
    sns.scatterplot(data=df, x=x, y=y)
    plt.title("Seaborn Scatter Plot")
    plt.tight_layout()
    plt.show()
import plotly.express as px

def plotly_plot(df, x, y):
    fig = px.scatter(df, x=x, y=y, title="Plotly Interactive Plot")
    fig.show()
    fig.write_html("interactive_plot.html")
    print("✅ Plot saved as interactive_plot.html")
def main():
    print("📊 Welcome to the Data Visualization Tool")

    file_path = "data.csv"
    df = load_data(file_path)
    if df is None:
        return

    x_col = input("Enter column for X-axis: ").strip()
    y_col = input("Enter column for Y-axis: ").strip()

    print("\nChoose Library:")
    print("1. Matplotlib")
    print("2. Seaborn")
    print("3. Plotly (Interactive)")

    choice = input("Enter choice (1/2/3): ").strip()

    if choice == '1':
        matplotlib_plot(df, x_col, y_col)
    elif choice == '2':
        seaborn_plot(df, x_col, y_col)
    elif choice == '3':
        plotly_plot(df, x_col, y_col)
    else:
        print("❌ Invalid choice")
if __name__ == "__main__":
    main()
