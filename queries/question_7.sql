SELECT 
    r.`ID Fonte de Recursos`, 
    a.`Nome Fonte de Recursos`,
    ROUND(AVG(r.`Arrecadado`), 2) AS `Media Arrecadacao`
FROM 
    `orcamento.sp_rec_2022` AS r
JOIN 
    `orcamento.sp_agg_2022` AS a
ON 
    r.`ID Fonte de Recursos` = a.`ID Fonte de Recursos`
GROUP BY 
    r.`ID Fonte de Recursos`, 
    a.`Nome Fonte de Recursos`
ORDER BY 
    `Media Arrecadacao` DESC;