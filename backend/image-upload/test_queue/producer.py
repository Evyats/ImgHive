import celery_app



def first_test():
    r1 = celery_app.add.delay(2, 3)
    r2 = celery_app.add.delay(10, 20)

    print("Sent tasks!")
    print("r1 id:", r1.id)
    print("r2 id:", r2.id)

    print("Result 1:", r1.get(timeout=10))
    print("Result 2:", r2.get(timeout=10))



def main():
    pass
    for _ in range(10):
        celery_app.add.delay(1,2)





if __name__ == "__main__":
    main()