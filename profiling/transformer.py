from core.profile.calculation import poc, value_area, edge

"""
process the raw profile data for creating
the to_profile output
"""


class Transformer:
    """
    Process the raw profile data and create a dictionary of a single given profile
    """

    def to_profile(self, profile):
        try:
            profile = Transformer.__process_profile(profile)

            # Convert the profile into two list
            profile_price, profile_volume = zip(*profile.items())
            res = [profile_price, profile_volume]
            return res
        except Exception as err:
            print(err)

    def __process_profile(self, profile):
        try:
            p = {}
            for key, value in profile.items():
                p[key] = value[profile_type]
            return p
        except Exception as err:
            print(err)
            print('Could not process the profile for {}'.format(profile))

    @staticmethod
    def __process_array(profile, profile_type):
        try:
            res = []
            for key, value in profile.items():
                delta = Delta_profile.run(value)
                bid_volume, ask_volume = Bid_ask_profile.run(value)
                data = {'Price_index': key,
                        'Price_volume': value[profile_type],
                        'Delta': delta,
                        'bid_volume': bid_volume,
                        'ask_volume': ask_volume
                        }
                res.append(data)
            return res
        except Exception as err:
            print(err)
            print('failed at {} for {}'.format(profile_type, profile))

    """
    Process the raw profile data
    and create an array of
    a single given profiling
    """
    @staticmethod
    def to_array(profile, profile_type):
        try:
            if profile_type == 'Buy':
                profile = Transformer.__process_array(profile, profile_type)
            elif profile_type == 'Sell':
                profile = Transformer.__process_array(profile, profile_type)
            elif profile_type == 'Profile':
                profile = Transformer.__process_array(profile, profile_type)
            return profile
        except Exception as err:
            print('Could not build the profiling{}'.format(profile))

    ''' All calculations at one place '''

    @staticmethod
    def __calculations(profile, profile_type, value_area_pct):
        cal_profile = Transformer.to_profile(profile, profile_type)
        poc_volume, poc_price, _ = POC.get(cal_profile)
        lower_edge, upper_edge = Edge.run(cal_profile, value_area_pct)
        value_area = Volueme_Area.run(cal_profile, value_area_pct)
        profile = Transformer.to_array(profile, profile_type)
        return profile, poc_volume, poc_price, upper_edge, lower_edge, value_area

    @staticmethod
    def to_dict(profile, profile_type, value_area_pct):
        profile, poc_volume, poc_price, upper_edge, lower_edge, value_area = Transformer.__calculations(profile,
                                                                                                        profile_type,
                                                                                                        value_area_pct)
        profile_dict = {
            "open_time": 0,
            "close_time": 0,
            "volume_area": value_area,
            "lower_edge_price": lower_edge,
            "upper_edge_price": upper_edge,
            "poc_volume": poc_volume,
            "poc_price": poc_price,
            "volume_profiles": profile}
        return profile_dict
