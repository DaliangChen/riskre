from models.frequency import sample_frequency
from models.severity import sample_severity

def simulate_annual_loss(config):
    n_events = sample_frequency(config)
    losses = sample_severity(n_events, config)
    return losses
