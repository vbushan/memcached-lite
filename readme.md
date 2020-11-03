### Procedure to run the files:

1) Place all the files in a single directory.

2) Run the server using the command python3 server.py 

3) To run an individual client or manually create different sessions of clients open new terminal windows and type python3 client.py. Make sure that the server is running before running this command. After the client is ready, run the get or set commands as specified in the assignment description. For example: 
    
    i) set Hello 5
    ii) Vamsi

    Or

    i) get Hello
     
4) To run the test scripts, open a new terminal and type the command- python3 clientTest.py.

Note: I have print statements for debugging and info. I will replace them in the subsequent assignments with logs. While running the test script, the server terminal would have a deluge of log statements. In order to avoid it, you can pipe the log statements into a log file, by using the command python3 server.py | cat 1>log.txt 2>output.txt. After this command, run the clientTest.py file.
