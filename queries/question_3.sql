SELECT 
    `Nome Fonte Recurso`, 
    `Total Arrecadado`, 
    `Total Liquidado`, 
    (`Total Arrecadado` - `Total Liquidado`) AS `Margem Bruta`
FROM 
    `orcamento.sp_2022`
ORDER BY 
    `Margem Bruta` DESC
LIMIT 5;