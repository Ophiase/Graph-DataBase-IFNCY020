from dataclasses import dataclass


@dataclass
class Work:
    id: int
    worktype: str
    primary_title: str
    original_title: str
    is_adult: int
    start_year: int
    end_year: int
    runtime_minutes: int


@dataclass
class Akas:
    id_work: int
    ordering: int
    title: str
    region: str
    language: str
    attributes: str
    is_original_title: int


@dataclass
class Episode:
    id_work: int
    id_work_parent: int
    season_number: int
    episode_number: int


@dataclass
class Genre:
    id_work: int
    genre: str


@dataclass
class WorkType:
    id_work: int
    ordering: int
    type: str


@dataclass
class Person:
    id_person: int
    name: str
    birth_year: int
    death_year: int


@dataclass
class Profession:
    id_work: int
    ordering: int
    id_person: int
    category: str
    job: str
    characters: str


@dataclass
class Director:
    id_work: int
    id_person: int


@dataclass
class Writer:
    id_work: int
    id_person: int


@dataclass
class KnownFor:
    id_person: int
    id_work: int
