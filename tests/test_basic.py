# encoding: utf-8
#
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import pytest

import sql
from tidservice import TIDService

config = None


@pytest.fixture
def service(new_db):
    if new_db == 'yes':
        return TIDService(conn=sql.Sql(":memory:"))
    elif new_db == 'no':
        return TIDService(conn=sql.Sql("resources/test.db"))


def test_new_then_old(service):
    # delete database then run this test
    old = service.get_tids("/testing/geckodriver/CONTRIBUTING.md", "6162f89a4838")
    new = service.get_tids("/testing/geckodriver/CONTRIBUTING.md", "06b1a22c5e62")
    assert len(new) == len(old)
    for i in range(0, len(old)):
        assert old[i] == new[i]


def test_tids_on_changed_file(service):
    # https://hg.mozilla.org/integration/mozilla-inbound/file/a6fdd6eae583/taskcluster/ci/test/tests.yml
    old_lines = service.get_tids(  # 2205 lines
        "/taskcluster/ci/test/tests.yml", "a6fdd6eae583"
    )

    # THE FILE HAS NOT CHANGED, SO WE EXPECT THE SAME SET OF TIDs AND LINES TO BE RETURNED
    # https://hg.mozilla.org/integration/mozilla-inbound/file/a0bd70eac827/taskcluster/ci/test/tests.yml
    same_lines = service.get_tids(  # 2201 lines

        "/taskcluster/ci/test/tests.yml", "a0bd70eac827"
    )

    # assertAlmostEqual PERFORMS A STRUCURAL COMPARISION
    assert len(old_lines) == len(same_lines)

    # THE FILE HAS FOUR LINES REMOVED
    # https://hg.mozilla.org/integration/mozilla-inbound/rev/c8dece9996b7
    # https://hg.mozilla.org/integration/mozilla-inbound/file/c8dece9996b7/taskcluster/ci/test/tests.yml
    # 2201 lines
    new_lines = service.get_tids(
        "/taskcluster/ci/test/tests.yml", "c8dece9996b7"
    )

    # EXPECTING
    assert len(new_lines) == len(old_lines) - 4


def test_remove_file(service):
    no_lines = service.get_tids("/third_party/speedometer/InteractiveRunner.html", "e3f24e165618")
    assert 0 == len(no_lines)


def test_generic_1(service):
    old = service.get_tids("/gfx/ipc/GPUParent.cpp", "a5a2ae162869")
    new = service.get_tids("/gfx/ipc/GPUParent.cpp", "3acb30b37718")
    assert len(old) == 467
    assert len(new) == 476
    for i in range(1, 207):
        assert old[i] == new[i]


def test_500_file(service):
    # this file has no history (nore should it have tuids)
    # calling hg will return a 500 error
    tuids = service.get_tids("/browser/tools/mozscreenshots/mozscreenshots/extension/lib/robot_upperleft.png", "d3ed36f4fb7a")
    assert len(tuids) == 0


def test_file_with_line_replacement(service):
    new = service.get_tids("/python/mozbuild/mozbuild/action/test_archive.py", "e3f24e165618")
    old = service.get_tids("/python/mozbuild/mozbuild/action/test_archive.py", "c730f942ce30")
    assert 653 == len(new)
    assert 653 == len(old)
    for i in range(0, 600):
        if i == 374 or i == 376:
            assert old[i] != new[i]
        else:
            assert old[i] == new[i]


def test_distant_rev(service):
    old = service.get_tids("/python/mozbuild/mozbuild/action/test_archive.py", "e3f24e165618")
    new = service.get_tids("/python/mozbuild/mozbuild/action/test_archive.py", "0d1e55d87931")
    assert len(old) == 653
    assert len(new) == 653
    for i in range(0, 653):
        assert new[i] == old[i]


def test_new_file(service):
    rev = service.get_tids("/media/audioipc/server/src/lib.rs", "a39241b3e7b1")
    assert len(rev) == 636
