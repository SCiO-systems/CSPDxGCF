from flask import Flask, render_template, request, redirect, url_for, session
from flask import send_from_directory
import pandas as pd
import folium
from folium.plugins import HeatMap
import geopandas as gpd

# Create the application object and set a secret key (to be updated later)
app = Flask(__name__)
app.secret_key = 'key'


sector_mapping = {
    "Sector_1": "Health Sector",
    "Sector_2": "Food Security",
    "Sector_3": "Water Security",
    "Sector_4": "Infrastructure and Environment",
    "Sector_5": "Livelihoods of People and Communities",
    "Sector_6": "Ecosystems and Ecosystem Services",
    "Sector_7": "Energy Generation and Access",
    "Sector_8": "Buildings, Cities, Industries, and Appliances",
    "Sector_9": "Transport",
    "Sector_10": "Forests and Land Use"
}

# Starting page of the CSPD Dashboard
@app.route('/intro')
def intro():
    with open("data/data_modal.txt", "r") as f:
        data_modal = f.read()
    return render_template('intro.html',data_modal=data_modal)

# 'About' page in the CSPD Website
@app.route('/about')
def about():
    with open("data/data_modal.txt", "r") as f:
        data_modal = f.read()
    return render_template('about.html', data_modal=data_modal)

@app.route('/data/<filename>')
def data(filename):
    return send_from_directory('data', filename)

# 'Knowledge Hub' page in the CSPD Website
@app.route('/knowledgehub')
def knowledgehub():
    return render_template('knowledgehub.html')

# 'Contact Us' page in the CSPD Website
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Home page of the CSPD Dashboard
@app.route('/')
def home():
    return render_template('home.html')

# First step of the CSPD Dashboard (input 1: country and sectors)
@app.route('/step1', methods=['GET', 'POST'])
def step1():
    if request.method == 'POST':
        # Clear previous sector selections
        for i in range(1, 11):
            session.pop(f'Sector_{i}', None)
        
        # Store new form data in the session
        for key in request.form:
            session[key] = request.form.get(key)

        # Redirect to the risk profile page
        return redirect(url_for('step2'))
    else:
        # Clear previous sector selections when loading the page
        for i in range(1, 11):
            session.pop(f'Sector_{i}', None)
        
        return render_template('step1.html')

# Second step of the CSPD Dashboard (input 2: survey on project design)    
@app.route('/step2', methods=['GET', 'POST'])
def step2():
    if request.method == 'POST':
        a1 = 1 if request.form.get('A1') == 'yes' else 0
        a1p1 = 1 if request.form.get('A1.1') == 'yes' else 0
        a1p2 = 1 if request.form.get('A1.2') == 'yes' else 0
        a1p3 = 1 if request.form.get('A1.3') == 'yes' else 0
        a1p4 = 1 if request.form.get('A1.4') == 'yes' else 0
        a2 = 1 if request.form.get('A2') == 'yes' else 0
        a2p1 = 1 if request.form.get('A2.1') == 'yes' else 0
        a2p2 = 1 if request.form.get('A2.2') == 'yes' else 0
        a2p3 = 1 if request.form.get('A2.3') == 'yes' else 0
        a2p4 = 1 if request.form.get('A2.4') == 'yes' else 0
        a2p5 = 1 if request.form.get('A2.5') == 'yes' else 0
        a2p6 = 1 if request.form.get('A2.6') == 'yes' else 0
        b3 = 1 if request.form.get('B3') == 'yes' else 0
        b3p1 = 1 if request.form.get('B3.1') == 'yes' else 0
        b3p2 = 1 if request.form.get('B3.2') == 'yes' else 0
        b3p3 = 1 if request.form.get('B3.3') == 'yes' else 0
        b4 = 1 if request.form.get('B4') == 'yes' else 0
        b4p1 = 1 if request.form.get('B4.1') == 'yes' else 0
        b4p2 = 1 if request.form.get('B4.2') == 'yes' else 0
        b4p3 = 1 if request.form.get('B4.3') == 'yes' else 0
        b4p4 = 1 if request.form.get('B4.4') == 'yes' else 0
        c5 = 1 if request.form.get('C5') == 'yes' else 0
        c5p1 = 1 if request.form.get('C5.1') == 'yes' else 0
        c5p2 = 1 if request.form.get('C5.2') == 'yes' else 0
        c5p3 = 1 if request.form.get('C5.3') == 'yes' else 0
        c5p4 = 1 if request.form.get('C5.4') == 'yes' else 0
        c5p5 = 1 if request.form.get('C5.5') == 'yes' else 0
        c6 = 1 if request.form.get('C6') == 'yes' else 0
        c7 = 1 if request.form.get('C7') == 'yes' else 0

        session['a1'] = a1
        session['a1p1'] = a1p1
        session['a1p2'] = a1p2
        session['a1p3'] = a1p3
        session['a1p4'] = a1p4
        session['a2'] = a2
        session['a2p1'] = a2p1
        session['a2p2'] = a2p2
        session['a2p3'] = a2p3
        session['a2p4'] = a2p4
        session['a2p5'] = a2p5
        session['a2p6'] = a2p6
        session['b3'] = b3
        session['b3p1'] = b3p1
        session['b3p2'] = b3p2
        session['b3p3'] = b3p3
        session['b4'] = b4
        session['b4p1'] = b4p1
        session['b4p2'] = b4p2
        session['b4p3'] = b4p3
        session['b4p4'] = b4p4
        session['c5'] = c5
        session['c5p1'] = c5p1
        session['c5p2'] = c5p2
        session['c5p3'] = c5p3
        session['c5p4'] = c5p4
        session['c5p5'] = c5p5
        session['c6'] = c6
        session['c7'] = c7        
        
        # Compute sum for each category
        a_sum = a1 + a1p1 + a1p2 + a1p3 + a1p4 + a2 + a2p1 + a2p2 + a2p3 + a2p4 + a2p5 + a2p6
        b_sum = b3 + b3p1 + b3p2 + b3p3 + b4 + b4p1 + b4p2 + b4p3 + b4p4
        c_sum = c5 + c5p1 + c5p2 + c5p3 + c5p4 + c5p5 + c6 + c7

        # Assign category values based on (rounded)tertiles
        a_value = 1 if a_sum <= 4 else (2 if a_sum <= 8 else 3)
        b_value = 1 if b_sum <= 3 else (2 if b_sum <= 6 else 3)
        c_value = 1 if c_sum <= 3 else (2 if c_sum <= 5 else 3)
        aa_value = "Low" if a_sum <= 4 else ("Medium" if a_sum <= 8 else "High")
        bb_value = "Low" if b_sum <= 3 else ("Medium" if b_sum <= 6 else "High")
        cc_value = "Low" if c_sum <= 3 else ("Medium" if c_sum <= 5 else "High")
        
        # calculate mean of category values
        programming_mean = (a_value + b_value + c_value) / 3
        programming_value = 'Low' if programming_mean <= 1.33 else ('Medium' if programming_mean <= 2.66 else 'High')

        # Store in session
        session['a_value'] = a_value
        session['b_value'] = b_value
        session['c_value'] = c_value
        session['programming_value'] = programming_value
        session['aa_value'] = aa_value
        session['bb_value'] = bb_value
        session['cc_value'] = cc_value

        return redirect(url_for('risk_profile'))
    
    return render_template('step2.html')

# Third step of the CSPD Dashboard (outbput a: project profile based on input 1)
@app.route('/risk_profile')
def risk_profile():
    country = session.get('country')
    # Retrieve selected sectors from session and create a list of those that are checked
    selected_sectors = [str(i) for i in range(1, 11) if session.get(f'Sector_{i}') == 'true']

    if not country:
        return redirect(url_for('home'))
    
    with open("data/data_modal.txt", "r") as f:
        data_modal = f.read() 

    data = pd.read_csv('data/data_ACLED_INFORM.tsv', delimiter='\t')

    row = data.loc[data['ISO3'] == country].iloc[0]

    columns = ['COUNTRY','Conflict Risk', 'Institutional Risk', 'Socio-economic Risk', 
            'fatalities', 'Event Count', 'Sector_1_Percentage', 'Sector_2_Percentage', 
            'Sector_3_Percentage', 'Sector_4_Percentage', 'Sector_5_Percentage', 
            'Sector_6_Percentage', 'Sector_7_Percentage', 'Sector_8_Percentage', 
            'Sector_9_Percentage','Sector_10_Percentage',
            'Sector_1_Risk', 'Sector_2_Risk', 'Sector_3_Risk', 'Sector_4_Risk', 
            'Sector_5_Risk', 'Sector_6_Risk', 'Sector_7_Risk', 'Sector_8_Risk',
            'Sector_9_Risk', 'Sector_10_Risk', 
            'Aggregate Exposure Sector_1_Risk Category', 
            'Aggregate Exposure Sector_2_Risk Category', 
            'Aggregate Exposure Sector_3_Risk Category', 
            'Aggregate Exposure Sector_4_Risk Category', 
            'Aggregate Exposure Sector_5_Risk Category', 
            'Aggregate Exposure Sector_6_Risk Category', 
            'Aggregate Exposure Sector_7_Risk Category', 
            'Aggregate Exposure Sector_8_Risk Category',
            'Aggregate Exposure Sector_9_Risk Category',
            'Aggregate Exposure Sector_10_Risk Category']

    required_data = row[columns]

    user_data = {key: session.get(key) for key in session.keys()}

    # Create a mapping for the risk levels
    risk_level = {"Low": 1, "Medium": 2, "High": 3}

    # Find the maximum aggregate exposure among selected sectors
    highest_aggregate = "Low"
    for i in range(1, 11):
        if user_data.get(f'Sector_{i}') and risk_level[required_data[f'Aggregate Exposure Sector_{i}_Risk Category']] > risk_level[highest_aggregate]:
            highest_aggregate = required_data[f'Aggregate Exposure Sector_{i}_Risk Category']
            
    # Find the maximum aggregate exposure among selected sectors
    highest_sector_risk = "Low"
    for i in range(1, 11):
        if user_data.get(f'Sector_{i}') and risk_level[required_data[f'Sector_{i}_Risk']] > risk_level[highest_sector_risk]:
            highest_sector_risk = required_data[f'Sector_{i}_Risk']
            
    # Load ACLED data
    acled = pd.read_csv('data/ACLED_data.tsv', delimiter='\t')

    # Filter data for chosen country and selected sectors
    filtered_acled = acled.loc[
        (acled['ISO'] == country) & 
        (acled[selected_sectors].any(axis=1))
        ]

    # Create a GeoDataFrame
    gdf = gpd.GeoDataFrame(filtered_acled, geometry=gpd.points_from_xy(filtered_acled.longitude, filtered_acled.latitude))

    # Create a base map
    if filtered_acled['latitude'].isna().all() or filtered_acled['longitude'].isna().all():
        m = folium.Map(location=[0, 0], zoom_start=2)
    else:
        mean_latitude = filtered_acled['latitude'].dropna().mean()
        mean_longitude = filtered_acled['longitude'].dropna().mean()
        m = folium.Map(location=[mean_latitude, mean_longitude], zoom_start=5)

    # Add a heat map to the base map
    HeatMap(data=gdf[['latitude', 'longitude']].groupby(['latitude', 'longitude']).sum().reset_index().values.tolist(), radius=8, max_zoom=13).add_to(m)

    # Pass the session variables to the template
    a_value = session.get('a_value', 1)
    b_value = session.get('b_value', 1)
    c_value = session.get('c_value', 1)
    programming_value = session.get('programming_value', 'Low')
    aa_value = session.get('aa_value', 'Low')
    bb_value = session.get('bb_value', 'Low')
    cc_value = session.get('cc_value', 'Low')
    # Save variables to session
    session['highest_aggregate'] = highest_aggregate
    session['required_data'] = required_data.to_dict()

    # Pass the required variables to the template
    return render_template('risk_profile.html', data_modal=data_modal, data=required_data, country=country, user_data=user_data, highest_aggregate=highest_aggregate, highest_sector_risk=highest_sector_risk, map=m._repr_html_(), risk_level=risk_level, a_value=a_value, b_value=b_value, c_value=c_value, programming_value=programming_value, aa_value=aa_value, bb_value=bb_value, cc_value=cc_value)

# Fourth step of the CSPD Dashboard (output b: action points based on input 2)
@app.route('/action_points')
def action_points():
    selected_sectors = [f"Sector_{i}" for i in range(1, 11) if session.get(f"Sector_{i}") == "true"]
    # Filter action points based on the conditions
    highest_aggregate = session.get('highest_aggregate', 'Low')  # Assuming 'High' as the default value

    aa_value = session.get('aa_value', 'Low')
    bb_value = session.get('bb_value', 'Low')
    cc_value = session.get('cc_value', 'Low')
    
    required_data = session.get('required_data')
    if required_data:
        required_data = pd.DataFrame(required_data, index=[0])  # Convert dict back to DataFrame
    
    selected_sectors = []
    for i in range(1, 11):  # Assuming you have sectors numbered from 1 to 10
        sector_key = f"Sector_{i}"
        if session.get(sector_key) == "true":
            selected_sectors.append(sector_key)
            
    selected_sectors_names = []
    for i in range(1, 11):  # Assuming you have sectors numbered from 1 to 10
        sector_key = f"Sector_{i}"
        if session.get(sector_key) == "true":
            selected_sectors_names.append(sector_mapping[sector_key])
    
    a1=session.get('a1', '')
    a1p1=session.get('a1p1', '')
    a1p2=session.get('a1p2', '')
    a1p3=session.get('a1p3', '')
    a1p4=session.get('a1p4', '')
    a2=session.get('a2', '')
    a2p1=session.get('a2p1', '')
    a2p2=session.get('a2p2', '')
    a2p3=session.get('a2p3', '')
    a2p4=session.get('a2p4', '')
    a2p5=session.get('a2p5', '')
    a2p6=session.get('a2p6', '')
    b3=session.get('b3', '')
    b3p1=session.get('b3p1', '')
    b3p2=session.get('b3p2', '')
    b3p3=session.get('b3p3', '')
    b4=session.get('b4', '')
    b4p1=session.get('b4p1', '')
    b4p2=session.get('b4p2', '')
    b4p3=session.get('b4p3', '')
    b4p4=session.get('b4p4', '')
    c5=session.get('c5', '')
    c5p1=session.get('c5p1', '')
    c5p2=session.get('c5p2', '')
    c5p3=session.get('c5p3', '')
    c5p4=session.get('c5p4', '')
    c5p5=session.get('c5p5', '')
    c6=session.get('c6', '')
    c7=session.get('c7', '')

    user_data = {key: session.get(key) for key in session.keys()}
    return render_template('action_points.html', user_data=user_data, data=required_data, highest_aggregate=highest_aggregate, aa_value=aa_value, bb_value=bb_value, cc_value=cc_value, selected_sectors=selected_sectors, selected_sectors_names=selected_sectors_names,
                            a1=a1, a1p1=a1p1, a1p2=a1p2, a1p3=a1p3, a1p4=a1p4,a2=a2, a2p1=a2p1, a2p2=a2p2, a2p3=a2p3, a2p4=a2p4, a2p5=a2p5, a2p6=a2p6, b3=b3, b3p1=b3p1, b3p2=b3p2, b3p3=b3p3, b4=b4, b4p1=b4p1, b4p2=b4p2, b4p3=b4p3, b4p4=b4p4, c5=c5, c5p1=c5p1, c5p2=c5p2, c5p3=c5p3, c5p4=c5p4, c5p5=c5p5, c6=c6, c7=c7)

if __name__ == "__main__":
    app.run(debug=True)
