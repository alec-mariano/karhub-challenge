SELECT 
    `Nome Fonte Recurso`, 
    `Total Liquidado`
FROM 
    `orcamento.sp_2022`
ORDER BY 
    `Total Liquidado` ASC
LIMIT 5;
