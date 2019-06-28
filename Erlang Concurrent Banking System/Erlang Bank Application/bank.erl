-module(bank).
-export([fund/2]).

fund(Bank_Name, Bank_Fund)->
  receive
    {Customer_Name, Customer_Req_Loan_Amount, Customer_Id, Main_Process_Id} when Bank_Fund == 0 ->
      Msg=io_lib:format("~p denies a loan of ~p dollar(s) from ~p~n",[Bank_Name, Customer_Req_Loan_Amount, Customer_Name]),
      Main_Process_Id ! {Msg},
      Customer_Id ! {remove, Bank_Name},
      fund(Bank_Name, Bank_Fund);
    {Customer_Name, Customer_Req_Loan_Amount, Customer_Id, Main_Process_Id} when Customer_Req_Loan_Amount > Bank_Fund ->
      Msg_New=io_lib:format("~p denies a loan of ~p dollar(s) from ~p~n",[Bank_Name, Customer_Req_Loan_Amount, Customer_Name]),
      Main_Process_Id ! {Msg_New},
      Customer_Id ! {false, Main_Process_Id},
      fund(Bank_Name, Bank_Fund);
    {Customer_Name, Customer_Req_Loan_Amount, Customer_Id, Main_Process_Id} when Customer_Req_Loan_Amount =< Bank_Fund ->
      Msg_Ne=io_lib:format("~p approves a loan of ~p dollar(s) from ~p~n",[Bank_Name, Customer_Req_Loan_Amount, Customer_Name]),
      Main_Process_Id ! {Msg_Ne},timer:sleep(10),
      Customer_Id ! {true, Customer_Req_Loan_Amount, Main_Process_Id},
      fund(Bank_Name, Bank_Fund - Customer_Req_Loan_Amount)
     after 650->
      io:format("~p has ~p dollar(s) remaining.~n",[Bank_Name, Bank_Fund])
  end.
