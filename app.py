import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.algorithms import brute_force_solve, greedy_solve, hill_climbing_solve, Item, Mule
from src.instance_generator import generate_instance, generate_case1, generate_case2, generate_case3, generate_case4, generate_case5, generate_case6, generate_case7, generate_case8, generate_case9, generate_case10, generate_case11, generate_case12

st.set_page_config(page_title="Discrete Transport Optimization", layout="wide")

st.title("Discrete Transport Optimization")
st.markdown("""
This application visualizes algorithms for the **Discrete Transport Problem**.
The goal is to distribute items among mules to **minimize the difference in total value** between the most and least loaded mules, 
while respecting weight capacities.
""")

# Sidebar for configuration
st.sidebar.header("Instance Configuration")

instance_type = st.sidebar.radio("Instance Type", ["Random", "Predefined Cases"])

if instance_type == "Random":
    num_items = st.sidebar.slider("Number of Items (N)", 2, 100, 10)
    num_mules = st.sidebar.slider("Number of Mules (M)", 2, 10, 3)

    st.sidebar.subheader("Item Parameters")
    min_w, max_w = st.sidebar.slider("Weight Range", 1, 50, (1, 10))
    min_v, max_v = st.sidebar.slider("Value Range", 1, 100, (10, 50))

    st.sidebar.subheader("Mule Parameters")
    cap_mode = st.sidebar.radio("Capacity Mode", ["Fixed", "Random Range", "Manual"])

    fixed_cap = None
    mule_cap_range = None
    custom_caps = None

    if cap_mode == "Fixed":
        fixed_cap = st.sidebar.number_input("Fixed Capacity", min_value=10, value=50)
    elif cap_mode == "Random Range":
        mule_cap_range = st.sidebar.slider("Capacity Range", 10, 200, (40, 60))
    elif cap_mode == "Manual":
        custom_caps = []
        st.sidebar.write("Set capacity for each mule:")
        for i in range(num_mules):
            cap = st.sidebar.number_input(f"Mule {i} Capacity", min_value=10, value=50, key=f"mule_cap_{i}")
            custom_caps.append(cap)

    if st.sidebar.button("Generate New Instance"):
        items, mules = generate_instance(
            num_items, num_mules,
            (min_w, max_w), (min_v, max_v),
            fixed_capacity=fixed_cap,
            mule_capacity_range=mule_cap_range,
            custom_capacities=custom_caps
        )
        st.session_state['items'] = items
        st.session_state['mules'] = mules
        st.session_state['results'] = {}

elif instance_type == "Predefined Cases":
    case_options = [f"Case {i}" for i in range(1, 13)]
    selected_case = st.sidebar.selectbox("Select Case", case_options)

    if selected_case == "Case 12":
        cases = generate_case12()
        subcase_options = [c[0] for c in cases]
        selected_subcase = st.sidebar.selectbox("Select Subcase", subcase_options)
        if st.sidebar.button("Load Case"):
            idx = subcase_options.index(selected_subcase)
            items, mules = cases[idx][1], cases[idx][2]
            st.session_state['items'] = items
            st.session_state['mules'] = mules
            st.session_state['results'] = {}
    else:
        if st.sidebar.button("Load Case"):
            case_num = int(selected_case.split()[1])
            func_name = f"generate_case{case_num}"
            items, mules = globals()[func_name]()
            st.session_state['items'] = items
            st.session_state['mules'] = mules
            st.session_state['results'] = {}


# Check if instance exists
if 'items' not in st.session_state:
    st.info("Please generate an instance from the sidebar.")
else:
    items = st.session_state['items']
    mules_config = st.session_state['mules']

    # Display Instance Data
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Items")
        items_df = pd.DataFrame([vars(i) for i in items])
        st.dataframe(items_df, height=200)
    
    with col2:
        st.subheader("Mules")
        mules_df = pd.DataFrame([{'id': m.id, 'capacity': m.capacity} for m in mules_config])
        st.dataframe(mules_df, height=200)

    st.divider()
    
    # Algorithm Selection and Execution
    st.header("Run Algorithms")
    
    alg_col1, alg_col2, alg_col3 = st.columns(3)
    
    with alg_col1:
        if st.button("Run Greedy Heuristic"):
            mules_res, diff, time_taken = greedy_solve(items, mules_config)
            st.session_state['results']['Greedy'] = (mules_res, diff, time_taken)
            
    with alg_col2:
        if st.button("Run Hill Climbing"):
            mules_res, diff, time_taken = hill_climbing_solve(items, mules_config)
            st.session_state['results']['Hill Climbing'] = (mules_res, diff, time_taken)
            
    with alg_col3:
        if len(items) <= 12:
            if st.button("Run Brute Force (Optimal)"):
                with st.spinner("Calculating optimal solution..."):
                    mules_res, diff, time_taken = brute_force_solve(items, mules_config)
                    st.session_state['results']['Brute Force'] = (mules_res, diff, time_taken)
        else:
            st.button("Brute Force Disabled (N > 12)", disabled=True)

    # Display Results
    if st.session_state['results']:
        st.subheader("Results Comparison")
        
        res_data = []
        for alg_name, (res, diff, time_taken) in st.session_state['results'].items():
            status = "Success" if res else "Failed"
            res_data.append({
                "Algorithm": alg_name,
                "Difference (Risk)": diff if res else "N/A",
                "Time (s)": f"{time_taken:.6f}",
                "Status": status
            })
        
        st.table(pd.DataFrame(res_data))
        
        # Visualization of Assignments
        st.subheader("Assignment Visualization")
        selected_alg = st.selectbox("Select Algorithm to Visualize", list(st.session_state['results'].keys()))
        
        res_mules, diff, _ = st.session_state['results'][selected_alg]
        
        if res_mules:
            # Prepare data for plotting
            plot_data = []
            for m in res_mules:
                for item in m.items:
                    plot_data.append({
                        "Mule ID": f"Mule {m.id}",
                        "Item Value": item.value,
                        "Item Weight": item.weight,
                        "Item ID": f"Item {item.id}"
                    })
            
            if plot_data:
                df_plot = pd.DataFrame(plot_data)
                
                # Stacked Bar Chart for Value Distribution
                fig, ax = plt.subplots(figsize=(10, 6))
                
                # We want to show the total value per mule, broken down by item
                # A simple bar chart of total values is good
                mule_values = [m.current_value for m in res_mules]
                mule_ids = [f"Mule {m.id}" for m in res_mules]
                
                sns.barplot(x=mule_ids, y=mule_values, ax=ax, palette="viridis")
                ax.set_title(f"Total Value per Mule (Diff: {diff})")
                ax.set_ylabel("Total Value")
                
                # Add value labels on top
                for i, v in enumerate(mule_values):
                    ax.text(i, v + 1, str(v), ha='center')
                
                st.pyplot(fig)
                
                # Detailed Item Breakdown
                st.write("### Detailed Assignment")
                cols = st.columns(len(res_mules))
                for idx, mule in enumerate(res_mules):
                    with cols[idx]:
                        st.markdown(f"**Mule {mule.id}**")
                        st.markdown(f"Total Value: {mule.current_value}")
                        st.markdown(f"Total Weight: {mule.current_weight}/{mule.capacity}")
                        st.markdown("Items:")
                        for item in mule.items:
                            st.text(f"- ID:{item.id} (V:{item.value}, W:{item.weight})")
            else:
                st.warning("No items assigned.")
        else:
            st.error("Algorithm failed to find a valid assignment.")
