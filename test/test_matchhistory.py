import arrow

import cassiopeia as cass
from cassiopeia import Season, Queue, Summoner


def test_match_history_1():
    region = "NA"
    summoner = Summoner(name="Kalturi", account=34718348, id=21359666, region=region)
    match_history = cass.get_match_history(summoner=summoner, queues={Queue.ranked_solo_fives})
    assert len(match_history) > 400


def test_match_history_2():
    region = "NA"
    summoner = Summoner(name="Kalturi", account=34718348, id=21359666, region=region)
    match_history = cass.get_match_history(summoner=summoner, seasons={Season.season_8}, queues={Queue.ranked_solo_fives}, begin_time=arrow.now().shift(days=-140), end_time=arrow.now())
    assert len(match_history) > 0


def test_match_history_3():
    region = "NA"
    summoner = Summoner(name="Kalturi", account=34718348, id=21359666, region=region)
    match_history = cass.get_match_history(summoner=summoner, queues={Queue.ranked_solo_fives}, begin_time=arrow.get(2017, 2, 7), end_time=arrow.get(2017, 2, 14))
    assert len(match_history) == 16


def test_match_history_4():
    region = "NA"
    summoner = Summoner(name="Kalturi", account=34718348, id=21359666, region=region)
    match_history = cass.get_match_history(summoner=summoner, seasons={Season.season_8}, queues={Queue.ranked_solo_fives}, begin_time=arrow.get(2016, 1, 1), end_time=arrow.get(2016, 1, 11))
    assert len(match_history) == 0


def test_match_history_5():
    region = "NA"
    summoner = Summoner(name="Kalturi", account=34718348, id=21359666, region=region)
    match_history = cass.get_match_history(summoner=summoner, seasons={Season.season_8}, queues={Queue.ranked_solo_fives}, begin_time=arrow.get(2016, 1, 1), end_time=arrow.now())
    assert len(match_history) > 0


def test_match_history_6():
    region = "NA"
    summoner = Summoner(name="Kalturi", account=34718348, id=21359666, region=region)
    match_history = cass.get_match_history(summoner=summoner, queues={Queue.ranked_solo_fives}, begin_time=arrow.get(2016, 12, 1), end_time=arrow.get(2016, 12, 30))
    assert len(match_history) > 0


def test_match_history_7():
    region = "NA"
    summoner = Summoner(name="Kalturi", account=34718348, id=21359666, region=region)
    match_history = cass.get_match_history(summoner=summoner, seasons={Season.season_8}, queues={Queue.ranked_solo_fives}, begin_time=arrow.get(2016, 12, 1))
    assert len(match_history) > 0


def test_match_history_8():
    summoner = cass.Summoner(name="chowdog", region="NA")
    mh = cass.get_match_history(summoner=summoner, begin_index=0, end_index=20)
    match = mh[0]
    assert len(match.participants) == 10
