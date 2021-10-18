from rir_data.models.indicator import Indicator
from rir_data.models.scenario import ScenarioLevel


def overall_scenario() -> ScenarioLevel:
    """ Return overall scenario level """

    scenarios = {}
    for indicator in Indicator.list():
        scenario_level = indicator.scenario_level
        level = f'{scenario_level.level}'
        if level not in scenarios:
            scenarios[level] = {
                'scenario': scenario_level,
                'count': 0
            }
        scenarios[level]['count'] += 1

    overall = None
    for level, scenario in scenarios.items():
        if not overall:
            overall = scenario
        else:
            if scenario['count'] == overall['count']:
                if scenario['scenario'].level < overall['scenario'].level:
                    overall = scenario
            elif scenario['count'] > overall['count']:
                overall = scenario
    return overall['scenario']
