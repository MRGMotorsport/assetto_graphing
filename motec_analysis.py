# Motec Data Analysis For Improving Laptime

import pandas as pd
import plotly.express as px


# Files Required
analysis_file = r'c:\YOUR_USER_PATH\458gt2_comparison_lap.csv'
ref_file = r'c:\YOUR_USER_PATH\458gt2_fast_lap.csv'
track_left_wall = r'c:\YOUR_USER_PATH\spa_left_side.csv'
track_right_wall = r'c:\YOUR_USER_PATH\spa_right_side.csv'


# FUNCTIONS

def get_metadata(file_url, lap_type):

    # initialise data list to then become a pd df
    metadata_rows = []

    # open and read first 11 lines of the file and remove any examples of column 7 data
    with open(file_url, 'r') as file:
        for i in range(11):
            line = file.readline().strip().split(',') # readline does what it says, strip removes any \n characters or any unwanted punctuation, and split splits the string into a list of substings based on the argument it is given, in this case ','
            if len(line) == 7:
                line = line[:-1] # remove the last column if there are 7 values of data in the line
            metadata_rows.append(line)

    metadata_df = pd.DataFrame(metadata_rows)

    metadata_dict = {
        "Format" : metadata_df.iloc[0,1],
        "Venue" : metadata_df.iloc[1,1],
        "Vehicle" : metadata_df.iloc[2,1],
        "Driver" : metadata_df.iloc[3,1],
        "Device" : metadata_df.iloc[4,1],
        "Comment" : metadata_df.iloc[5,1],
        "Log Date" : metadata_df.iloc[6,1],
        "Log Time" : metadata_df.iloc[7,1],
        "Sample Rate" : metadata_df.iloc[8,1],
        "Session Duration" : metadata_df.iloc[9,1],
        "Session Range" : metadata_df.iloc[10,1],
        "Session Type" : metadata_df.iloc[5,5],
        "Origin Time" : metadata_df.iloc[6,5],
        "Start Time" : metadata_df.iloc[7,5],
        "End Time" : metadata_df.iloc[8,5],
        "Start Distance" : metadata_df.iloc[9,5],
        "End Distance" : metadata_df.iloc[10,5]
    }

    # print the keys and values from the dict
    print(": ",lap_type," :","\n")
    for key, value in zip(metadata_dict.keys(),metadata_dict.values()):
        print(f"{key}: {value}")

def get_dataframe(file_url):

    # get the headers
    headers = pd.read_csv(file_url,skiprows=13, nrows=1).columns.to_list()

    # read the csv and skip first 7 rows anbd then drop the 2nd row
    data = pd.read_csv(file_url, skiprows=15, names=headers)
    #data = data.drop(2)

    # reset the row index
    data.reset_index(drop=True, inplace=True)

    return data

#   METADATA

# print the metadata for both the laps
get_metadata(ref_file,"Base Lap")
print("\n")
get_metadata(analysis_file, "Compare Lap")
print("\n")

#   DATA FILES

df1 = get_dataframe(ref_file)
df2 = get_dataframe(analysis_file)
df_lw = get_dataframe(track_left_wall)
df_rw = get_dataframe(track_right_wall)

# Add a driver column

df1['Driver'] = 'James G'
df2['Driver'] = input("Please enter the driver's name:  ")
df_lw['Driver'] = 'Track Limits Left'
df_rw['Driver'] = 'Track Limits Right'

# prints the first few rows for checking

print(df1.head())
print(df2.head())

# concatinate the dataframes

data = pd.concat([df1, df2, df_lw, df_rw], ignore_index=True)
data_without_track_limits = pd.concat([df1, df2], ignore_index=True)

print(data.head())




#   GRAPHS

# 3d track map ------------------------------------------

#df = px.data
fig1 = px.line_3d(data, x='Car Coord X', y='Car Coord Y', z='Car Coord Z', color='Driver', title= 'XYZ Position')

#lock the axis sizes
fig1.update_layout(scene=dict(
        xaxis=dict(range=[-1500,1500], title='X Axis (m)'),
        yaxis=dict(range=[-1500,1500], title='Y Axis (m)'),
        zaxis=dict(range=[-1500,1500], title='Z Axis (m)')
    ))
fig1.show()


# steering angle against distance chart ------------------------------------------

fig2 = px.line(data_without_track_limits, x='Distance', y='Steering Angle', color = 'Driver', title='Steering Angle Against Distance')
fig2.show()
 

# brake pedal position  ------------------------------------------

fig3 = px.line(data_without_track_limits, x='Distance', y='Brake Pos', color='Driver', title='Brake Pos Against Distance')
fig3.show()


# delta t -------------------------------------------

fig4 = px.line(data_without_track_limits, x='Distance', y='Time', color='Driver', title='Delta T')
fig4.show()


# speed ------------------------------------------------

fig5 = px.line(data_without_track_limits, x='Distance', y='Ground Speed', color='Driver', title='Speed')
fig5.show()


# g-g diagram -----------------------------------------------

fig6 = px.scatter(data_without_track_limits, x='CG Accel Lateral', y='CG Accel Longitudinal', color='Driver', title='G-G')
fig6.update_layout( xaxis=dict(range=[-3,3], title='X Axis Accel (ms^-2)') , yaxis=dict(range=[-3,3], title='Y Axis Accel (ms^-2)') )
fig6.show()


 










"""
These are graphs that I am working on as there are currently a few issues


# ride height against distance chart
data_long = data.melt(id_vars=['Distance'], value_vars=['Suspension Travel FL', 'Suspension Travel FR', 'Suspension Travel RL', 'Suspension Travel RR'], var_name='Wheel', value_name='Suspension Travel')
fig3 = px.line(data_long, x='Distance', y='Suspension Travel', color='Wheel', title='Suspension Travel Against Distance')
fig3.show()




# Gears against distance
fig9 = px.line(data_without_track_limits, x='Distance', y='Gear', color = 'Driver' , title='Gear Against Distance')
fig9.show()





# tire load against distance chart
data_long = data.melt(id_vars=['Distance'], value_vars=['Tire Load FL', 'Tire Load FR', 'Tire Load RL', 'Tire Load RR'], var_name='Wheel', value_name='Tire Load')
fig4 = px.line(data_long, x='Distance', y='Tire Load', color='Wheel', title='Tire Load Against Time')
fig4.show()





# tire pressure against time chart
data_long = data.melt(id_vars=['Distance'], value_vars=['Tire Pressure FL', 'Tire Pressure FR', 'Tire Pressure RL', 'Tire Pressure RR'], var_name='Wheel', value_name='Tire Pressure')
# create the line plot
fig7 = px.line(data_long, x='Distance', y='Tire Pressure', color='Wheel', title='Tire Pressure Over Distance')
fig7.show()




# Currently working on getting an animated 2d track map
# 2D track map  ------------------------------------------

fig2 = px.line(data, x='Car Coord X', y='Car Coord Y',color='Driver', title= 'XY Position')

# Create the scatter plot for the moving point
scatter = go.Scatter(
    x=[data['Car Coord X'][0]], 
    y=[data['Car Coord Y'][0]], 
    mode='markers', 
    marker=dict(color='red', size=10)
)

# Add scatter plot to the figure
fig2.add_trace(scatter)

#lock the axis sizes
fig2.update_layout( xaxis=dict(range=[-1200,1200], title='X Axis (m)') , yaxis=dict(range=[-1200,1200], title='Y Axis (m)') )


# Create frames for the animation
frames = [go.Frame(data=[go.Scatter(x=[data['Car Coord X'][k]], y=[data['Car Coord Y'][k]], mode='markers', marker=dict(color='red', size=10))],
                   name=str(k)) for k in range(len(data))]

# Add frames to the figure
fig2.frames = frames

# Add the play button and slider to the layout
fig2.update_layout(
    updatemenus=[dict(
        type="buttons",
        showactive=False,
        buttons=[
            dict(label="Play",
                 method="animate",
                 args=[None, dict(frame=dict(duration=100, redraw=True), fromcurrent=True)]),
            dict(label="Pause",
                 method="animate",
                 args=[[None], dict(frame=dict(duration=0, redraw=False), mode="immediate")])
        ]
    )],
    sliders=[dict(
        steps=[dict(method='animate', args=[[str(k)], dict(mode='immediate', frame=dict(duration=100, redraw=True))], label=str(k)) for k in range(len(data))],
        active=0
    )]
) 
# Show the figure
fig2.show()

"""


