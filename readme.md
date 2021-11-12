# Python Script .. 

- doWork("Goods[]") 
- Empty ShoppingCarts
- Postman Scripts to Generate OrderId
- Run Prom

# Third party lib in requirement.
- pika==1.2.0

# What You Should Install 
  [https://www.npmjs.com/package/newman](https://www.npmjs.com/package/newman)



wt --title Goods -p Goods --tabColor "#009999" -d "D:\proj\everrich-ec-backend\EverRich.EC\Services\Goods\EverRich.EC.Services.Goods" cmd /k "dotnet run" ;
wt new-tab --title Invoice -p Invoice -d "D:\proj\everrich-ec-backend\EverRich.EC\Services\Invoice\EverRich.EC.Services.Invoice" cmd /k "dotnet run" ;
wt new-tab --title Logistics -p Logistics -d "D:\proj\everrich-ec-backend\EverRich.EC\Services\Logistics\EverRich.EC.Services.Logistics" cmd /k "dotnet run" ;
wt new-tab --title Members -p Members -d "D:\proj\everrich-ec-backend\EverRich.EC\Services\Members\EverRich.EC.Services.Members" cmd /k "dotnet run" ;
wt new-tab --title Order -p Order -d "D:\proj\everrich-ec-backend\EverRich.EC\Services\Order\EverRich.EC.Services.Order" cmd /k "dotnet run" ;
wt new-tab --title Payment -p Payment -d "D:\proj\everrich-ec-backend\EverRich.EC\Services\Payment\EverRich.EC.Services.Payment" cmd /k "dotnet run" ;
wt new-tab --title ShoppingCart -p ShoppingCart -d "D:\proj\everrich-ec-backend\EverRich.EC\Services\ShoppingCart\EverRich.EC.Services.ShoppingCart" cmd /k "dotnet run" ;
wt new-tab --title Promotion -p Promotion --tabColor "#007500" -d "D:\proj\everrich-ec-backend\EverRich.EC\Services\Promotion\EverRich.EC.Services.Promotion" cmd /k "dotnet run" ;
wt new-tab --title WebApi -p WebApi --tabColor "#FF0080" -d "D:\proj\everrich-ec-backend\EverRich.EC\WebAPI\EverRich.EC.WebAPI" cmd /k "dotnet run" ;
wt new-tab --title PikaChu -p PikaChu --tabColor "#005757" -d "C:\Users\coder\Desktop\NewMan" --suppressApplicationTitle ; 
