from typing import Iterator

import pytest


@pytest.fixture
def demo_fixture() -> Iterator[tuple[int, int]]:
    print("1. SETUP SOME MOCKS / OTHER RESOURCES")
    yield (6, 7)
    print("2. TEAR DOWN / RESET CHANGES")


def test_six_seven(demo_fixture: tuple[int, int]):
    print("3.")
    six, seven = demo_fixture
    assert six == 6
    assert seven == 7
    print("4.")
