import cpca

if __name__ == '__main__':
    location_str = ["顺德区", "呼和浩特", "福州", "广州", "南昌", "合肥"]
    df = cpca.transform(location_str)
    print(df)