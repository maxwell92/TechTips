def main():
    acl_secret = {}
    print type(acl_secret)
    #acl_secret.setdefault("mushroom", ["1. mogu", "2. magic"])
    acl_secret.setdefault("mushroom", []).append("1. mogu")
    #print type(acl_secret.setdefault("mushroom", []))
    #print acl_secret
    print acl_secret["mushroom"]
    print acl_secret.get("mushroom")
main();
