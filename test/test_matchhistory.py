import arrow

import cassiopeia as cass
from cassiopeia import Season, Queue, Summoner


def test_match_history_1():
    region = "NA"
    summoner = Summoner(name="Kalturi", region=region)
    match_history = cass.get_match_history(summoner=summoner, queues={Queue.ranked_solo_fives})
    assert len(match_history) > 400


def test_match_history_2():
    region = "NA"
    summoner = Summoner(name="Kalturi", region=region)
    match_history = cass.get_match_history(summoner=summoner, seasons={Season.season_9}, queues={Queue.ranked_solo_fives}, begin_time=arrow.now().shift(days=-140), end_time=arrow.now())
    assert len(match_history) > 0


def test_match_history_3():
    region = "NA"
    summoner = Summoner(name="Kalturi", region=region)
    match_history = cass.get_match_history(summoner=summoner, queues={Queue.ranked_solo_fives}, begin_time=arrow.get(2019, 10, 1), end_time=arrow.get(2019, 10, 31))
    assert len(match_history) == 6


def test_match_history_5():
    region = "NA"
    summoner = Summoner(name="Kalturi", region=region)
    match_history = cass.get_match_history(summoner=summoner, seasons={Season.season_9}, queues={Queue.ranked_solo_fives}, begin_time=arrow.get(2019, 1, 1), end_time=arrow.now())
    assert len(match_history) > 0


def test_match_history_6():
    region = "NA"
    summoner = Summoner(name="Kalturi", region=region)
    match_history = cass.get_match_history(summoner=summoner, queues={Queue.ranked_solo_fives}, begin_time=arrow.get(2019, 10, 1), end_time=arrow.get(2019, 10, 31))
    assert len(match_history) > 0


def test_match_history_7():
    region = "NA"
    summoner = Summoner(name="Kalturi", region=region)
    match_history = cass.get_match_history(summoner=summoner, seasons={Season.season_9}, queues={Queue.ranked_solo_fives}, begin_time=arrow.get(2019, 10, 1))
    assert len(match_history) > 0


def test_match_history_8():
    summoner = cass.Summoner(name="chowdog", region="NA")
    mh = cass.get_match_history(summoner=summoner, begin_index=0, end_index=20, queues={Queue.ranked_solo_fives})
    match = mh[0]
    assert len(match.participants) == 10
