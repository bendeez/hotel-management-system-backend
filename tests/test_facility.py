from app.facility.schemas import FacilityCreate, FacilityOut

def test_create_facility(facility_service):
    facility_info = FacilityCreate(title="spa",description="place to relax")
    facility = facility_service.create_facility(facility=facility_info)
    assert FacilityOut(id=1, **facility.__dict__) == FacilityOut(id=1, **facility_info.model_dump())