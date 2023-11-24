# import keyboard as keyboard
# import mysql.connector
# from mysql.connector import Error
#
# import serial
#
# # Replace 'COMx' with the actual port name on your PC
# ser = serial.Serial('COM11', 115200)  # Use the same baud rate as in your Arduino code
# ser.close()
# # Initialize user information
# name = input("Enter your name: ")
# age = input("Enter your age: ")
# gender = input("Enter your gender: ")
# # Initialize lists to store sensor data for each position
# sensor_data_list = []
#
# position = 1
# try:
#     while position <= 13:
#         # Display a message and wait for the user to press Enter
#         input(f"Position {position}: Are you ready? Press Enter when ready...")
# pp
#         ser = serial.Serial('COM11', 115200)  # Use the same baud rate as in your Arduino code
#         data=[]
#         # Read data from Arduino
#         while True:
#             if keyboard.is_pressed("enter"):
#                 data = ser.readline().decode().strip()
#
#                 break
#
#         sensor_values = data.split(',')
#         # Check if the received data is valid
#         if len(sensor_values) == 33:
#             # Split the received data into individual sensor values
#             # Print received sensor values
#             print(f"Position {position}: Received Sensor Values:")
#             for i, value in enumerate(sensor_values):
#                 print(f"Channel {i}: {value}")
#             print(data)
#             sensor_values.pop()
#             # Store sensor data for this position
#             sensor_data_list.append(sensor_values)
#
#             # Increment the position
#             position += 1
#
#             ser.close()
#         else:
#             ser.close()
#             print("다시 입력해야해요")
# except serial.SerialException as e:
#     print("Serial port error:", e)
# finally:
#     # Close the serial port when done
#     if ser.is_open:
#         ser.close()
#         print("Serial port closed")
#
# # Now you can access sensor_data_list to process the sensor data as needed
# print(sensor_data_list)
# # DB
# # Replace these with your MySQL database credentials
# db_config = {
#     'host': 'udm.accx.dev',  # Hostname or IP address
#     'port': 50101,           # Port number
#     'database': 'breadseat',
#     'user': 'breadseat',
#     'password': 'KiUzZHnghVzLpnM5'
# }
#
# try:
#     # Connect to the MySQL database
#     conn = mysql.connector.connect(**db_config)
#
#     if conn.is_connected():
#         print("Connected to MySQL database")
#
#         # Create a cursor object to execute SQL commands
#         cursor = conn.cursor()
#
#         # Iterate through the sensor data list and insert into the database
#         for position, sensor_values in enumerate(sensor_data_list, start=1):
#             posture_type = position  # You can set the posture type based on the position
#
#             # Prepare the INSERT statement
#             insert_data_query = '''INSERT INTO Test_Data (PostureType, SD1, SD2, SD3, SD4, SD5, SD6, SD7, SD8, SD9,
#                                                          SD10, SD11, SD12, SD13, SD14, SD15, SD16, SD17, SD18, SD19,
#                                                          SD20, SD21, SD22, SD23, SD24, SD25, SD26, SD27, SD28, SD29,
#                                                          SD30, SD31, SD32)
#                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
#                                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
#             # Convert the sensor values to integers
#             sensor_values = [int(value) for value in sensor_values]
#
#             # Execute the INSERT statement
#             cursor.execute(insert_data_query, [posture_type] + sensor_values)
#
#         # Commit the changes to the database
#         conn.commit()
#
# except Error as e:
#     print("Error:", e)
# finally:
#     # Close the database connection when done
#     if 'conn' in locals() and conn.is_connected():
#         cursor.close()
#         conn.close()
#         print("MySQL connection closed")
import tkinter as tk
import colorsys

def pressure_to_color(pressure_value):
    normalized_value = pressure_value / 500.0  # 최대 센서 값으로 가정, 500
    hue = 0 if normalized_value >= 1.0 else (1.0 - normalized_value) * 0.5  # 색상 매핑 조정
    rgb = colorsys.hsv_to_rgb(hue, 1, 1)
    return '#%02x%02x%02x' % (int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))

def create_rectangles(data, start_y):
    rectangles = []
    total_width = len(data) * 50 + (len(data) - 1) * 10
    start_x = (1000 - total_width) // 2
    for i, pressure in enumerate(data):
        x = start_x + i * (50 + 10)
        y = start_y
        rect = canvas.create_rectangle(x, y, x + 50, y + 50, fill=pressure_to_color(pressure), outline="black")
        text = canvas.create_text(x + 25, y + 25, text=str(pressure))
        rectangles.append((rect, text))
    return rectangles

def update_rectangles(rectangles, data):
    for i, pressure in enumerate(data):
        rect, text = rectangles[i]
        canvas.itemconfig(rect, fill=pressure_to_color(pressure))
        canvas.itemconfig(text, text=str(pressure))

def on_button_click():
        data_str = text_box.get()
        data_list = [int(i) for i in data_str.split()]
        last_row_data = [data_list[8], data_list[5], data_list[2]]
        middle_row_data = [data_list[7], data_list[4], data_list[1]]
        first_row_data = [data_list[6], data_list[3], data_list[0]]
        update_rectangles(first_rectangles, first_row_data)
        update_rectangles(middle_rectangles, middle_row_data)
        update_rectangles(last_rectangles, last_row_data)

app = tk.Tk()
app.title("센서 데이터 시각화 프로그램")
canvas = tk.Canvas(app, height=600, width=1000)
canvas.pack()

first_rectangles = create_rectangles([0]*3, 20)
middle_rectangles = create_rectangles([0]*3, 90)
last_rectangles = create_rectangles([0]*3, 160)

text_box = tk.Entry(app, width=80)
text_box.pack()
button = tk.Button(app, text="Update Data", command=on_button_click)
button.pack()

app.mainloop()
