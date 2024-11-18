import java.util.*;


public class one{

    Queue<Integer> q = new LinkedList<>();
    Semaphore empty = new Semaphore(10);
    Semaphore full = new Semaphore(0);
    Mutex mutex = new Mutex();
    Integer items_produced = 10;
    Integer buffer_size = 10;
    class Semaphore{
        int value;
        Semaphore(int val)
        {
            value =val;
        }
        public synchronized void acquire_buffer() throws InterruptedException
        {
            while(value==0)
            {
                wait();
            }
            value = value-1;
        }
        public synchronized void release_buffer() throws InterruptedException
        {
            value += 1;
            notify();
        }
    }
    class Mutex{
        boolean is_locked = false;
        public synchronized void lock() throws InterruptedException
        {
            while(is_locked)
            {
                wait();
            }
            is_locked = false;
        }
        public synchronized void unlock() throws InterruptedException
        {
            is_locked = false;
        }
    }
    class Producer implements Runnable{
        public void run()
        {
            while (true) {
                try {
                    while(items_produced>0)
                    {
                        empty.acquire_buffer();
                        mutex.lock();
                        System.out.println("Items produced by " + items_produced + "....");
                        q.add(items_produced);
                        items_produced = items_produced -1;
                        mutex.unlock();
                        full.release_buffer();
                        Thread.sleep(1500);
                    }
                } catch (Exception e) {
                    System.out.println("Error in producing");
                }
            }
        }
    }
    class Consumer implements Runnable
    {
        public void run()
        {
            while (true) {
                try {
                    full.acquire_buffer();
                    mutex.lock();
                    while(!q.isEmpty())
                    {  
                        int item = q.poll();
                        System.out.println("Items consumed by " + item + "....");
                        mutex.unlock();
                        empty.release_buffer();
                        Thread.sleep(1500);
                    }
                } catch (Exception e) {
                   System.out.println("Error in consuming");
                }
            }
        }
    }
    public static void main(String[] args) {
        one obj = new one();
        Thread producer = new Thread(obj.new Producer());
        Thread consumer = new Thread(obj.new Consumer());
        producer.start();
        consumer.start();
    }
}