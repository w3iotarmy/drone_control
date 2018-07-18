import json
class JsonBuilderClass:
    @staticmethod
    def get_start_information(vehicle):
        start_data = {}
        start_data['u'] = 'eagle'
        start_data['action'] = 'gps'
        start_data['lat'] = vehicle.location.global_frame.lat
        start_data['lon'] = vehicle.location.global_frame.lon
        start_data['mode'] =  vehicle.mode.name
        json_data = json.dumps(start_data)
        return json_data

    @staticmethod
    def get_is_arm():
        start_data = {}
        start_data['u'] = 'eagle'
        start_data['action'] = 'arm'
        json_data = json.dumps(start_data)
        return json_data

    @staticmethod
    def get_is_takeoff():
        start_data = {}
        start_data['u'] = 'eagle'
        start_data['action'] = 'takeoff'
        json_data = json.dumps(start_data)
        return json_data

    @staticmethod
    def get_is_no_waypoint():
        start_data = {}
        start_data['u'] = 'eagle'
        start_data['action'] = 'no_waypoint'
        json_data = json.dumps(start_data)
        return json_data
    @staticmethod
    def get_location_information(lat,lon,alt):
        start_data = {}
        start_data['u'] = 'eagle'
        start_data['action'] = 'location'
        start_data['lat'] = lat
        start_data['lon'] = lon
        start_data['alt'] = alt
        json_data = json.dumps(start_data)
        return json_data

    @staticmethod
    def get_battery_information(voltage,current,level):
        start_data = {}
        start_data['u'] = 'eagle'
        start_data['action'] = 'battery'
        start_data['voltage'] = voltage
        start_data['current'] = current
        start_data['level'] = level
        json_data = json.dumps(start_data)
        return json_data

    @staticmethod
    def get_all_information(b_voltage, b_current, b_level,gps_fix,gps_num_sat,gps_lat,gps_lon,gps_alt):
        start_data = {}
        start_data['u'] = 'eagle'
        start_data['action'] = 'all_info'
        start_data['b_voltage'] = b_voltage
        start_data['b_current'] = b_current
        start_data['b_level'] = b_level
        start_data['gps_fix'] = gps_fix
        start_data['gps_num_sat'] = gps_num_sat
        start_data['gps_lat'] = gps_lat
        start_data['gps_lon'] = gps_lon
        start_data['gps_alt'] = gps_alt
        json_data = json.dumps(start_data)
        return json_data

    @staticmethod
    def get_mode_information(mode):
        start_data = {}
        start_data['u'] = 'eagle'
        start_data['action'] = 'mode'
        start_data['data'] = mode
        json_data = json.dumps(start_data)
        return json_data

    @staticmethod
    def get_gps_inf_information(fix,sat):
        start_data = {}
        start_data['u'] = 'eagle'
        start_data['action'] = 'gps_info'
        start_data['fix'] = fix
        start_data['sat_num'] = sat
        json_data = json.dumps(start_data)
        return json_data

    @staticmethod
    def get_waypoint_received_response():
        start_data = {}
        start_data['u'] = 'eagle'
        start_data['action'] = 'wp_res'
        start_data['value'] = True
        json_data = json.dumps(start_data)
        return json_data