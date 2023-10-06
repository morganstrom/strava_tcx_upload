from datetime import datetime
from models import Author, TrainingCenterDatabase, TrackPoint, INPUT_DATE_FORMAT, Track, Lap, Activity, Creator, Version


def test_from_xml():
    # given
    with open("tests/resources/input.tcx", "r") as f:
        xml = f.read()

    # when
    training_center_database = TrainingCenterDatabase.from_xml(xml)

    # then
    assert len(training_center_database.activities) == 35


def test_track_point():
    # given
    timestamp = datetime.strptime("2019-10-29T05:57:09.037Z", INPUT_DATE_FORMAT)
    track_point = TrackPoint(timestamp, 0.0)

    # when
    xml = track_point.to_xml()

    # then
    assert type(xml) == str
    print(xml)


def test_track():
    # given
    timestamp = datetime.strptime("2019-10-29T05:57:09.037Z", INPUT_DATE_FORMAT)
    track = Track([TrackPoint(timestamp, 0.0), TrackPoint(timestamp, 1.0)])

    # when
    xml = track.to_xml()

    # then
    assert type(xml) == str
    print(xml)


def test_lap():
    # given
    timestamp = datetime.strptime("2019-10-29T05:57:09.037Z", INPUT_DATE_FORMAT)
    track = Track([TrackPoint(timestamp, 0.0)])
    lap = Lap(timestamp, 0.0, 0.0, 0.0, "Active", "Manual", [track])

    # when
    xml = lap.to_xml()

    # then
    assert type(xml) == str
    print(xml)


def test_creator():
    # given
    version = Version(1, 0, 0, 0)
    creator = Creator("Garmin", "0", "Garmin Connect API - Python", version)

    # when
    xml = creator.to_xml()

    # then
    assert type(xml) == str
    print(xml)


def test_activity():
    # given
    timestamp = datetime.strptime("2019-10-29T05:57:09.037Z", INPUT_DATE_FORMAT)
    track = Track([TrackPoint(timestamp, 0.0)])
    lap = Lap(timestamp, 0.0, 0.0, 0.0, "Active", "Manual", [track])
    version = Version(1, 0, 0, 0)
    creator = Creator("Garmin", "0", "Garmin Connect API - Python", version)
    activity = Activity("Weight_Training", "alsvgds", [lap], creator)

    # when
    xml = activity.to_xml()

    # then
    assert type(xml) == str
    print(xml)


def test_author():
    # given
    author = Author("Garmin", Version(1, 0, 0, 0), "en", "1234")

    # when
    xml = author.to_xml()

    # then
    assert type(xml) == str
    print(xml)


def test_to_xml():
    # given
    author = Author("Garmin", Version(1, 0, 0, 0), "en", "1234")
    timestamp = datetime.strptime("2019-10-29T05:57:09.037Z", INPUT_DATE_FORMAT)
    track = Track([TrackPoint(timestamp, 0.0)])
    lap = Lap(timestamp, 0.0, 0.0, 0.0, "Active", "Manual", [track])
    version = Version(1, 0, 0, 0)
    creator = Creator("Garmin", "0", "Garmin Connect API - Python", version)
    activity = Activity("Weight_Training", "alsvgds", [lap], creator)

    training_center_database = TrainingCenterDatabase([activity], author)

    # when
    xml = training_center_database.to_xml()

    # then
    assert type(xml) == str
    print(xml)


def test_collapse_activities():
    # given
    with open("tests/resources/input.tcx", "r") as f:
        xml = f.read()

    # when
    training_center_database = TrainingCenterDatabase.from_xml(xml)
    training_center_database.collapse_activities()

    # then
    assert len(training_center_database.activities) == 1
    assert len(training_center_database.activities[0].laps) == 1
    assert len(training_center_database.activities[0].laps[0].tracks[0].track_points) == 70
