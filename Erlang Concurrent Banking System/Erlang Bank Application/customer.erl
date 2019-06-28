-module(customer).
-export([loan/4]).
-import(bank,[fund/2]).

loan(Customer_Name, Customer_Loan, Banks, Customers)->
  receive
    {Id} ->
      Customer_Req_Loan_Amount=get_customer_loan_amount_for_request(Customer_Loan),
      Bank=get_bank_for_request(Banks),
      Msg=io_lib:format("~p requests a loan of ~p dollar(s) from ~p~n",[Customer_Name, Customer_Req_Loan_Amount, Bank]),
      Id ! {Msg},
      whereis(Bank) ! {Customer_Name, Customer_Req_Loan_Amount, self(), Id},
      loan(Customer_Name, Customer_Loan, Banks, Customers);
    {true, Customer_Req_Loan_Amount, Main_Process_Id} when Customer_Loan- Customer_Req_Loan_Amount >0->
      Customer_Loan_New= Customer_Loan- Customer_Req_Loan_Amount,
      Customer_Req_Loan_Amount_New=get_customer_loan_amount_for_request(Customer_Loan_New),
      Bank_New=get_bank_for_request(Banks),
      Msg_New=io_lib:format("~p requests a loan of ~p dollar(s) from ~p~n",[Customer_Name, Customer_Req_Loan_Amount_New, Bank_New]),
      Main_Process_Id !{Msg_New},
      whereis(Bank_New) ! {Customer_Name, Customer_Req_Loan_Amount_New, self(), Main_Process_Id},
      loan(Customer_Name, Customer_Loan_New, Banks, Customers);
    {true, Customer_Req_Loan_Amount, Main_Process_Id} when Customer_Loan- Customer_Req_Loan_Amount ==0->
      Customer_Loan_New= Customer_Loan- Customer_Req_Loan_Amount,
      loan(Customer_Name, Customer_Loan_New, Banks, Customers),
      Main_Process_Id ! {};
    {false, Main_Process_Id} ->
      Customer_Req_Loan_Amount_Ne=get_customer_loan_amount_for_request(Customer_Loan),
      Bank_Ne=get_bank_for_request(Banks),
      Msg_Ne=io_lib:format("~p requests a loan of ~p dollar(s) from ~p~n",[Customer_Name, Customer_Req_Loan_Amount_Ne, Bank_Ne]),
      Main_Process_Id ! {Msg_Ne},
      whereis(Bank_Ne) ! {Customer_Name, Customer_Req_Loan_Amount_Ne, self(), Main_Process_Id},
      loan(Customer_Name, Customer_Loan, Banks, Customers);
    {remove, Bank_Name} ->
      unregister(Bank_Name),
      loan(Customer_Name, Customer_Loan, Banks, Customers)
    after 650 ->
          display_customer_report(Customers, Customer_Name, Customer_Loan)
    end.


get_customer_loan_amount_for_request(Customer_Loan)->
  if
    Customer_Loan == 0 ->
      Customer_Loan;
    Customer_Loan =< 50 ->
      rand:uniform(Customer_Loan);
    Customer_Loan > 50 ->
      rand:uniform(50)
  end.

get_bank_for_request(Banks)->
  Bank_Index=rand:uniform(length(Banks)),
  {Bank_Name,_}=lists:nth(Bank_Index, Banks),
  Bank_Name.

display_customer_report(Customers, Customer_Name, Customer_Loan)->
  if
    Customer_Loan == 0 ->
      {_,Customer_Target}=lists:keyfind(Customer_Name, 1, Customers ),
      io:format("~p has reached the objective of ~p dollar(s). Woo Hoo!~n",[Customer_Name, Customer_Target]);
    true->
      {_,Customer_Target}=lists:keyfind(Customer_Name, 1, Customers ),
      io:format("~p was only able to borrow ~p dollar(s). Boo Hoo!!~n",[Customer_Name, Customer_Target-Customer_Loan])
  end.
