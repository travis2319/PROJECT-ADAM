import requests
import json

def send_data_to_server(obd_df, gps_df=None):
    # Convert dataframes to JSON format
    obd_data = obd_df.to_dict(orient="records")
    data = {"obd_data": obd_data}
    # data={}
    # Add GPS data if available
    if gps_df is not None:
        gps_data = gps_df.to_dict(orient="records")
        # data["gps_data"] = gps_data
        data = {
            "gps_data": gps_data,
            "obd_data": obd_data
        }

    # Send data to server
    url = "http://localhost:8080/jsonupload"  # Replace with your server's endpoint
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, data=json.dumps(data), headers=headers)

        if response.status_code == 200:
            print("Data sent successfully.")
            return True
        else:
            print("Failed to send data. Server responded with:", response.status_code)
            return False
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)
        return False

def send_csv_to_server(file_path):
    url = "http://localhost:3000/upload"  # Replace with your server's endpoint
    
    # sending temp.csv to go server
    try:
        with open(file_path, 'rb') as file:
            files = {'file': file}
            response = requests.post(url, files=files)

            if response.status_code == 200:
                print("CSV file sent successfully.")
                return True
            else:
                print("Failed to send CSV file. Server responded with:", response.status_code)
                return False
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)
        return False
