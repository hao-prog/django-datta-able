from core.settings import DEGREE_ARR, SPECIALIZED_ARR  # import the settings file


def common_dictionary(request):
    # return the value you want as a dictionnary. you may add multiple values in there.
    return {"SPECIALIZED_ARR": SPECIALIZED_ARR, "DEGREE_ARR": DEGREE_ARR}
