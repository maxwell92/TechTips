def main():
    list1 = ["1", "2"]
    list2 = ["2", "3"]
    print list1
    print list2

    list3 = list(set(list1) - set(list2))
    list4 = list(set(list2) - set(list1))
    print list3
    print list4

main()
