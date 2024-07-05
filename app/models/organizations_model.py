"""This module contains the model for interacting with the organizations collection in the database"""

from typing import List

from app.models.mongodb_model import MongoCollection
from app.logging_config import models_logger
from app.views.organization_schema import OrganizationSchema, OrganizationRoles
from app.exceptions import ModelInDbException

class OrganizationsCollection(MongoCollection):
    """Class to interact with organizations collection in the database"""

    def __init__(self):
        super().__init__("organizations")

    def create_organization(self, organization: OrganizationSchema) -> str:
        """
        Create a new organization in the database
        """
        try:
            if not isinstance(organization, OrganizationSchema):
                raise ModelInDbException("Organization must be an instance of OrganizationSchema")

            # check for name field in organization
            if not organization.organization_name:
                raise ModelInDbException("Organization must have a name")

            organization_id = self.create_document(organization.model_dump(by_alias=True))
            return organization_id

        except Exception as e:
            models_logger.error(e)
            raise e
        
    def retrieve_organization_by_id(self, organization_id: str) -> OrganizationSchema:
        """Retrieve an organization by its id"""
        try:
            document = self.retrieve_document_by_id(organization_id)
            if document:
                return OrganizationSchema(**document)
            
        except Exception as e:
            models_logger.warning(e)
            raise e

    def retrieve_user_organizations(self, user_id: str) -> List[OrganizationSchema]:
        """
        Retrieve all organizations for a single user
        A single user can be part of multiple organizations
        """

        try:
            organizations = self.retrieve_documents_by_fields({"members." + user_id: {"$exists": True}})
            if organizations:
                return [OrganizationSchema(**organization) for organization in organizations]
            return organizations

        except Exception as e:
            models_logger.error(e)
            raise e
    
    def user_has_role(self, user_id: str, organization_id: str, desired_role: OrganizationRoles) -> bool:
        """
        Check if a user has a desired role in an given organization
        """

        try:
            organization = self.retrieve_organization_by_id(organization_id)
            if organization:
                roles_hierarchy = OrganizationRoles.get_roles_hierarchy()
                user_role = organization.members.get(user_id)
                if user_role:
                    return roles_hierarchy[user_role] >= roles_hierarchy[desired_role]
            return False

        except Exception as e:
            models_logger.error(e)
            raise e
        
    def add_user_to_organization(self, user_id: str, organization_id: str, role: OrganizationRoles):
        """
        Add a user to an organization
        """

        try:

            if not isinstance(role, OrganizationRoles):
                raise ModelInDbException("Role must be an instance of OrganizationRoles")

            organization = self.retrieve_organization_by_id(organization_id)
            if organization:
                organization.members[user_id] = role.value
                result = self.edit_document_by_id(organization_id, organization.model_dump(by_alias=True))
                if result:
                    return True
            return False

        except Exception as e:
            models_logger.error(e)

    def remove_user_from_organization(self, user_id: str, organization_id: str):
        """
        Remove a user from an organization
        """

        try:
            organization = self.retrieve_organization_by_id(organization_id)
            if organization:
                organization.members.pop(user_id, None)
                result = self.edit_document_by_id(organization_id, organization.model_dump(by_alias=True))
                if result:
                    return True
            return False

        except Exception as e:
            models_logger.error(e)
        
    def delete_organization(self, organization_id: str):
        """Delete an organization from the database"""
        try:
            result = self.delete_document(organization_id)
            models_logger.debug(f"Organization deleted: {result}")
            return result
        except Exception as e:
            models_logger.error(e)
            raise e

organizationsCollection = OrganizationsCollection()

if __name__ == "__main__":
    organizationsCollection = OrganizationsCollection()
    organization1 = OrganizationSchema(
        id="e6c56ca5-e695-4325-a9a7-29a96d2fc4e7",
        organization_name="Test Organization 2",
        owner_id="e6c56ca5-e695-4325-a9a7-29a96d2fc4e7",
        members={
            "e6c56ca5-e695-4325-a9a7-29a96d2fc4e7": OrganizationRoles.admin.value,
            "e6c56ca5-e695-4325-a9a7-29a96d2fc4e4": OrganizationRoles.manager.value,
            }
    )

    organization2 = OrganizationSchema(
        id="e6c56ca5-e695-4325-a9a7-29a96d2fc4e4",
        organization_name="Test Organization 1",
        owner_id="e6c56ca5-e695-4325-a9a7-29a96d2fc4e7",
        members={
            "e6c56ca5-e695-4325-a9a7-29a96d2fc4e7": OrganizationRoles.admin.value,
            "e6c56ca5-e695-4325-a9a7-29a96d2fc4e2": OrganizationRoles.user.value,
            }
    )
    
    organization1_id = organizationsCollection.create_organization(organization1)
    organization2_id = organizationsCollection.create_organization(organization2)
    print(f"Organization1 ID: {organization1_id}")
    print(f"Organization2 ID: {organization2_id}")

    user_id1 = "e6c56ca5-e695-4325-a9a7-29a96d2fc4e7"
    organizations = organizationsCollection.retrieve_user_organizations(user_id1)
    print(f"User {user_id1} is part of the following organizations: {organizations}")

    user_id2 = "e6c56ca5-e695-4325-a9a7-29a96d2fc4e2"
    organizations = organizationsCollection.retrieve_user_organizations(user_id2)
    print(f"User {user_id2} is part of the following organizations: {organizations}")

    user_id3 = "e6c56ca5-e695-4325-a9a7-29a96d2fc4e1"
    organizations = organizationsCollection.retrieve_user_organizations(user_id3)
    print(f"User {user_id3} is part of the following organizations: {organizations}")

    #check if user1 has access viewer role in organization1
    print(organizationsCollection.user_has_role(user_id1, organization1_id, OrganizationRoles.admin))
    print(organizationsCollection.user_has_role(user_id2, organization2_id, OrganizationRoles.user))

    #delete organizations
    organizationsCollection.delete_organization(organization1_id)
    organizationsCollection.delete_organization(organization2_id)
