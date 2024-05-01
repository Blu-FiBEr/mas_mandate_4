import simulator2

def test_match_index2():
    list1 = [1,4,3,6,7,5,9,8,2]
    count = simulator2.match_index2(list1)
    print(count)

def main():
    """
    This main is only used to test the scenario creation methods implemented in this package.
    :return:
    """
    test_match_index2()

if __name__ == '__main__':
    main()