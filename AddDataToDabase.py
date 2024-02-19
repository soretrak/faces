import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://ecommerce-c6a64-default-rtdb.europe-west1.firebasedatabase.app/"
})


ref = db.reference('Agent')
data = {
    "1015":
        {
            "name": "Fakhri Kharrat",
            "major": "Robotics",
            "starting_year": 2017,
            "total_attendance": 6,
            "standing": "G",
            "year": 4,
            "last_attendance_time": "2024-01-01 00:54:30"
        },
    "1000":
        {
            "name": "Yassine Kharrat",
            "major": "Robotics",
            "starting_year": 2022,
            "total_attendance": 6,
            "standing": "G",
            "year": 4,
            "last_attendance_time": "2024-01-01 00:54:30"
        },
    "1014":
        {
            "name": "Aya Zrigue",
            "major": "Computer sciences",
            "starting_year": 2020,
            "total_attendance": 2,
            "standing": "G",
            "year": 4,
            "last_attendance_time": "2024-01-01 00:54:30"
        },
    "1023":
        {
            "name": "Bechir",
            "major": "Robotics",
            "starting_year": 2017,
            "total_attendance": 6,
            "standing": "G",
            "year": 4,
            "last_attendance_time": "2024-01-01 00:54:30"
        },
    "1199":
        {
            "name": "Mohamed",
            "major": "Driver",
            "starting_year": 2010,
            "total_attendance": 6,
            "standing": "G",
            "year": 4,
            "last_attendance_time": "2024-01-01 00:54:30"
        },
     "1124":
        {
            "name": "Tarek Fatnassi",
            "major": "Driver",
            "starting_year": 2010,
            "total_attendance": 6,
            "standing": "G",
            "year": 4,
            "last_attendance_time": "2024-01-01 00:54:30"
        }
}
for key,value in data.items():
    ref.child(key).set(value)
