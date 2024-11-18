import java.util.*;

public class mutex_semaphore {
    Queue<Integer> q = new LinkedList<>();
    Integer buffer_size = 10;
    Semaphore empty = new Semaphore(10);
    Semaphore full = new Semaphore(0);
    Mutex mutex = new Mutex();
    Integer item_produced = 10;

   class Semaphore{
       
       int value;
       Semaphore(int val)
       {
          value = val;
       }
       public synchronized void acquire_buffer() throws InterruptedException
       {
            while(value==0)
            {
                wait();
            }
            value = value -1;
       }

       public synchronized void release_buffer()throws InterruptedException{
           value = value + 1;
           notify();
       }
   };
    class Mutex {
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

    class Producer implements Runnable {
        public void run() {
            while (true) {
                try {
                    
                    while(item_produced >0)
                    {
                        empty.acquire_buffer();
                        mutex.lock();
                        System.out.println("Item produced is " + item_produced +" .....");
                        q.add(item_produced);
                        item_produced = item_produced - 1;
                        mutex.unlock();
                        full.release_buffer();
                        Thread.sleep(500);
                    }
                } catch (Exception e) {
                    System.out.println("Error in Producer");
                }
            }
        }
    }

    class Consumer implements Runnable {
        public void run() {
            while (true) {
                try {
                    full.acquire_buffer();
                    mutex.lock();
                    while(!q.isEmpty())
                    {
                        int item = q.poll();
                        System.out.println("Item consumed is " + item + " ....");
                        mutex.unlock();
                        empty.release_buffer();
                        Thread.sleep(1500);
                    }
                } catch (Exception e) {
                    System.out.println("Error in Consumer");
                }
            }
        }
    }

    public static void main(String[] args) {
        mutex_semaphore obj = new mutex_semaphore();
        Thread producer = new Thread(obj.new Producer());
        Thread consumer = new Thread(obj.new Consumer());
        producer.start();
        consumer.start();
    }
}
