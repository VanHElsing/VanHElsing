from src.schedulers.EAuto import EAutoScheduler

def init_scheduler(problem, time_limit, Id, model=None):
    # TODO: Read ID from config file
    scheduler = choose_scheduler(Id)
    return scheduler(problem, time_limit, model)

def choose_scheduler(Id):
    if Id == 'EAuto':
        return EAutoScheduler
    else:
        raise IOError(99,'Unknown scheduler ID %s ' % Id)

