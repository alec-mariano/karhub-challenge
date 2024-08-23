SELECT 
    `Nome Fonte Recurso`, 
    `Total Arrecadado`
FROM 
    `orcamento.sp_2022`
ORDER BY 
    `Total Arrecadado` DESC
LIMIT 5;