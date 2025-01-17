from multiprocessing import Process, Queue

def push(q, items):
    """아이템을 큐에 추가하는 함수."""
    for pid, item in enumerate(items, start=1):
        q.put(item)
        print(f'item No: {pid} {item}')

def pop(q):
    """큐에서 아이템을 꺼내는 함수."""
    i = 0
    while not q.empty():  # 큐가 비어 있지 않은 동안 실행
        print(f'item No: {i} {q.get()}')
        i += 1

if __name__ == '__main__':
    items = ['red', 'blue', 'green', 'black']
    q = Queue()

    # `push` 프로세스 생성
    print('pushing items to queue:')
    producer = Process(target=push, args=(q, items))
    producer.start()  # 프로세스 시작

    # `pop` 프로세스 생성
    print('popping items from queue:')
    consumer = Process(target=pop, args=(q,))
    consumer.start()  # 프로세스 시작

    # 모든 프로세스가 종료될 때까지 기다림
    producer.join()
    consumer.join()
