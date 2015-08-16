from cassiopeia import baseriotapi
import .setup

def test_all():
    print("dto/championapi tests...")
    test_champion_status()
    test_champion_statuses()

def test_champion_status():
    setup.test_result(baseriotapi.get_champion_status(setup.champion_id))

def test_champion_statuses():
    setup.test_result(baseriotapi.get_champion_statuses())