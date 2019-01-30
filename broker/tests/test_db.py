import db
import pytest




def test_uuid():
    uuid1 = db.get_a_uuid()
    uuid2 = db.get_a_uuid()

    assert uuid1 != uuid2

def test_invalid_db():
    ret = db.initialize_database()
    assert ret != False

def test_create_new_database(temp_database):
    ret=db.initialize_database(temp_database)
    assert ret != False

def test_create_duplicate_database(temp_database):
    ret=db.initialize_database(temp_database)
    print(ret)
    assert ret != False
    ret = db.initialize_database(temp_database)
    print(ret)
    assert ret != False

def test_insert_good_records(temp_database):
    ret,msg = db.insert_into_database(temp_database, "guest", NAME="testemail", DEVICE="testdeviceid", STATUS="initiated", TEAMSROOMID="testteamsroom")
    assert ret != False

    ret, msg = db.insert_into_database(temp_database, "device", NAME="testdevice")
    assert ret != False

    ret, msg = db.insert_into_database(temp_database, "domain", NAME="testdomain")
    assert ret != False

@pytest.mark.parametrize("database", ["domain","device"])
def test_insert_duplicate_records(temp_database,database):

    ret, msg = db.insert_into_database(temp_database, database, NAME="duptestdevice1")
    assert ret != False
    ret, msg = db.insert_into_database(temp_database, database, NAME="duptestdevice1")
    assert ret == False

    ret, msg = db.insert_into_database(temp_database, database, NAME="duptestdomain1")
    assert ret != False
    ret, msg = db.insert_into_database(temp_database, database, NAME="duptestdomain1")
    assert ret == False


def test_insert_bad_record(temp_database):
    ret, msg = db.insert_into_database(temp_database, "badtable", NAME="field doesn't exist")
    assert ret == False

def test_insert_bad_field(temp_database):
    ret, msg = db.insert_into_database(temp_database, "guest", BADCOLUMN="column doesn't exist")
    assert ret== False

@pytest.mark.parametrize("database", ["guest","domain","device"])
def test_search_db(temp_database,database):
    ret = db.search_db(temp_database,database)
    ret1 = db.search_db(temp_database,database)
    assert ret == ret1

@pytest.mark.parametrize("database", ["domain","device"])
def test_search_db(temp_database,database):
    ret, msg = db.insert_into_database(temp_database, database, NAME="searchname")
    assert ret != False
    ret,msg = db.search_database(temp_database,database,"NAME","searchname")
    assert ret == True

    ret, msg = db.search_database(temp_database, database, "NAME", "definitelynotfound")
    assert ret != True


