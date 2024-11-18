import xmlrpc.client

def main():
    proxy = xmlrpc.client.ServerProxy("http://localhost:8000/RPC2")
    
    while(True):
    
        print("\nSelect an operation:")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Square")
        print("4. Cube")
        
        choice = input("Enter choice")
        
        if choice == '1':
            x = int(input("Enter first num"))
            y = int(input("Enter second num"))
            
            result = proxy.add(x,y)
            print(f"Addition result: {result:}")
            
        elif choice =='2':
            x = int(input("Enter first num"))
            y = int(input("Enter second num"))
            result = proxy.subtract(x,y)
            print(f"Substraction result: {result}")
            
        elif choice == '3':
            x = int(input("Enter first num"))
            result = proxy.square(x)
            print(f"Square : {result}")
            
        elif choice == '4':
            x = int(input("Enter first num"))
            result = proxy.cube(x)
            print(f"Cubing result: {result}")
        elif choice == '5':
            print("Exiting")
            break
        else:
            print("Invalid choice")
            
        
if __name__ == "__main__":
    main()
             
        
    