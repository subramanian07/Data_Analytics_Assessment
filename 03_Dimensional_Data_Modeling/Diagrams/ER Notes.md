# flowchart TB

    FactSales[FactSales]
    FactReturns[FactReturns]

    DimDate[DimDate]
    DimCustomer[DimCustomer]
    DimProduct[DimProduct]
    DimProductCategory[DimProductCategory]
    DimStore[DimStore]
    DimPromotion[DimPromotion]

## Relationships:
### Star Schema
    DimDate --> FactSales
    DimCustomer --> FactSales
    DimProduct --> FactSales
    DimStore --> FactSales
    DimPromotion --> FactSales

    DimDate --> FactReturns
    DimCustomer --> FactReturns
    DimProduct --> FactReturns
    DimStore --> FactReturns
    
### Snowflake Schema
    DimProduct --> DimProductCategory