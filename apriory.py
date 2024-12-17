import streamlit as st
import pandas as pd
from apyori import apriori

# Load dataset
st.title("Multazam Mart Analysis")
st.write("This application allows you to explore transaction data and perform association rule analysis using the Apriori algorithm.")

uploaded_file = st.file_uploader("Choose a file", type="xlsx")

if uploaded_file:
    data = pd.read_excel(uploaded_file)
    st.write("## Data Preview")
    st.dataframe(data.head())

    # Prepare data for Apriori
    items_data = data['Items'].dropna()
    records = [str(item).split(', ') for item in items_data]
    
    st.write("## Apriori Analysis Settings")
    min_support = st.slider("Minimum Support", min_value=0.01, max_value=1.0, value=0.05)
    min_confidence = st.slider("Minimum Confidence", min_value=0.01, max_value=1.0, value=0.5)
    min_lift = st.slider("Minimum Lift", min_value=1.0, max_value=10.0, value=1.5)

    if st.button("Run Apriori"):
        st.write("## Results")
        association_rules = apriori(records, min_support=min_support, min_confidence=min_confidence, min_lift=min_lift)
        association_results = list(association_rules)
        
        if not association_results:
            st.write("No association rules found. Try lowering the thresholds.")
        else:
            # Process and display results in a structured format
            results = []
            for result in association_results:
                for ordered_stat in result.ordered_statistics:
                    results.append({
                        "Rule": f"{list(ordered_stat.items_base)} -> {list(ordered_stat.items_add)}",
                        "Support": f"{result.support:.2%}",  # Format as percentage
                        "Confidence": f"{ordered_stat.confidence:.2%}",  # Format as percentage
                        "Lift": f"{ordered_stat.lift:.2f}"
                    })

            results_df = pd.DataFrame(results)

            # Display results as formatted strings
            st.write("### Generated Rules:")
            st.table(results_df)

            # For visualizations, we still need numeric values
            results_df["Support_num"] = results_df["Support"].str.rstrip('%').astype(float) / 100
            results_df["Confidence_num"] = results_df["Confidence"].str.rstrip('%').astype(float) / 100

            # Visualizations
            st.write("### Support Visualization:")
            st.bar_chart(results_df.set_index('Rule')['Support_num'])
            st.write("### Confidence Visualization:")
            st.bar_chart(results_df.set_index('Rule')['Confidence_num'])

    # Export results
    if 'results_df' in locals() and not results_df.empty:
        st.write("## Export Results")
        st.download_button(label="Download CSV", data=results_df.to_csv(), file_name="apriori_results.csv", mime='text/csv')
