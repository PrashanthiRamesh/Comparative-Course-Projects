-module(money).
-export([start/0, create_processes/2, print_message/0]).
-import(customer,[loan/4]).
-import(bank, [fund/2]).

start()->
  io:fwrite("\n** Customers and loan objectives **\n"),
  Input_Customers_File_Data = file:consult("customers.txt"),
	Customers_Data=element(2,Input_Customers_File_Data),
	Customers=maps:from_list(Customers_Data),
	maps:fold(fun(Customer_Name, Customer_Loan, ok) -> io:format("~p: ~p~n", [Customer_Name, Customer_Loan]) end, ok, Customers),
	io:fwrite("~n"),
  io:fwrite("** Banks and financial resourses **\n"),
  Input_Banks_File_Data = file:consult("banks.txt"),
	Banks_Data=element(2,Input_Banks_File_Data),
	Banks=maps:from_list(Banks_Data),
	maps:fold(fun(Bank_Name, Bank_Fund, ok) -> io:format("~p: ~p~n", [Bank_Name, Bank_Fund]) end, ok, Banks),
	io:fwrite("~n"),
  spawn(money, create_processes,[Customers_Data, Banks_Data]).


create_processes(Customers_Data, Banks_Data)->
  Banks=maps:from_list(Banks_Data),
  Bank_Process=fun(Bank_Name,Bank_Fund,Acc)-> Bank_Process_Id = spawn(bank, fund, [Bank_Name,Bank_Fund]), register(Bank_Name,Bank_Process_Id), Bank_Process_Id ! {self()} end,
  maps:fold(Bank_Process,[],Banks),
  Customers=maps:from_list(Customers_Data),
  Customer_Process=fun(Customer_Name,Customer_Loan,Acc)-> Customer_Process_Id = spawn(customer, loan, [Customer_Name,Customer_Loan, Banks_Data, Customers_Data]), Customer_Process_Id ! {self()} end,
  maps:fold(Customer_Process,[],Customers),
  print_message().

print_message()->
  receive
      {Message} ->
        io:format("~s~n", [Message]),
        print_message()
  end.
