from app.models.organizations_model import organizationsCollection
from app.views.organization_schema import OrganizationSchema, OrganizationRoles

def test_create_organization(_organization):
    organization_id = organizationsCollection.create_organization(_organization)
    assert organization_id is not None

def test_retrieve_organization_by_id(_organization):
    retrieved_organization = organizationsCollection.retrieve_organization_by_id(_organization.id)
    assert retrieved_organization is not None
    assert retrieved_organization.organization_name == _organization.organization_name

def test_retrieve_user_organizations(_organization, _user):
    user_organizations = organizationsCollection.retrieve_user_organizations(_user.id)
    assert user_organizations is not None
    assert len(user_organizations) > 0

def test_user_has_role(_organization, _user):
    user_has_role = organizationsCollection.user_has_role(_user.id, _organization.id, OrganizationRoles.admin)
    assert user_has_role is True

def test_invalid_user_has_role(_organization, _invalid_user):
    user_has_role = organizationsCollection.user_has_role(_invalid_user.id, _organization.id, OrganizationRoles.admin)
    assert user_has_role is False

# def test_delete_organization(_organization):
#     organizationsCollection.delete_organization(_organization.id)
#     removed_organization = organizationsCollection.delete_organization(_organization.id)
#     assert removed_organization is True
