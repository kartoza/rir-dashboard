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


def get_level_instance_in_tree(instance, level_instances) -> dict:
    """
    Return level instance in tree
    """
    from rir_data.models import GeometryLevelInstance
    levels = {}
    for top in level_instances:
        levels[top.level.id] = {
            'parent': top.parent.id if top.parent else 0,
            'child': get_level_instance_in_tree(
                instance,
                GeometryLevelInstance.objects.filter(
                    instance=instance,
                    parent=top.level
                )
            )
        }

    return levels
