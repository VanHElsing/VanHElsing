from src.schedulers.EAuto import EAutoScheduler


def init_scheduler(problem, time_limit, scheduler_id, model=None):
    # TODO: Read ID from config file
    scheduler = choose_scheduler(scheduler_id)
    return scheduler(problem, time_limit, model)


def choose_scheduler(scheduler_id):
    if scheduler_id == 'EAuto':
        return EAutoScheduler
    else:
        raise IOError(99, 'Unknown scheduler ID %s ' % scheduler_id)