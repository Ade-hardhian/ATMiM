import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt

tab1, tab2, tab3 = st.tabs(["Replenishment Time Adjustment", "Terminal Analysis", "Cassette Capacity Analysis"])
# Tab 1 - Replenishment Time Adjustment
with tab1:
    st.text("Welcome to the Replenishment Time Adjustment Tool. Please upload the file you would like to adjust the replenishment time for.")

    def analysis_DSA(uploaded_files):
        output = []

        for uploaded_file in uploaded_files:
            # Read the file content as string
            file_content = uploaded_file.getvalue().decode("utf-8")

            # Split content into lines
            all_lines = file_content.splitlines()
            
            # Search for the specific keyword in the lines
            for i, line in enumerate(all_lines):
                if "---Replenishment -----------------------------" in line:
                    # Extract relevant lines based on your logic
                    line_a = all_lines[i + 1]  # Next line after the found line
                    line_b = all_lines[i + 2]  # Two lines after the found line
                    
                    # Split the lines to extract specific data
                    id_polos = line_a.split(" ")
                    id = id_polos[4] if len(id_polos) > 4 else None  # Ensure the index exists
                    
                    tanggal_polos = line_b.split(" ")
                    ej_tanggal = tanggal_polos[12] if len(tanggal_polos) > 12 else None
                    time = tanggal_polos[13] if len(tanggal_polos) > 13 else None
                    
                    # Append extracted data to the output list, but only once per occurrence
                    output.append([id, ej_tanggal, time])

        return output

    # File uploader to upload multiple files
    uploaded_files = st.file_uploader("Choose a file", accept_multiple_files=True, key="file_uploader_1")

    st.header("Replenishment Time Adjustment")
    
    # Start button to trigger the analysis
    if st.button("START", key="start_button_1"):
        if uploaded_files:
            # Call the analysis function and display results
            df3 = analysis_DSA(uploaded_files)
            df_final = pd.DataFrame(df3)
            df_final.rename(columns={0:'ID', 1:'Date', 2:'Adjustment time RPL'}, inplace=True)
            st.write(df_final)
        else:
            st.error("Please upload files to process.")

# Tab 2 - Terminal Analysis
with tab2:
    st.text("Welcome to the terminal analysis Tool. Please upload the file you would like to analyze a terminal.")
    
    def analysis_terminal(uploaded_ejs):
        output = []
        
        for uploaded_ej in uploaded_ejs:
            # Read the file content as string
            file_content = uploaded_ej.getvalue().decode("utf-8")

            # Split content into lines
            all_lines = file_content.splitlines()
            
            # Initialize variables to store results for each entry
            trx, ej_waktu, rm10, rm20, rm50, rm100 = 'N/A', 'N/A', '0', '0', '0', '0'
            kata = "in cassette : Succeeded"
            kata2 = "Stored banknote :"
            kata3 = "==>"
            
            # Search for the specific keywords and extract data
            for i, line in enumerate(all_lines):
                if kata in line:
                    line_a = i
                    line_b = i - 1  # Previous line
                    line_c = i + 1  # Next line
                    
                    # Extract transaction information from the relevant lines
                    id_polos = all_lines[line_a].split(" ")
                    trx = id_polos[0]
                    trx = trx.replace("in cassette : Succeeded", "Dispense")  # Replace text as needed
                    
                    jam = all_lines[line_b].split(" ")
                    ej_waktu = jam[4] if len(jam) > 4 else 'N/A'  # Ensure there is enough data
                    
                    denom = all_lines[line_c].split(":")
                    rm10 = "-" + denom[1][:2] if len(denom) > 1 else '0'
                    rm20 = "0"
                    rm50 = "-" + denom[2][:2] if len(denom) > 2 else '0'
                    rm100 = "0"

                    # Extract the date from the file name
                    df2 = uploaded_ej.name
                    wsid = df2.split('-')
                    tanggal = wsid[1]
                    
                    # Append extracted data to the output list
                    output.append([id, trx, tanggal, ej_waktu, rm10, rm20, rm50, rm100])

                elif kata2 in line:  # If another keyword is found, handle similarly
                    line_a_s = i
                    line_b_s = i + 1
                    line_c_s = i + 2
                    
                    id_polos_s = all_lines[line_a_s].split(" ")
                    trx = id_polos_s[5] if len(id_polos_s) > 5 else 'N/A'
                    ej_waktu = id_polos_s[4] if len(id_polos_s) > 4 else 'N/A'
                    
                    denom_s = all_lines[line_b_s].split(":")
                    denom_s_100 = all_lines[line_c_s].split(":")
                    rm10 = denom_s[1][:2] if len(denom_s) > 1 else '0'
                    rm20 = denom_s[2][:2] if len(denom_s) > 2 else '0'
                    rm50 = denom_s[3][:2] if len(denom_s) > 3 else '0'
                    rm100 = denom_s_100[1][:2] if len(denom_s_100) > 1 else '0'
                    
                    # Extract the date from the file name
                    df2 = uploaded_ej.name
                    wsid = df2.split('-')
                    tanggal = wsid[1]
                    
                    # Append extracted data to the output list
                    output.append([id, trx, tanggal, ej_waktu, rm10, rm20, rm50, rm100])
                
                elif kata3 in line:
                    line_id = i
                    id_ter = all_lines[line_id].split(" ")
                    id = id_ter[6] if len(id_ter) > 6 else 'N/A'
                    output.append([id])


        return output
    

    uploaded_fil = st.file_uploader("Choose a file", accept_multiple_files=True, key="file_uploader_2")

    st.header("Terminal Analysis")
    
    # Start button to trigger the analysis
    if st.button("START", key="start_button_2"):
        if uploaded_fil:
            # Call the analysis function and display results
            df4 = analysis_terminal(uploaded_fil)
            df_final1 = pd.DataFrame(df4)
            df_final1 = df_final1.drop_duplicates()  # Ensure no duplicates in the result
            df_final2 = df_final1.rename(columns={0: 'ID', 1: 'Trx',2: 'Date', 3: 'Time', 4: 'RM10', 5: 'RM20', 6: 'RM50', 7: 'RM100'})
            #merge date and time
            df_final2['Date'] = df_final2['Date'].str.replace('.txt', '', regex=False)
            df_final2.insert(1, "Timestamp", df_final2["Date"] + " " + df_final2["Time"])
            df_final2.drop(columns=["Date", "Time"], inplace=True)
            df_final = df_final2.sort_values(by="Timestamp")
            df_final["Timestamp"] = pd.to_datetime(df_final["Timestamp"])
            df_final = df_final.reset_index(drop=True)
            df_final_true = df_final.dropna()
            #show period and terminal id
            first_time = df_final_true["Timestamp"].iloc[0] 
            last_time = df_final_true["Timestamp"].iloc[-1]
            first_id = df_final_true["ID"].iloc[0]
            combined_text = f"Period: {first_time} - {last_time} | Terminal ID: {first_id}"

            #graph denom flow
            
            # Menghitung Running Total untuk RM50
            numeric_cols = ["RM10", "RM20", "RM50", "RM100"]
            df_final_true[numeric_cols] = df_final_true[numeric_cols].apply(pd.to_numeric, errors="coerce")
            df_final_true["Cumulative_RM10"] = df_final_true["RM10"].cumsum()
            df_final_true["Cumulative_RM20"] = df_final_true["RM20"].cumsum()
            df_final_true["Cumulative_RM50"] = df_final_true["RM50"].cumsum()
            df_final_true["Cumulative_RM100"] = df_final_true["RM100"].cumsum()

            df_form = df_final_true[["ID", "Timestamp", "Trx", "RM10", "RM20", "RM50", "RM100"]]

            # Menentukan Warna Berdasarkan Kenaikan/Penurunan
            colors = ["blue" if x > 0 else "orange" for x in df_final_true["RM10"]]
            colors20 = ["blue" if x > 0 else "orange" for x in df_final_true["RM20"]]
            colors50 = ["blue" if x > 0 else "orange" for x in df_final_true["RM50"]]
            colors100 = ["blue" if x > 0 else "orange" for x in df_final_true["RM100"]]

            # Membuat Grafik Waterfall Kumulatif
            fig = go.Figure()
            fig20 = go.Figure()
            fig50 = go.Figure()
            fig100 = go.Figure()

            fig.add_trace(go.Scatter(
                x=df_final_true["Timestamp"], 
                y=df_final_true["Cumulative_RM10"], 
                mode="lines+markers", 
                marker=dict(color=colors),
                line=dict(color="white", width=2),
                name="Total",
            ))

            fig.add_hline(y=0, line=dict(color="red", width=2, dash="dash"))
            # Layout Styling
            fig.update_layout(
                title="Denom RM10 Trend",
                title_x=0.5,
                xaxis=dict(title="Time", tickangle=-45, showgrid=False),
                yaxis=dict(title="Cumulative RM10"),
                plot_bgcolor="black",
                paper_bgcolor="white",
                font=dict(color="black"),
                legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
            )

            fig20.add_trace(go.Scatter(
                x=df_final_true["Timestamp"], 
                y=df_final_true["Cumulative_RM20"], 
                mode="lines+markers", 
                marker=dict(color=colors20),
                line=dict(color="white", width=2),
                name="Total"
            ))
            fig20.add_hline(y=0, line=dict(color="red", width=2, dash="dash"))
            # Layout Styling
            fig20.update_layout(
                title="Denom RM20 Trend",
                title_x=0.5,
                xaxis=dict(title="Time", tickangle=-45, showgrid=False),
                yaxis=dict(title="Cumulative RM20"),
                plot_bgcolor="black",
                paper_bgcolor="white",
                font=dict(color="black"),
                legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
            )

            fig50.add_trace(go.Scatter(
                x=df_final_true["Timestamp"], 
                y=df_final_true["Cumulative_RM50"], 
                mode="lines+markers", 
                marker=dict(color=colors50),
                line=dict(color="white", width=2),
                name="Total"
            ))
            fig50.add_hline(y=0, line=dict(color="red", width=2, dash="dash"))
            # Layout Styling
            fig50.update_layout(
                title="Denom RM50 Trend",
                title_x=0.5,
                xaxis=dict(title="Time", tickangle=-45, showgrid=False),
                yaxis=dict(title="Cumulative RM50"),
                plot_bgcolor="black",
                paper_bgcolor="white",
                font=dict(color="black"),
                legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
            )

            fig100.add_trace(go.Scatter(
                x=df_final_true["Timestamp"], 
                y=df_final_true["Cumulative_RM100"], 
                mode="lines+markers", 
                marker=dict(color=colors100),
                line=dict(color="white", width=2),
                name="Total"
            ))
            fig100.add_hline(y=0, line=dict(color="red", width=2, dash="dash"))
            # Layout Styling
            fig100.update_layout(
                title="Denom RM100 Trend",
                title_x=0.5,
                xaxis=dict(title="Time", tickangle=-45, showgrid=False),
                yaxis=dict(title="Cumulative RM100"),
                plot_bgcolor="black",
                paper_bgcolor="white",
                font=dict(color="black"),
                legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
            )

            # chart denom bar chart
            # Hitung total nilai positif dan negatif
            positive_sums = df_form[numeric_cols].apply(lambda x: x[x > 0].sum())
            negative_sums = df_form[numeric_cols].apply(lambda x: x[x < 0].sum())

            # Buat Bar Chart dengan Plotly
            fig_bar = go.Figure()

            fig_bar.add_trace(go.Bar(
                x=positive_sums.index, 
                y=positive_sums.values,
                name="Deposit",
                marker_color="dark blue"
            ))

            fig_bar.add_trace(go.Bar(
                x=negative_sums.index, 
                y=negative_sums.values,
                name="Dispense",
                marker_color="#87CEFA"
            ))

            fig_bar.update_layout(
                title="Total Deposit and Dispense",
                xaxis_title="Denomination",
                yaxis_title="# of Notes",
                barmode="relative"
            )
            fig_bar.add_hline(y=0, line=dict(color="red", width=2, dash="dash"))

            st.markdown(f"<h5>{combined_text}</h5>", unsafe_allow_html=True)
            # Menampilkan Grafik
            st.plotly_chart(fig_bar)
            col1, col2 = st.columns(2)
            col1.plotly_chart(fig, use_container_width=True)
            col2.plotly_chart(fig20, use_container_width=True)
            col3, col4 = st.columns(2)
            col3.plotly_chart(fig50, use_container_width=True)
            col4.plotly_chart(fig100, use_container_width=True)
            
            st.write(df_form)

        else:
            st.error("Please upload files to process.")

#cassettes capacity analysis
with tab3:
    st.text("Welcome to the Cassette capacity analysis. Please upload the file you would like to cassette capacity.")

    def analysis_cassette(uploaded_cass):
        output = []
        kata = "in cassette : Succeeded"
        kata2 = "Stored banknote :"
        kata3 = "==>"

        for uploaded_cass1 in uploaded_cass:
            # Read the file content as string
            file_content = uploaded_cass1.getvalue().decode("utf-8")

            # Split content into lines
            all_lines = file_content.splitlines()
            
            # Search for the specific keyword in the lines
            for i, line in enumerate(all_lines):
                if kata in line:
                    
                    # Extract relevant lines based on your logic
                    line_a = all_lines[i + 2]  # Next line after the found line
                    line_b = all_lines[i - 1]  # Two lines after the found line
                    
                    # Split the lines to extract specific data
                    id_polos = line_a.split(":")
                    id_polos1 = [item[1:] for item in id_polos]
                    cass1 = id_polos1[0] if len(id_polos1) > 0 else None  # Ensure the index exists
                    cass2 = id_polos1[1] if len(id_polos1) > 1 else None
                    cass3 = id_polos1[2] if len(id_polos1) > 2 else None
                    cass4 = id_polos1[3] if len(id_polos1) > 3 else None
                    cass5 = id_polos1[4] if len(id_polos1) > 4 else None
                    cass6 = id_polos1[5] if len(id_polos1) > 5 else None
                    cass7 = id_polos1[6] if len(id_polos1) > 6 else None
                    
                    id_polos_time = line_b.split(" ")
                    time = id_polos_time[4] if len(id_polos_time) > 3 else None
                    # Extract the date from the file name
                    df2 = uploaded_cass1.name
                    wsid = df2.split('-')
                    tanggal = wsid[1]
                    # Append extracted data to the output list, but only once per occurrence
                    output.append([ter, tanggal, time, cass1, cass2, cass3, cass4, cass5, cass6, cass7])

                elif kata2 in line:
                    line_a = all_lines[i + 3]  # Next line after the found line
                    line_b = all_lines[i]
                    
                    # Split the lines to extract specific data
                    id_polos = line_a.split(":")
                    id_polos1 = [item[1:] for item in id_polos]
                    cass1 = id_polos1[0] if len(id_polos1) > 0 else None  # Ensure the index exists
                    cass2 = id_polos1[1] if len(id_polos1) > 1 else None
                    cass3 = id_polos1[2] if len(id_polos1) > 2 else None
                    cass4 = id_polos1[3] if len(id_polos1) > 3 else None
                    cass5 = id_polos1[4] if len(id_polos1) > 4 else None
                    cass6 = id_polos1[5] if len(id_polos1) > 5 else None
                    cass7 = id_polos1[6] if len(id_polos1) > 6 else None

                    id_polos_time = line_b.split(" ")
                    time = id_polos_time[4] if len(id_polos_time) > 3 else None
                    # Extract the date from the file name
                    df2 = uploaded_cass1.name
                    wsid = df2.split('-')
                    tanggal = wsid[1]
                    # Append extracted data to the output list, but only once per occurrence
                    output.append([ter, tanggal, time, cass1, cass2, cass3, cass4, cass5, cass6, cass7])

                elif kata3 in line:
                    line_id = i
                    id_ter = all_lines[line_id].split(" ")
                    ter = id_ter[6] if len(id_ter) > 6 else 'N/A'
                    output.append([ter])
                
                   
        return output
        

    # File uploader to upload multiple files
    uploaded_cass = st.file_uploader("Choose a file", accept_multiple_files=True, key="file_uploader_3")

    st.header("Cassette Capacity")
    
    # Start button to trigger the analysis
    if st.button("START", key="start_button_3"):
        if uploaded_cass:
            # Call the analysis function and display results
            df3 = analysis_cassette(uploaded_cass)
            df_final = pd.DataFrame(df3)
            df_final.rename(columns={0:'ID', 1:'Date', 2:'Time', 3:'Cassette 1', 4:'Cassette 2',
            5:'Cassette 3', 6:'Cassette 4', 7:'Cassette MIX', 8:'Reject', 9:'Retract'}, inplace=True)
            
            try:
                df_final['Cassette 1'] = df_final['Cassette 1'].str.replace('A', '', regex=False)
                df_final['Date'] = df_final['Date'].str.replace('.txt', '', regex=False)
                #merge date and time
                df_final.insert(0, "Timestamp", df_final["Date"] + " " + df_final["Time"])
                df_final.drop(columns=["Date", "Time"], inplace=True)
                df_final = df_final.sort_values(by="Timestamp")
                df_final["Timestamp"] = pd.to_datetime(df_final["Timestamp"])
                df_final1 = df_final.reset_index(drop=True)
                df_final_true = df_final1.dropna()
                first_time = df_final_true["Timestamp"].iloc[0] 
                last_time = df_final_true["Timestamp"].iloc[-1]
                first_id = df_final_true["ID"].iloc[0]

                combined_text = f"Period: {first_time} - {last_time} | Terminal ID: {first_id}"
                
                #graph
                df_graph = df_final_true[["Timestamp", "Cassette 1", "Cassette 2", "Cassette 3", "Cassette 4", "Cassette MIX", "Reject", "Retract"]]
                df_long = df_graph.melt(id_vars=["Timestamp"], var_name="Cassette", value_name="# of Notes")
                fig = px.line(df_long, x="Timestamp", y="# of Notes", color="Cassette", title="Capacity of Cassettes", color_discrete_sequence=px.colors.qualitative.Plotly)
                
                st.markdown(f"<h5>{combined_text}</h5>", unsafe_allow_html=True) 
                st.plotly_chart(fig, use_container_width=True)
                st.write(df_final_true)


            except KeyError:
                st.write("No data to display.")
            
            #st.write(df_final)
            #st.dataframe(df_final)
        else:
            st.error("Please upload files to process.")
