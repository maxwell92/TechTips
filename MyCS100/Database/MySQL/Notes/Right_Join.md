SELECT user.name, organization.name FROM user RIGHT JOIN organization ON user.orgId=organization.id;
