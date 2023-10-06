from xml.dom import minidom
from dataclasses import dataclass
from datetime import datetime
from typing import List

INPUT_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%f%z"
OUTPUT_DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


@dataclass
class TrackPoint:
    time: datetime
    distance_meters: float

    def to_xml(self) -> str:
        return f"""
            <Trackpoint>
                <Time>{self.time.strftime(OUTPUT_DATE_FORMAT)}</Time>
                <DistanceMeters>{self.distance_meters}</DistanceMeters>
            </Trackpoint>
        """

    @classmethod
    def from_xml(cls, track_point: minidom.Element):
        time = datetime.strptime(
            track_point.getElementsByTagName("Time")[0].firstChild.data, INPUT_DATE_FORMAT)
        distance_meters = track_point.getElementsByTagName("DistanceMeters")[0].firstChild.data
        return cls(time, distance_meters)


@dataclass
class Track:
    track_points: List[TrackPoint]

    def to_xml(self) -> str:
        return f"""
            <Track>
                {" ".join([track_point.to_xml() for track_point in self.track_points])}
            </Track>
        """

    @classmethod
    def from_xml(cls, track: minidom.Element):
        track_points = [TrackPoint.from_xml(track_point) for track_point in track.getElementsByTagName("Trackpoint")]
        return cls(track_points)


@dataclass
class Lap:
    start_time: datetime
    total_time_seconds: float
    distance_meters: float
    calories: float
    intensity: str
    trigger_method: str
    tracks: List[Track]

    def to_xml(self):
        return f"""
            <Lap StartTime="{self.start_time.strftime(OUTPUT_DATE_FORMAT)}">
                <TotalTimeSeconds>{self.total_time_seconds}</TotalTimeSeconds>
                <DistanceMeters>{self.distance_meters}</DistanceMeters>
                <Calories>{self.calories}</Calories>
                <Intensity>{self.intensity}</Intensity>
                <TriggerMethod>{self.trigger_method}</TriggerMethod>
                {" ".join([track.to_xml() for track in self.tracks])}
            </Lap>
        """

    @classmethod
    def from_xml(cls, lap: minidom.Element):
        start_time = datetime.strptime(lap.getAttribute("StartTime"), "%Y-%m-%dT%H:%M:%S.%f%z")
        total_time_seconds = lap.getElementsByTagName("TotalTimeSeconds")[0].firstChild.data
        distance_meters = lap.getElementsByTagName("DistanceMeters")[0].firstChild.data
        calories = lap.getElementsByTagName("Calories")[0].firstChild.data
        intensity = lap.getElementsByTagName("Intensity")[0].firstChild.data
        trigger_method = lap.getElementsByTagName("TriggerMethod")[0].firstChild.data
        tracks = [Track.from_xml(track) for track in lap.getElementsByTagName("Track")]
        return cls(start_time, total_time_seconds, distance_meters, calories, intensity, trigger_method, tracks)


@dataclass
class Version:
    version_major: int
    version_minor: int
    build_major: int
    build_minor: int

    def to_xml(self):
        return f"""
            <Version>
                <VersionMajor>{self.version_major}</VersionMajor>
                <VersionMinor>{self.version_minor}</VersionMinor>
                <BuildMajor>{self.build_major}</BuildMajor>
                <BuildMinor>{self.build_minor}</BuildMinor>
            </Version>
        """

    @classmethod
    def from_xml(cls, version: minidom.Element):
        version_major = version.getElementsByTagName("VersionMajor")[0].firstChild.data
        version_minor = version.getElementsByTagName("VersionMinor")[0].firstChild.data
        build_major = version.getElementsByTagName("BuildMajor")[0].firstChild.data
        build_minor = version.getElementsByTagName("BuildMinor")[0].firstChild.data
        return cls(version_major, version_minor, build_major, build_minor)


@dataclass
class Creator:
    name: str
    unit_id: str
    product_id: str
    version: Version

    def to_xml(self):
        return f"""
            <Creator xsi:type="Device_t">
                <Name>{self.name}</Name>
                <UnitId>{self.unit_id}</UnitId>
                <ProductID>{self.product_id}</ProductID>
                {self.version.to_xml()}
            </Creator>
        """


@dataclass
class Activity:
    sport: str
    id: str
    laps: List[Lap]
    creator: Creator = None

    def to_xml(self):
        return f"""
            <Activity Sport="{self.sport}">
                <Id>{self.id}</Id>
                {self.creator.to_xml() if self.creator else ""}
                {" ".join([lap.to_xml() for lap in self.laps])}
            </Activity>
        """

    @classmethod
    def from_xml(cls, activity: minidom.Element):
        sport = activity.getAttribute("Sport")
        id = activity.getElementsByTagName("Id")[0].firstChild.data
        laps = [Lap.from_xml(lap) for lap in activity.getElementsByTagName("Lap")]
        return cls(sport, id, laps)


@dataclass
class Author:
    name: str
    build: Version
    lang_id: str
    part_number: str

    def to_xml(self):
        return f"""
            <Author xsi:type="Application_t">
                <Name>{self.name}</Name>
                <Build>{self.build.to_xml()}</Build>
                <LangID>{self.lang_id}</LangID>
                <PartNumber>{self.part_number}</PartNumber>
            </Author>
        """

    @classmethod
    def from_xml(cls, author: minidom.Element):
        name = author.getElementsByTagName("Name")[0].firstChild.data
        build = Version.from_xml(author.getElementsByTagName("Build")[0])
        lang_id = author.getElementsByTagName("LangID")[0].firstChild.data
        part_number = author.getElementsByTagName("PartNumber")[0].firstChild.data
        return cls(name, build, lang_id, part_number)


@dataclass
class TrainingCenterDatabase:
    activities: List[Activity]
    author: Author

    def to_xml(self):
        return f"""
            <TrainingCenterDatabase xmlns="http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2"
                                    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                                    xmlns:ns2="http://www.garmin.com/xmlschemas/UserProfile/v2"
                                    xmlns:ns3="http://www.garmin.com/xmlschemas/ActivityExtension/v2"
                                    xmlns:ns4="http://www.garmin.com/xmlschemas/ProfileExtension/v1"
                                    xmlns:ns5="http://www.garmin.com/xmlschemas/ActivityGoals/v1"
                                    xsi:schemaLocation="http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2 
                                    http://www.garmin.com/xmlschemas/TrainingCenterDatabasev2.xsd">
                {self.author.to_xml()}
                {" ".join([activity.to_xml() for activity in self.activities])}
            </TrainingCenterDatabase>
        """

    def to_file(self, path: str):
        xml = self.to_xml()
        doc = minidom.parseString(xml)
        with open(path, "w") as f:
            doc.writexml(f, encoding="utf-8")

    @classmethod
    def from_xml(cls, xml: str):
        document = minidom.parseString(xml)
        activities = [Activity.from_xml(activity) for activity in document.getElementsByTagName("Activity")]
        return cls(
            author=Author.from_xml(document.getElementsByTagName("Author")[0]),
            activities=activities
        )

    def collapse_activities(self):
        sport = self.activities[0].sport
        id = self.activities[0].id
        laps = []
        laps.extend([activity.laps[0] for activity in self.activities])
        total_time = round(sum([float(lap.total_time_seconds) for lap in laps]))
        total_distance = round(sum([float(lap.distance_meters) for lap in laps]))
        total_calories = round(sum([float(lap.calories) for lap in laps]))
        track_points = []
        track_points.extend([track_point for lap in laps for track in lap.tracks for track_point in track.track_points])
        lap = Lap(
            start_time=laps[0].start_time,
            total_time_seconds=total_time,
            distance_meters=total_distance,
            calories=total_calories,
            intensity="Active",
            trigger_method="Manual",
            tracks=[Track(track_points)]
        )
        self.activities = [Activity(sport, id, [lap])]
        return self
