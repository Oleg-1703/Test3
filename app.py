import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats as stats

# Заголовок приложения
st.title("Анализ больничных дней")

#print('abc)

# Инструкция для загрузки файла
st.write("Загрузите CSV файл с данными:")

# Виджет для загрузки файла
uploaded_file = st.file_uploader("Выберите файл")

if uploaded_file is not None:
    # Чтение файла в DataFrame с нужной кодировкой
    df = pd.read_csv('Статистика.csv', encoding='Windows-1251')
    df['Пол'] = df['Пол'].replace({'М': 1,'Ж': 0})

    # Превью данных
    st.write("Превью загруженных данных:")
    st.write(df.head())

    # 1. Графики по полу

    # Визуализация распределения больничных дней среди мужчин
    male_sick_days = df[df['Пол'] == 1]['Количество больничных дней']
    fig_male, ax_male = plt.subplots()
    sns.histplot(male_sick_days, bins=10, kde=True, ax=ax_male)
    ax_male.set_title('Распределение количества больничных дней среди мужчин')
    ax_male.set_xlabel('Количество больничных дней')
    ax_male.set_ylabel('Частота')
    st.pyplot(fig_male)

    # Визуализация распределения больничных дней среди женщин
    female_sick_days = df[df['Пол'] == 0]['Количество больничных дней']
    fig_female, ax_female = plt.subplots()
    sns.histplot(female_sick_days, bins=10, kde=True, ax=ax_female)
    ax_female.set_title('Распределение количества больничных дней среди женщин')
    ax_female.set_xlabel('Количество больничных дней')
    ax_female.set_ylabel('Частота')
    st.pyplot(fig_female)

    # Boxplot для количества больничных дней по полу
    fig_boxplot_gender, ax_boxplot_gender = plt.subplots()
    sns.boxplot(x='Пол', y='Количество больничных дней', data=df, ax=ax_boxplot_gender)
    ax_boxplot_gender.set_title('Количество больничных дней по полу')
    st.pyplot(fig_boxplot_gender)

    # 2. Проверка гипотез по полу

    alpha = 0.05  # Уровень значимости
    results_gender = stats.ttest_ind(male_sick_days, female_sick_days, alternative="greater")
    mean_male = male_sick_days.mean()
    mean_female = female_sick_days.mean()

    # Вывод результатов гипотезы по полу
    st.write(f"Среднее количество больничных дней у мужчин: {mean_male:.3f}")
    st.write(f"Среднее количество больничных дней у женщин: {mean_female:.3f}")
    st.write(f"p-значение (пол): {results_gender.pvalue:.4f}")
    st.write(f"T-статистика (пол): {results_gender.statistic:.4f}")

    # Интерпретация результатов по полу
    if results_gender.pvalue < alpha:
        st.write("Отклоняем нулевую гипотезу: мужчины пропускают 2 и более дней по болезни чаще, чем женщины.")
    else:
        st.write("Не удалось отклонить нулевую гипотезу: мужчины пропускают 2 и более дней по болезни так же, как женщины.")

    # 3. Графики по возрасту

    # Визуализация распределения больничных дней среди сотрудников старше 35 лет
    old_sick_days = df[df['Возраст'] > 35]['Количество больничных дней']
    young_sick_days = df[df['Возраст'] <= 35]['Количество больничных дней']

    # Распределение для старших
    fig_old, ax_old = plt.subplots()
    sns.histplot(old_sick_days, bins=10, kde=True, ax=ax_old)
    ax_old.set_title('Распределение количества больничных дней среди старших сотрудников')
    ax_old.set_xlabel('Количество больничных дней')
    ax_old.set_ylabel('Частота')
    st.pyplot(fig_old)

    # Распределение для молодых
    fig_young, ax_young = plt.subplots()
    sns.histplot(young_sick_days, bins=10, kde=True, ax=ax_young)
    ax_young.set_title('Распределение количества больничных дней среди молодых сотрудников')
    ax_young.set_xlabel('Количество больничных дней')
    ax_young.set_ylabel('Частота')
    st.pyplot(fig_young)

    # Boxplot для количества больничных дней по возрастным группам
    df['Возраст группа'] = ['Старше 35' if x > 35 else 'Моложе 35' for x in df['Возраст']]
    fig_boxplot_age, ax_boxplot_age = plt.subplots()
    sns.boxplot(x='Возраст группа', y='Количество больничных дней', data=df, ax=ax_boxplot_age)
    ax_boxplot_age.set_title('Количество больничных дней по возрастным группам')
    st.pyplot(fig_boxplot_age)

    # 4. Проверка гипотез по возрасту

    results_age = stats.ttest_ind(old_sick_days, young_sick_days, alternative="greater")
    mean_old = old_sick_days.mean()
    mean_young = young_sick_days.mean()

    # Вывод результатов гипотезы по возрасту
    st.write(f"Среднее количество больничных дней у старших сотрудников: {mean_old:.3f}")
    st.write(f"Среднее количество больничных дней у молодых сотрудников: {mean_young:.3f}")
    st.write(f"p-значение (возраст): {results_age.pvalue:.4f}")
    st.write(f"T-статистика (возраст): {results_age.statistic:.4f}")

    # Интерпретация результатов по возрасту
    if results_age.pvalue < alpha:
        st.write("Отклоняем нулевую гипотезу: сотрудники старше 35 лет пропускают 2 и более дней по болезни чаще, чем молодые.")
    else:
        st.write("Не удалось отклонить нулевую гипотезу: сотрудники старше 35 лет пропускают 2 и более дней по болезни так же, как молодые.")
