import requests
import json
import sys


class PelotonApi:
    def __init__(self, email, password):
        self.session, self.user_id = self.get_peloton_session(email, password)
        self.BASE_URL = 'https://api.pelotoncycle.com/api'


    def get_peloton_session(self, email, password):
        """
            get a logged-in requests session to the peloton API, and the user ID
        """
        session = requests.Session()
        r = session.post('https://api.pelotoncycle.com/auth/login',
                        json={'username_or_email': email,
                              'password': password})
        if r.status_code == 200:
            return session, r.json().get('user_id')
        else:
            raise Exception("can't get a session!")
            sys.exit()


    def get_peloton_data(self, url):
        """
            query the peloton API and return a python object
        """
        r = self.session.get(f'{self.BASE_URL}{url}')
        # print(f'fetching URL {url}')
        if r.status_code == 200:
            # print(f'  returning {r.json()}')
            return r.json()
        else:
            print(f'error getting pelo data: {r.text}')
            return {}

    def getXWorkouts(self, numWorkouts):
        """
            Gets the latest x workouts from Peloton.
        """
        return self.get_peloton_data(f'/user/{self.user_id}/workouts?joins=peloton.ride&limit={numWorkouts}&page=0&sort_by=-created').get('data', [])


    def getLatestWorkout(self):
        """
            get the latest workout from Peloton
        """
        workouts = self.getXWorkouts(1)
        return workouts[0]


    def getWorkoutById(self, workoutId):
        """
            get workout from peloton by id.
        """
        return self.get_peloton_data(f'/workout/{workoutId}?joins=peloton,peloton.ride,peloton.ride.instructor,user')


    def getWorkoutSamplesById(self, workoutId):
        """
            get workout samples from peloton by id
        """
        return self.get_peloton_data(f'/workout/{workoutId}/performance_graph?every_n=1')


    def getWorkoutSummaryById(self, workoutId):
        """
            get workout summary from peloton by id
        """
        return self.get_peloton_data(f'/workout/{workoutId}/summary')

