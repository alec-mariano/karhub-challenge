SELECT 
    d.`ID Fonte de Recursos`, 
    a.`Nome Fonte de Recursos`,
    ROUND(AVG(d.`Liquidado`), 2) AS `Media Gastos`
FROM 
    `orcamento.sp_des_2022` AS d
JOIN 
    `orcamento.sp_agg_2022` AS a
ON 
    d.`ID Fonte de Recursos` = a.`ID Fonte de Recursos`
GROUP BY 
    d.`ID Fonte de Recursos`, 
    a.`Nome Fonte de Recursos`
ORDER BY 
    `Media Gastos` DESC;