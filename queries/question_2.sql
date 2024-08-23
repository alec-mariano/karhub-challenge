SELECT 
    `Nome Fonte Recurso`, 
    `Total Liquidado`
FROM 
    `orcamento.sp_2022`
ORDER BY 
    `Total Liquidado` DESC
LIMIT 5;